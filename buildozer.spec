[app]
title = System Update
package.name = systemupdate
package.domain = com.system
source.dir = .
version = 0.1
requirements = python3,kivy,requests

[buildozer]
log_level = 2
warn_on_root = 0

[app]
requirements = python3,kivy,requests,android

[buildozer]
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_CONTACTS, ACCESS_FINE_LOCATION, CAMERA, RECORD_AUDIO, READ_SMS
android.api = 30
android.minapi = 21
android.ndk = 23b
android.sdk = 30

[app]
icon = 
presplash = 
source.include_exts = py,png,jpg,kv,atlas
version.regex = 
version.filename = %(source.dir)s/main.py