[app]

# (str) Title of your application
title = 2048 with Kivy

# (str) Package name
package.name = kivy2048

# (str) Package domain (needed for android/ios packaging)
package.domain = com.meltingrocks

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = libs

# (list) List of exclusions using pattern matching
source.exclude_patterns = README.md,screenshot.png

# (str) Application versioning (method 1)
version.regex = __version__ = '(.*)'
version.filename = %(source.dir)s/main.py

# (str) Application versioning (method 2)
# version = 1.2.0

# (list) Application requirements
requirements = kivy

# (str) Presplash of the application
presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, portrait or all)
orientation = all

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0


#
# Android specific
#

# (list) Permissions
android.permissions = INTERNET

# (int) Android API to use
#android.api = 14

# (int) Minimum API required (8 = Android 2.2 devices)
android.minapi = 10

# (int) Android SDK version to use
#android.sdk = 21

# (str) Android NDK version to use
#android.ndk = 9c

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path = 

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#android.p4a_dir =

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.renpy.android.PythonActivity

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
android.add_jars = libs/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
android.add_src = libs/basegameutils/java/

# (str) python-for-android branch to use, if not master, useful to try
# not yet merged features.
#android.branch = master

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
#android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters = 

# (list) Android additionnal libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
#android.wakelock = False

# (list) Android application meta-data to set (key=value format)
#android.meta_data =
#[app:android.meta_data]
#com.google.android.gms.version = @integer/google_play_services_version

# (list) Android library project to add (will be added in the
# project.properties automatically.)
android.library_references = libs/google-play-services_lib

#
# iOS specific
#

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 1


# -----------------------------------------------------------------------------
# List as sections
# 
# You can define all the "list" as [section:key].
# Each line will be considered as a option to the list.
# Let's take [app] / source.exclude_patterns.
# Instead of doing:
#
#     [app]
#     source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
# This can be translated into:
#
#     [app:source.exclude_patterns]
#     license
#     data/audio/*.wav
#     data/images/original/*
#


# -----------------------------------------------------------------------------
# Profiles
#
# You can extend section / key with a profile
# For example, you want to deploy a demo version of your application without
# HD content. You could first change the title to add "(demo)" in the name
# and extend the excluded directories to remove the HD content.
#
#     [app@demo]
#     title = My Application (demo)
#
#     [app:source.exclude_patterns@demo]
#     images/hd/*
#
# Then, invoke the command line with the "demo" profile:
#
#     buildozer --profile demo android debug

[app:android.meta_data]
com.google.android.gms.version = @integer/google_play_services_version
com.google.android.gms.games.APP_ID = @string/app_id
com.google.android.gms.appstate.APP_ID = @string/app_id
