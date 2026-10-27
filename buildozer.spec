[app]
title = Lichnii Dohodyaga
package.name = lichdohod
package.domain = org.dohodyaga
source.dir = .
source.include_exts = py,png,jpg,jpeg,mp3,ogg,wav
version = 0.1
requirements = python3==3.10.12,hostpython3==3.10.12,kivy==2.3.0,pyjnius==1.5.0,pygame-ce,cython<3.0
orientation = portrait
fullscreen = 1
android.api = 33
android.minapi = 24
android.ndk = 28c
android.archs = arm64-v8a
android.accept_sdk_license = True
android.build_tools_version = 34.0.0
android.debug_art = 0
p4a.branch = develop

[buildozer]
log_level = 1
warn_on_root = 1
