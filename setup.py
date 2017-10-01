"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['RectSky.py']
APP_NAME = "RectSky"
DATA_FILES = ['example_input.json']
OPTIONS = {'argv_emulation': True,
           'iconfile': 'icon.icns',
           'plist': {
                'CFBundleName': APP_NAME,
                'CFBundleDisplayName': APP_NAME,
                'CFBundleGetInfoString': "Transform skyline based on minimal number of horizontal rectangles",
                'CFBundleIdentifier': "com.jmcruz.osx.rectsky",
                'CFBundleVersion': "1.0.0",
                'CFBundleShortVersionString': "1.0.0",
                'NSHumanReadableCopyright': u"Copyright 2017, Juan Cruz, All Rights Reserved"
                }
            }

setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)