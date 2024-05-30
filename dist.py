from cx_Freeze import setup, Executable


class AppSettings:
    PYTHON_SCRIPT = './src/exe.py'
    UPDATER_SCRIPT = './src/updater_exe.py'
    PRODUCT_NAME = 'MCPTool'
    PRODUCT_VERSION = '1.0'
    COMPANY_NAME = 'MCPTool'
    PRODUCT_DESCRIPTION = 'A tool for Minecraft pentesting'
    UPGRADE_CODE = '{2d2b8940-8bc9-41e6-b5d4-c4a51174c313}'
    AUTHOR_EMAIL = 'vegapedroagustin2004@gmail.com'
    COPYRIGHT = 'Copyright (C) 2024 cx_Freeze'
    ICON = './img/icon.ico'

# Executable settings
executables = [
    Executable(
        script=AppSettings.PYTHON_SCRIPT,
        base=None,
        target_name='MCPTool.exe',
        icon=AppSettings.ICON,
        copyright=AppSettings.COPYRIGHT,
        shortcut_name=AppSettings.PRODUCT_NAME,
    ),
    Executable(
        script=AppSettings.UPDATER_SCRIPT,
        base=None,
        target_name='MCPToolUpdater.exe',
        icon=AppSettings.ICON,
        copyright=AppSettings.COPYRIGHT,
        shortcut_name='MCPToolUpdater',
    )
]

# Cz_Freeze setup
setup(
    name=AppSettings.PRODUCT_NAME,
    version=AppSettings.PRODUCT_VERSION,
    description=AppSettings.PRODUCT_DESCRIPTION,
    executables=executables,
    options={
        'build_exe': {
            'packages': ['mcptool', 'base64'],
            'includes': ['plyer.platforms.win.notification'],
            'include_files': [],
        },
        'bdist_msi': {
            'upgrade_code': f'{AppSettings.UPGRADE_CODE}',
            'add_to_path': True,
            'all_users': True,
            'initial_target_dir': r'[AppDataFolder]\%s' % AppSettings.COMPANY_NAME,
            'data': {
                'Shortcut': [
                    ('DesktopShortcut', 'DesktopFolder', AppSettings.PRODUCT_NAME, 'TARGETDIR', '[TARGETDIR]MCPTool.exe', None, None, None, None, None, None, 'TARGETDIR'),
                    ("StartMenuShortcut", "StartMenuFolder", AppSettings.PRODUCT_NAME, "TARGETDIR", "[TARGETDIR]MCPTool.exe", None, None, None, None, None, None, "TARGETDIR")
                ],
                "Icon": [
                    ('IconId', AppSettings.ICON),
                ],
            }
        }
    },
    author=AppSettings.COMPANY_NAME,
    author_email=AppSettings.AUTHOR_EMAIL,
)
