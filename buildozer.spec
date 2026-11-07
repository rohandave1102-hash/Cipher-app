[app]
title = CipherApp
package.name = cipherapp
package.domain = org.cipherapp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,so
version = 1.0.0
requirements = python3,kivy

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.allow_backup = True
android.api = 33
android.minapi = 21
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 1
