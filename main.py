# -*- coding: utf-8 -*-
# APK-версия "Личный доходяга". Вся игровая логика сохранена 1-в-1.
# Изменения только технические: print/input/sleep/display зампатчены для Android.
import os
import sys
import random
import time
import builtins

sys.setrecursionlimit(10000)

import pygame
pygame.init()
# Явные параметры для Android — без них звук может не работать
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
pygame.font.init()

# ---- Экран ----
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Личный доходяга")

SMALL_FONT = pygame.font.Font(None, max(28, HEIGHT // 42))
BIG_FONT   = pygame.font.Font(None, max(40, HEIGHT // 30))

# ---- Путь к ресурсам ----
image_path = os.path.dirname(os.path.abspath(__file__)) + "/"
if not os.path.exists(image_path + "Festival.mp3"):
    image_path = "/data/data/org.dohodyaga.lichdohod/files/app/"

# ---- Флаг: сейчас показывается картинка ----
image_showing = False

# ---- Текстовый лог ----
text_log = []
pending = ""
MAX_LOG = 200
MAX_LINES = 22


def _redraw():
    if image_showing:
        return
    screen.fill((0, 0, 0))
    y = 10
    for line in text_log[-MAX_LINES:]:
        if y > HEIGHT - 20:
            break
        surf = SMALL_FONT.render(str(line), True, (255, 255, 255))
        screen.blit(surf, (10, y))
        y += SMALL_FONT.get_linesize()
    if pending and y < HEIGHT - 20:
        surf = SMALL_FONT.render(str(pending), True, (255, 255, 255))
        screen.blit(surf, (10, y))
    pygame.display.flip()


def show_text(text):
    global pending
    for i, line in enumerate(str(text).split("\n")):
        if i > 0:
            text_log.append(pending)
            pending = ""
        pending += line
    while len(text_log) > MAX_LOG:
        text_log.pop(0)
    _redraw()


_orig_sleep = time.sleep


def wait(seconds):
    t0 = time.time()
    while time.time() - t0 < seconds:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
        _redraw()
        _orig_sleep(0.1)


def get_input(prompt=""):
    if prompt:
        show_text(prompt)
    try:
        pygame.key.start_text_input()
    except Exception:
        pass
    buf = ""
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if e.key == pygame.K_RETURN:
                    try:
                        pygame.key.stop_text_input()
                    except Exception:
                        pass
                    return buf
                if e.key == pygame.K_BACKSPACE:
                    buf = buf[:-1]
            if hasattr(pygame, "TEXTINPUT") and e.type == pygame.TEXTINPUT:
                buf += e.text
        if not image_showing:
            _redraw()
            pygame.draw.rect(screen, (40, 40, 40), (10, HEIGHT - 60, WIDTH - 20, 50))
            pygame.draw.rect(screen, (200, 200, 200), (10, HEIGHT - 60, WIDTH - 20, 50), 2)
            surf = BIG_FONT.render(buf, True, (255, 255, 255))
            screen.blit(surf, (20, HEIGHT - 55))
            pygame.display.flip()
        _orig_sleep(0.03)


# ---- Патчим встроенные функции ----
def _android_print(*args, **kwargs):
    end = kwargs.get("end", "\n")
    sep = kwargs.get("sep", " ")
    show_text(sep.join(str(a) for a in args) + end)


def _patched_sleep(seconds):
    wait(seconds)


builtins.print = _android_print
builtins.input = get_input
time.sleep = _patched_sleep


# ---- Патчим pygame.display для показа картинок ----
def _set_mode(*a, **kw):
    global image_showing
    screen.fill((0, 0, 0))
    image_showing = True
    return screen


def _quit():
    global image_showing
    image_showing = False
    _redraw()


def _init():
    pass


pygame.display.set_mode = _set_mode
pygame.display.quit = _quit
pygame.display.init = _init


# ============================================================
# ТВОЙ ОРИГИНАЛЬНЫЙ КОД. Логика не изменена.
# ============================================================

breakingg = 0
lomka = 0
pohod = 0
sideB = 0


def Breaking(povtor_func): 
    global lomka 
    global breakingg
    print()
    print("Выбери другое число.")
    print()
    breakingg += 1
    if breakingg == 6:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(image_path + "Weird_Sound.mp3")
        pygame.mixer.music.play()
        time.sleep(6)
        pygame.mixer.music.load(image_path + "Festival.mp3")
        pygame.mixer.music.play(-1)
        if lomka >= 6:
            pygame.mixer.music.load(image_path + "Happy_town.ogg")
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.load(image_path + "Festival.mp3")
            pygame.mixer.music.play(-1)
        Festival()
    else:
        povtor_func()


def pirozhok():
    print("Хотите попробовать пирожок?")
    time.sleep(1)
    print("1. Да")
    time.sleep(1)
    print("2. Нет")
    time.sleep(1)
    print("3. Отдать пирожок доходяге")
    time.sleep(1)
    user_input = input("Решение: ").strip()
    
    if user_input.isdigit():
        pirog = int(user_input)
    else:
        return Breaking(pirozhok)
        
    if pirog == 1:
        print("* Вы попробовали пирожок")
        time.sleep(2)
        print("* Он на вкус как Онионсан")
        Festival() 
    elif pirog == 2:
        print("* Вы отказались есть пирожок и поэтому отдали его Сьюзи")
        time.sleep(2)
        if pohod == 0:
            print("Сьюзи: Офигенный пирожок, Ноэль попробуй!!!")
            print()
        else:
            print("Сьюзи: Офигенный пирожок, Крис попробуй!!!")
            time.sleep(3)
            print()
        Festival()
    elif pirog == 3:
        print("* Вы отдали пирожок Доходяге")
        time.sleep(2)
        print("* По его улыбке вы сразу поняли, что пирожок ему понравился")
        print()
        time.sleep(2)
        Festival()
    else:
        Breaking(pirozhok)


def cabinka():
    print("Раскачать кабинку?")
    print("1. Да")
    print("2. Нет")
    user_input = input("Решение: ").strip()
    
    if user_input.isdigit():
        cabin = int(user_input)
    else:
        return Breaking(cabinka)
    if cabin == 1:
        if pohod == 0:
            print("* Вы начали сильно раскачивать кабинку")
            time.sleep(0.5)
            if os.path.exists(image_path + "noelle.mp3"):
                noelle_sound = pygame.mixer.Sound(image_path + "noelle.mp3")
                noelle_sound.play()
                time.sleep(2)
            print("* После этого на Ноэль нахлынули воспоминания из детства")
            time.sleep(3)
            print("* Спустя несколько минут поездка окончилась")
            print()
            time.sleep(2)
        elif pohod == 1:
            print("Вы спокойно прокатились, смотря на прекрасный пейзаж")
            time.sleep(2)
    elif cabin == 2:
        print("Вы спокойно прокатились, смотря на прекрасный пейзаж")
    else:
        Breaking(cabinka)


def Festival():
    global pohod, lomka, breakingg, sideB
    print("1. Пойти покушать вкусного осьминога")
    print("2. Покататься на колесе обозрения")
    print("3. Взять вкусное мороженое у Санса")
    print("4. Искупаться в озере с Ноэль")
    print("5. Взять с собой Бердли?!?!?")
    print("6. Взять цветы у Азгора")
    print("7. Покинуть фестиваль")

    user_input = input("Выберите действие: ").strip()
    if user_input.isdigit():
        festivalChoice = int(user_input)
    else:
        return Breaking(Festival)

    if festivalChoice == 1:
        print()
        print("Продавец: Продаю пирожки из осьминога за 2 G...", end="", flush=True);time.sleep(3); print(" То есть бесплатно")
        time.sleep(2)
        pirozhok()
        print()
    elif festivalChoice == 2:
        if lomka < 6 and breakingg < 6:
            print()
            if pohod == 0:
                print("* Вы с остальными сели на колесо обозрения")
                time.sleep(4)
                print("* Вокруг города видно только осенний лес и озеро, покрытое золотистыми лучами солнца")
                time.sleep(6)
                cabinka()
                print()
            elif pohod == 1 and breakingg >= 6 and lomka >= 6:
                print("* Вы с остальной компанией, кроме Ноэлль, сели на колесо обозрения")
                time.sleep(4)
                print("* Вокруг города видно только осенний лес и озеро, покрытое золотистыми лучами солнца")
                print("* Около него стоит Ноэлль, любуясь закатом")
                time.sleep(6)
                cabinka()
                print()
        elif breakingg >= 6 and lomka >= 6 and pohod == 0:
            print()
            print("* Вы и Ноэлль садитесь в кабинку.")
            time.sleep(4)
            print("* Колесо начинает медленно вращаться.")
            time.sleep(4)
            print("Ноэль: Крис,", end="", flush=True);time.sleep(2); print(" сегодня ТЫ ведешь себя очень СТРАННО.")
            time.sleep(3)
            print("НоЭлЛь: ТЫ выбирал такие действия,", end="", flush=True);time.sleep(2); print(" которых нету.")
            time.sleep(3)
            print("НоэЛЛьь: Я ощущаю,", end="", flush=True);time.sleep(2); print(" рядом с тобой СТРАННУЮ силу,", end="", flush=True);time.sleep(2); print(" С ПОМОЩЬЮ КОТОРОЙ МОЖНО СДЕЛАТЬ ЧТО УГОДНО!!!")
            time.sleep(4)
            print("НоЭлЛь: ТАК ДАВАЙ С ТОБОЙ СДЕЛАЕМ БЕЗУМНЫЕ ВЕЩИ!!!")
            time.sleep(3)
            print("* Ноэлль ожидает вас у озера")
            time.sleep(3)
            pohod += 1
            print()
        Festival()

    elif festivalChoice == 3:
        if pohod == 0:
            print()
            print("* Ваша группа подошла к Сансу за мороженым")
            time.sleep(3)
            print("Санс: Ребятки, перед тем как я дам вам мороженое, вы должны выслушать мой анекдот")
            time.sleep(4)
            print("Сьюзи: Может ты нам просто дашь мороженое?")
            time.sleep(4)
            print("Санс: Итак мой анекдот: ")
            time.sleep(4)
            print("Сьюзи: Ноэль, за это мы с Крисом его ненавидим")
            time.sleep(3)
            print("Ноэль: Он же просто хочет нас развеселить!")
            time.sleep(4)
            print("Санс: Так и есть. В общем слушайте мой анекдот: ")
            time.sleep(4)
            print("Вчера вечером")
            time.sleep(1.5)
            print("Мы с мамой Криса")
            time.sleep(2)
            print("Трясли КОСТЯМи")
            time.sleep(4)
            print("Сьюзи: Крис, ты почему такой красный?", end="", flush=True);time.sleep(2); print(" Он что, твои КОСТОЧКИ задел?")
            time.sleep(3)
            print("Санс: Быстро учишься :)")
            time.sleep(2.5)
            print("Санс: Вот ваше мороженое, хорошего отдыха!!!")
            print()
        elif pohod == 1:
            print()
            print("* Ты, Сьюзи и Доходяга подошли к Сансу за мороженым")
            time.sleep(3)
            print("Санс: Ребятки, перед тем как я дам вам мороженое, вы должны нарисовать себя и друзей на карточке, чтобы я мог вас запомнить")
            time.sleep(5)
            print("Сьюзи: Ну как скажешь.", end="", flush=True);time.sleep(2);print(" Вот я, Крис и Ральзей")
            time.sleep(3)
            print("Сьюзи: Где наше бесплатное мороженое?")
            time.sleep(4)
            print("Санс: Какое бесплатное мороженое? Я просто попросил нарисовать рисунок, с тебя 0.6$")
            time.sleep(5)
            print("КРИС ПОШЛИ ОТСЮДА!!!")
            time.sleep(2)
            print()
        Festival()
    elif festivalChoice == 4:
        if breakingg >= 6 and lomka >=  6 and pohod == 0:
            print()
            print("* Вы спите.", end="", flush=True);time.sleep(2);print(" Вам снится,", end="", flush=True);time.sleep(2);print(" что вы утонули с Ноэлль в озере") 
        elif breakingg >= 6 and lomka >= 6 and pohod == 1:
            if os.path.exists(image_path + "Monolog.ogg"):
                pygame.mixer.music.load(image_path + "Monolog.ogg")
                pygame.mixer.music.play(-1)
            print()
            print("* Ноэлль стоит на берегу, и смотрит на ярко-огненный закат.")
            time.sleep(3)
            print("Ноэлль: Все это время Ноэлль была Ноэлль, а Крис - Крисом")
            time.sleep(3)
            print("Ноэлль: Но твои последние действия,", end="", flush=True);time.sleep(3);print(" не похожи на ТЕБЯ!!!")
            time.sleep(3)
            print("Ноэлль: ТЫ больше не занимался делами КРИСА,", end="", flush=True);time.sleep(2);print(" ТЫ занимался ДРУГИМИ ДЕЛАМИ")
            time.sleep(3)
            print("Ноэлль: Я тоже больше не хочу заниматся делами НОЭЛЛЬ,", end="", flush=True);time.sleep(4);print(" а также как и ты, Я ХОЧУ ЗАНИМАТСЯ РАЗНЫМИ ВЕЩАМИ!!!")
            time.sleep(5)
            print("Ноэлль: Скажи ЭТО и Я последую за ТОБОЙ")
            time.sleep(3)
            pygame.mixer.music.stop()
            print()
            print("1. Продолжай")
            print("2. Стой")
            proceed = input("ТЫ: ")
            if proceed == "1":
                weird_sound = pygame.mixer.Sound(image_path + "Weird_Sound.mp3")
                weird_sound.play()
                print("* Вы с Ноэлль зашли в озеро.")
            elif proceed == "2":
                print("Крис, не сопротивляйся!!!")
                time.sleep(3)
                print("* Вы с Ноэлль зашли в озеро.")
                time.sleep(3)
            else:
                proceed = "0"
                pygame.mixer.music.load(image_path + "Happy_town.ogg")
                pygame.mixer.music.play(-1)
                print()
                Festival()
            proceed = "0"
            print()
            print("1. Продолжай")
            print("2. Остановись")
            proceed = input("ТЫ: ")
            if proceed == "1":
                weird_sound = pygame.mixer.Sound(image_path + "Weird_Sound.mp3")
                weird_sound.play()
                print("* Вы с Ноэлль стоите поколено в воде.")
                time.sleep(3)
                print("Ноэлль: Разве вода не прекрасная, Крис?")
                time.sleep(2)
            elif proceed == "2":
                print("Ноэлль: Крис, ПЕРЕСТАНЬ СОПРАТИВЛЯТЬСЯ!!!")
                time.sleep(2)
                print("* Ноэлль завела вас поколено в воду.")
                time.sleep(2)
            else:
                proceed = "0"
                print()
                pygame.mixer.music.load(image_path + "Happy_town.ogg")
                pygame.mixer.music.play(-1)
                Festival()
            proceed = "0"
            print()
            print("1. Продолжай")
            print("2. МОЛЮ, ПЕРЕСТАНЬ!!!")
            proceed = input("ТЫ: ")
            if proceed == "1":
                weird_sound = pygame.mixer.Sound(image_path + "Weird_Sound.mp3")
                weird_sound.play()
                print("* Вы кое-как можете дышать.")
                time.sleep(3)
                print("Ноэлль: КРИС, ПРОДОЛЖАЙ!!!")
                time.sleep(3)
            elif proceed == "2":
                print("Ноэлль: КРИС, ПОЙДЕМ!!!")
                time.sleep(3)
                print("* Вы кое-как можете дышать.")
                time.sleep(3)
            else:
                proceed = "0"
                pygame.mixer.music.load(image_path + "Happy_town.ogg")
                pygame.mixer.music.play(-1)
                print()
                Festival()
            proceed = "0"
            print()
            print("1. Продолжай")
            print("2. ХВАТИТ!!!")
            proceed = input("ТЫ: ")
            if proceed == "1":
                weird_sound = pygame.mixer.Sound(image_path + "Weird_Sound.mp3")
                weird_sound.play()
                print("* Вы ушли под воду.")
                time.sleep(2)
                print("* КРИС, ТЫ МЕНЯ СЛЫШИШЬ?!?!?")
                time.sleep(2)
            elif proceed =="2":
                time.sleep(3)
                lomka = 0
                breakingg = 0
                pohod = 0
                proceed = "0"
                print()
                pygame.mixer.music.load(image_path + "Festival.mp3")
                pygame.mixer.music.play(-1)
                lomka = 0
                breakingg = 0
                pohod = 0
                proceed = "0"
                Festival()
            else:
                proceed = "0"
                print()
                pygame.mixer.music.load(image_path + "Happy_town.ogg")
                pygame.mixer.music.play(-1)
                Festival()
            proceed = "0"
            print()
            if os.path.exists(image_path + "inversion_lake_chant.ogg"):
                pygame.mixer.music.load(image_path + "inversion_lake_chant.ogg")
                pygame.mixer.music.play(-1)
            print("1. Продолжай")
            print("2. Продолжай")
            proceed = input("ТЫ: ")
            if proceed == "1":
                weirder_sound = pygame.mixer.Sound(image_path + "Snd_ominous_hell_music.wav")
                weirder_sound.play()
                print("* ПРОДОЛЖАЙ!!!")
                time.sleep(2)
            elif proceed =="2":
                weirder_sound = pygame.mixer.Sound(image_path + "Snd_ominous_hell_music.wav")
                weirder_sound.play()
                print("* ПРОДОЛЖАЙ!!!")
                time.sleep(2)
            else:
                proceed = "0"
                pygame.mixer.music.load(image_path + "Happy_town.ogg")
                pygame.mixer.music.play(-1)
                print()
                Festival()
            proceed = "0"
            print()
            print("1. Продолжай")
            print("2. Продолжай")
            proceed = input("ТЫ: ")
            if proceed == "1":
                weirder_sound = pygame.mixer.Sound(image_path + "Snd_ominous_hell_music.wav")
                weirder_sound.play()
            elif proceed =="2":
                weirder_sound = pygame.mixer.Sound(image_path + "Snd_ominous_hell_music.wav")
                weirder_sound.play()
            else:
                proceed = "0"
                pygame.mixer.music.load(image_path + "Happy_town.ogg")
                pygame.mixer.music.play(-1)
                print()
                Festival()
            proceed = "0"
            print()
            print("1. Продолжай")
            print("2. Продолжай")
            proceed = input("ТЫ: ")
            if proceed == "1":
                weirder_sound = pygame.mixer.Sound(image_path + "Snd_ominous_hell_super_music.wav")
                weirder_sound.play()
                time.sleep(4)
            elif proceed =="2":
                weirder_sound = pygame.mixer.Sound(image_path + "Snd_ominous_hell_super_music.wav")
                weirder_sound.play()
                time.sleep(4)
            else:
                proceed = "0"
                pygame.mixer.music.load(image_path + "Happy_town.ogg")
                pygame.mixer.music.play(-1)
                print()
                Festival()
            proceed = "0"
            print()
            pygame.mixer.music.stop()
            weirder_sound = pygame.mixer.Sound(image_path + "Snd_next_music.wav")
            weirder_sound.play()
            print("Вставьте программу: <<Личный доходяга>>, стороной B.")
            time.sleep(11)
            lomka = 0
            breakingg = 0
            pohod = 0
            proceed = "0"
            sideB += 1
            pygame.mixer.music.load(image_path + "Festival.mp3")
            pygame.mixer.music.play(-1)
            return Festival()
        elif breakingg <= 6 and lomka <= 6 and pohod == 0:
            pygame.mixer.music.load(image_path + "I_guess_I'm_in_love.mp3")
            pygame.mixer.music.play(-1)
            print()
            print("* Вы спите.", end="", flush=True);time.sleep(3);print(" Но сквозь сон вы слышите,", end="", flush=True);time.sleep(3); print(" как болтают Сьюзи и Ноэлль")
        else:
            print()
            print("*Вы спите.", end="", flush=True);time.sleep(2);print(" Вам снится,", end="", flush=True);time.sleep(2);print(" что вы утонули с Ноэлль в озере")
            time.sleep(3)
        pygame.mixer.music.load(image_path + "Festival.mp3")
        pygame.mixer.music.play(-1)
        print()
        Festival()

    elif festivalChoice == 5:
        print()
        if pohod == 0:
            print("Сьюзи, Ноэль и Доходяга: КАКОЙ БЕРДЛИ?!?!? МЫ ЕГО НЕ ВОЗМЕМ!!!")
            time.sleep(3)
        elif pohod == 1:
            print("Сьюзи и Доходяга: КАКОЙ БЕРДЛИ?!?!? МЫ ЕГО НЕ ВОЗМЕМ!!!")
        print()
        Festival()
    elif festivalChoice == 6:
        if pohod == 0:
            print()
            print("* Ваша дружная компания подошла к Азгору")
            time.sleep(3)
            print("Азгор: Крис, как я рад снова видеть тебя на фестивале с Ноэль!!!")
            time.sleep(4)
            print("Азгор: Если вам нужны цветы, то берите. Для друзей моей семьи все бесплатно!")
            time.sleep(4)
            print("Ноэль: Никогда себя не прощу, если не заплачу ему")
        elif pohod == 1:
            print()
            print("* Магазин Азгора закрыт.")
            time.sleep(2)
            print("* На берегу вы видете Ноэлль, которая освещена золотисто - оранжевыми лучами солнца. Она ожидает вас.")
            time.sleep(4)
        print()
        Festival()
    elif festivalChoice == 7:
        print()
        print("Вы покидаете Фестиваль...")
        print()
        pygame.mixer.music.stop()
        time.sleep(2)
    else:
        Breaking(Festival)


vopros = 0
vopros2 = 0
vopros3 = 0
pygame.mixer.init()

yaderki = []

while True:
    print("\n=== Личный доходяга: развлечения на корабле ===")
    print("1. Добавить игру для Доходяги")
    print("2. Показать все игры в которые Доходяга не поиграл")
    print("3. Отметить игру в которую Доходяга поиграл")
    print("4. Удалить развлечение из расписания")
    print("5. Дать Доходяге воды из кулера")
    print("6. Устроить Доходяге свиданку с анимешной кошко-девочкой")
    print("7. Начать ЧАС ТВ")
    print("8. Выйти и отпустить Доходягу в свободное плаванье")
    print("9. JARONA!!!")
    print("10. Добавить ральзея в контакты")
    print("11. Сходить на Фестиваль с Доходягой")
    try:
        nochoice = input("Выберите пункт меню: ")
    except KeyboardInterrupt:
        continue
    if nochoice == "1":
        new_reznya = input("Введите новое развлечение для Доходяги: ").strip()
        if new_reznya:
            yaderki.append(new_reznya)
            print("Развлечение добавлено! Доходяга идет развлекаться.")
            
            if random.randint(1, 100) == 1:
                if os.path.exists(image_path + "glacier.mp3"):
                    pygame.mixer.music.load(image_path + "glacier.mp3")
                    pygame.mixer.music.play()
                    time.sleep(67)
                else:
                    print("Файл не найден в папке со скриптом!")
        else:
            print("Нельзя заставить Доходягу скучать.")

    elif nochoice == "2":
        if yaderki:            
            print("Развлечения Доходяги:")
            for i, task in enumerate(yaderki):
                print(f"{i + 1}. {task}")
        else:
            print("Доходяга скучает.")

    elif nochoice == "3":
        if yaderki:
            for i, task in enumerate(yaderki):
                print(f"{i + 1}. {task}")
            try:
                task_num = int(input("Введите номер игры, в которую Доходяга обязан играть: "))
                if 1 <= task_num <= len(yaderki):
                    completed = yaderki.pop(task_num - 1)
                    print(f"Игра '{completed}' сыграна Доходягой.")
                else:
                    print("Неверный номер игры.")
            except ValueError:
                print("Введите число!")
        else:
            print("Доходяга скучает.")

    elif nochoice == "4":
        if yaderki:
            for i, task in enumerate(yaderki):
                print(f"{i+1}. {task}")
            try:
                task_num = int(input("Введите номер игры, в которую Доходяга больше не играет: "))
                if 1 <= task_num <= len(yaderki):
                    removed = yaderki.pop(task_num - 1)
                    print(f"Игра '{removed}' УДАЛЕНА И ДОХОДЯГА БУДЕТ СКУЧАТЬ ДО КОНЦА ЕГО ДНЕЙ!!! .")
                else:
                    print("Неверный номер игры.")
            except ValueError:
                print("Введите число!")
        else:
            print("Доходяга скучает.")

    elif nochoice == "8":
        print("Вы отправили ДОХОДЯГУ в свободное плаванье!")
        break

    elif nochoice == "9":
        print()
        print("JARONA!!!")
        if os.path.exists(image_path + "jarona.mp3"):
            pygame.mixer.music.load(image_path + "jarona.mp3")
            pygame.mixer.music.play()
            if random.randint(1, 10) == 1:
                time.sleep(2)
                print("Ральзей: Флаувери,", end ="", flush=True); time.sleep(1); print(" ЗАТКНИСЬ!!!")
                time.sleep(4)
                if os.path.exists(image_path + "HeyRaly.mp3"):
                    pygame.mixer.music.load(image_path + "HeyRaly.mp3")
                    pygame.mixer.music.play()
                if os.path.exists(image_path + "jarona.mp3"): 
                    print("Flowery: Hey Raly,", end="", flush=True); time.sleep(3); print(" you didn't like my ", end="", flush=True); time.sleep(1.5); pygame.mixer.music.load(image_path + "jarona.mp3"); pygame.mixer.music.play(); print("JARONA?")
                time.sleep(3)
                print("Ральзей: Флаувери,",end="", flush=True); time.sleep(2); print(" КАК ТЫ МЕНЯ ЗАЕ...")
                time.sleep(1)
                if os.path.exists(image_path + "nonono.mp3"):
                    pygame.mixer.music.load(image_path + "nonono.mp3")
                    pygame.mixer.music.play()
                print("Flowery: No no no")
                time.sleep(3)
                if os.path.exists(image_path + "TakeThat.mp3"):
                    pygame.mixer.music.load(image_path + "TakeThat.mp3")
                    pygame.mixer.music.play()
                print("Flowery: Take THAT!")
                time.sleep(1)
                print("Ральзей: ТОЛЬКО НЕ ЭТ...")
                if os.path.exists(image_path + "splat.mp3"):
                    pygame.mixer.music.load(image_path + "splat.mp3")
                    pygame.mixer.music.play()
                time.sleep(3)
                if random.randint(1, 10) == 1:
                    if os.path.exists(image_path + "ja-st-kidding.mp3"):
                        pygame.mixer.music.load(image_path + "ja-st-kidding.mp3")
                        pygame.mixer.music.play()
                        print("Flowery: Ja-st kidding!")
                        time.sleep(2)
                        if os.path.exists(image_path + "Goodbye.mp3"):
                            pygame.mixer.music.load(image_path + "Goodbye.mp3")
                            pygame.mixer.music.play()
                            print("Flowery: Goodbye")
                            print()
                            time.sleep(2)
                else:
                    if os.path.exists(image_path + "Kris.mp3"):
                        pygame.mixer.music.load(image_path + "Kris.mp3")
                        pygame.mixer.music.play()
                    print("Flowery: Kris,", end="", flush=True); time.sleep(2); print(" don't tell anyone,", end="", flush=True); time.sleep(2); print(" okay?")
                    time.sleep(3)
                    if os.path.exists(image_path + "Goodbye.mp3"): 
                        print("Flowery: Now,", end="", flush=True); time.sleep(1.5); pygame.mixer.music.load(image_path + "Goodbye.mp3"); pygame.mixer.music.play(); print(" goodbye")
                        print()
                        time.sleep(2)
            elif random.randint(1, 10) == 2:
                image = pygame.image.load(image_path + "ABSOLUTE_JARONA.jpg")
                img_width = image.get_width()
                img_height = image.get_height()
                window = pygame.display.set_mode((img_width, img_height), pygame.NOFRAME)
                window.blit(image, (0, 0))
                pygame.display.flip()
                time.sleep(0.5)
                pygame.display.quit()
                pygame.display.init()
            else:
                vopros = 0
        else:
            print("АБСОЛЮТНАЯ ДЖАРОНА ПОТЕРЯЛАСЬ :(((")

    elif nochoice == "5":
        if random.randint(1, 50) == 1:
            if os.path.exists(image_path + "powers-combined.mp3"):
                pygame.mixer.music.load(image_path + "powers-combined.mp3")
                pygame.mixer.music.play()
                print()
            print("Кулер грозно на вас посмотрел")
            time.sleep(4)
            print("Кулер вас избил и не отдал свою воду")
            time.sleep(4)
            print("Вы стоите на коленях перед кулером и молите о пощаде")
            time.sleep(4)
            print("У вас 0.6 хп")
            print()
            time.sleep(3)
            pygame.mixer.music.stop()
        else:
            print()
            print("Вы налили воды и отдали ее Доходяге")
            print()

    elif nochoice == "6":
        if os.path.exists(image_path + "thousand_cafe_zukan.mp3"):
            pygame.mixer.music.load(image_path + "thousand_cafe_zukan.mp3")
            pygame.mixer.music.play()
            print()
            print("Вы начали свиданку Доходяги с анимешной кошко-девочкой")
            time.sleep(6)
            print("Гастер: А ты в курсе, что этот Доходяга ходит на свиданку с каждой кошко-девочкой?")
            time.sleep(2)
            
            if os.path.exists(image_path + "OMG.mp3"):
                omg_sound = pygame.mixer.Sound(image_path + "OMG.mp3")
                omg_sound.play()
            time.sleep(4.3)
            print("Нормальный NPC: И причем каждая анимешная!")
            time.sleep(2)
            if os.path.exists(image_path + "OMG.mp3"):
                omg_sound = pygame.mixer.Sound(image_path + "OMG.mp3")
                omg_sound.play()
            print("Кошко-девочка от вас ушла...")
            print()
            time.sleep(5)
            pygame.mixer.music.stop()
        else:
            print("Вы не можете начать по какой-то причине...")

    elif nochoice == "7":
        if os.path.exists(image_path + "MIKE_the_BOARD_please!.mp3"):
            pygame.mixer.music.load(image_path + "MIKE_the_BOARD_please!.mp3")
            pygame.mixer.music.play()
            print()
            print("Вы начали ЧАС ТВ для Доходяги!!!")
            time.sleep(4.5)
            print("Если сможете помочь Доходяге ответить на все вопросы верно, то будет что-то интересное!")
            time.sleep(4)
            if os.path.exists(image_path + "ITSTVTIME.mp3"):
                pygame.mixer.music.load(image_path + "ITSTVTIME.mp3")
                pygame.mixer.music.play()
                time.sleep(7)
                pygame.mixer.music.stop()
                if os.path.exists(image_path + "Metaphysical_Challenge.mp3"):
                    pygame.mixer.music.load(image_path + "Metaphysical_Challenge.mp3")
                    pygame.mixer.music.play(-1)
                    print("Первый вопрос: ", end="", flush=True); time.sleep(1); print("Кто такой МАЙК?")
                    time.sleep(1)
                    print("1. Кошка" )
                    time.sleep(1)
                    print("2. Микрофон")
                    time.sleep(1)
                    print("3. МАЙК это МАЙК!!!")
                    time.sleep(1)
                    vopros = int(input("Ответ: "))
                    if vopros == 1:
                        print("Кошка Майк - это же Гастер")
                    else:
                        print("Ответ на вопрос принят")
                    time.sleep(3)
                    print("Второй вопрос: ", end="", flush=True); time.sleep(1);print("Любимый персонаж Азриеля в Super Smashing Fighters?")
                    time.sleep(1)
                    print("1. Плюшевый Ральзей с Фангеймер.ком за 32 доллара" )
                    time.sleep(1)
                    print("2. Мечник-маг")
                    time.sleep(1)
                    print("3. Друг")
                    time.sleep(1)
                    vopros2 = int(input("Ответ: "))
                    if vopros2 == 1:
                        print("Он такой няшка, а Крис его толкнул")
                    elif vopros2 == 3:
                        print("ТЕННА, ДРУГ ЗА НАМИ ПРИШЕЛ!!!")
                    elif vopros2 == 2:
                        print("ПРАВИЛЬНЫЙ ОТВЕТ!!!")
                    time.sleep(3)
                    print("Третий вопрос: ", end="", flush=True); time.sleep(1);print("Кто такой Гастер?")
                    time.sleep(1)
                    print("1. Кто это вообще?" )
                    time.sleep(1)
                    print("2. Королевский ученый который упал в свое творенье")
                    time.sleep(1)
                    print("3. Зеленый пират")
                    time.sleep(1)
                    vopros3 = int(input("Ответ: "))
                    if vopros3 == 666:
                        pygame.mixer.music.stop()
                        if os.path.exists(image_path + "GasterTheme.mp3"):
                            pygame.mixer.music.load(image_path + "GasterTheme.mp3")
                            pygame.mixer.music.play()
                            time.sleep(45)
                    elif vopros3 == 3:
                        pygame.mixer.music.stop()
                        if os.path.exists(image_path + "PiratGaster.mp3"):
                            pygame.mixer.music.load(image_path + "PiratGaster.mp3")
                            pygame.mixer.music.play()
                            time.sleep(26)
                    vopros = 0
                    vopros2 = 0
                    vopros3 = 0

                    if os.path.exists(image_path + "And_Now_For_Todays_Sponsors!.mp3"):
                        pygame.mixer.music.load(image_path + "And_Now_For_Todays_Sponsors!.mp3")
                        pygame.mixer.music.play(-1)
                    print("Ты прошел викторину!!!") 
                    print("И твоя награда это...", end="", flush=True); time.sleep(3);print("ПОСЕЩЕНИЕ ГАСТЕРА!!!")
                    time.sleep(4)
                    pygame.mixer.music.stop()
                    print("Как я его к тебе приведу?", end="", flush=True); time.sleep(4);print(" Хороший вопрос...")
                    time.sleep(6)
                    print("*Тенна удалился и не вернулся*")
                    print()
                    time.sleep(2)
        else:
            print()
            print("But nobody came...")
            print()
    elif nochoice == "10":
        image = pygame.image.load(image_path + "Ralsei_call.jpg")
        img_width = image.get_width()
        img_height = image.get_height()
        print()
        print("Вы добавили Ральзея в контакты")
        if os.path.exists(image_path + "Weird_Sound.mp3"):
            pygame.mixer.music.load(image_path + "Weird_Sound.mp3")
            pygame.mixer.music.play()
        time.sleep(3)
        window = pygame.display.set_mode((img_width, img_height), pygame.NOFRAME)
        window.blit(image, (0, 0))
        pygame.display.flip()
        pygame.mixer.music.load(image_path + "The_Third_Sanctuary.mp3")
        pygame.mixer.music.play()
        time.sleep(17)
        pygame.mixer.music.stop()
        pygame.display.quit()
        pygame.display.init()
        print("* Вы подняли трубку")
        time.sleep(2)
        print("* Ральзей начал петь колыбельную Доходяге")
        pygame.mixer.music.load(image_path + "ralsei-lullaby.mp3")
        pygame.mixer.music.play()
        time.sleep(8)
        print("* Доходяга уснул и вы сбросили трубку")
        print()
        time.sleep(4)
    elif nochoice == "11":
        if lomka < 6:
            pygame.mixer.music.load(image_path + "Festival.mp3")
            pygame.mixer.music.play(-1)
        elif lomka >= 6 and breakingg >= 6:
            pygame.mixer.music.load(image_path + "Happy_town.ogg")
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.load(image_path + "Festival.mp3")
            pygame.mixer.music.play(-1)
        print()
        print("Вы пошли на фестиваль")
        print()
        Festival()
    elif nochoice == 666:
        print()
        print("* Вы обратились к Гастеру за помощью")
        print()
        time.sleep(3)
    else:
        print()
        lomka += 1
        if lomka == 6:
            pygame.mixer.music.load(image_path + "Weird_Sound.mp3")
            pygame.mixer.music.play()
            time.sleep(4)
        else:
            print("Такой команды нет, обратитесь к Гастеру за помощью. Пожалуйста, выберите от 1 до 11.")
        print()