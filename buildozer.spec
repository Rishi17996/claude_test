[app]
# (str) Title of your application
title = KivyApp

# (str) Package name
package.name = kivyapp

# (str) Package domain (needed for android)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (str) Application versioning (method 1)
version = 0.1

# (int) Android API to use
android.api = 33

# (int) Minimum android API your APK will support
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 24

# (str) Android entry point, default is org.kivy.android.PythonActivity
#android.entrypoint = org.kivy.android.PythonActivity

# (list) Permissions
android.permissions = INTERNET

# (str) Presplash of the application
#presplash.filename = presplash.png

# (list) Source include patterns
source.include_exts = py,png,jpg,kv,atlas

# (str) Application icon
#icon.filename = icon.png


[buildozer]
log_level = 2
warn_on_rootdir = 0
