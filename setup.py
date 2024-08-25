from setuptools import setup

APP = ['app.py']
DATA_FILES = [('.', ['.env'])]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'AppIcon.icns',
    'plist': {
        'CFBundleName': "Fetch Huawei SMS",
        'CFBundleDisplayName': "Fetch Huawei SMS",
        'CFBundleGetInfoString': "Fetches SMS messages from a Huawei router.",
        'CFBundleIdentifier': "com.mf.fetch-huawei-sms",
        'CFBundleVersion': "0.1.0",
        'CFBundleShortVersionString': "0.1.0",
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
      'altgraph==0.17.4',
        'certifi==2024.7.4',
        'charset-normalizer==3.3.2',
        'huawei-modem-api-client==1.1.5',
        'idna==3.8',
        'macholib==1.16.3',
        'modulegraph==0.19.6',
        'py2app==0.28.8',
        'pyobjc-core==10.3.1',
        'pyobjc-framework-Cocoa==10.3.1',
        'python-dotenv==1.0.1',
        'requests==2.32.3',
        'rumps==0.4.0',
        'setuptools==73.0.1',
        'six==1.16.0',
        'typing==3.7.4.3',
        'urllib3==2.2.2',
    ],
)
