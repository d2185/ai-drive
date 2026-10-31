#!/usr/bin/env python3
"""Nextcloud's desktop program as «Smarta AI»: our name, icon and server, its own GUIDs (beside a real Nextcloud on
the same computer nothing collides), no updater, one account with virtual files (Windows Cloud Files API).

    brand.py <the program's source>        (github.com/nextcloud/desktop at VERSION, see build.yml)

Each change names the exact text it replaces: a new upstream version that moved it fails here, not in the build.
"""
import pathlib, shutil, sys

NAME, SHORT, EXE, ICON = "Smarta AI", "SmartaAI", "smarta-ai", "SmartaAI"
SERVER = "https://drive.ai.unert.com"

CMAKE = [
    ('set( APPLICATION_NAME       "Nextcloud" )', f'set( APPLICATION_NAME       "{NAME}" )'),
    ('set( APPLICATION_SHORTNAME  "Nextcloud" )', f'set( APPLICATION_SHORTNAME  "{SHORT}" )'),
    ('set( APPLICATION_EXECUTABLE "nextcloud" )', f'set( APPLICATION_EXECUTABLE "{EXE}" )'),
    ('set( APPLICATION_ICON_NAME  "${APPLICATION_SHORTNAME}" )', f'set( APPLICATION_ICON_NAME  "{ICON}" )'),
    ('"nextcloud.com"', '"ai.unert.com"'),
    ('"Nextcloud GmbH"', '"Smarta"'),
    ('set( APPLICATION_SERVER_URL "" CACHE', f'set( APPLICATION_SERVER_URL "{SERVER}" CACHE'),
    ('"com.nextcloud.desktopclient"', '"com.unert.ai.drive"'),
    ('set( APPLICATION_VIRTUALFILE_SUFFIX "nextcloud"', 'set( APPLICATION_VIRTUALFILE_SUFFIX "smarta"'),
    ('option( BUILD_UPDATER "Build updater" ON )', 'option( BUILD_UPDATER "Build updater" OFF )'),
    ('option( WITH_PROVIDERS "Build with providers list" ON )', 'option( WITH_PROVIDERS "Build with providers list" OFF )'),
    ('sync folder when available" OFF )', 'sync folder when available" ON )'),
    ('a single account in desktop client" OFF)', 'a single account in desktop client" ON)'),
    ('"#0082c9"', '"#171717"'),
    ("{BC6988AB-ACE2-4B81-84DC-DC34F9B24401}", "{8AE73118-0D8B-4E73-977A-46B29C7D7717}"),
    ("{E0342B74-7593-4C70-9D61-22F294AAFE05}", "{89B04258-D2BD-4A73-9093-4AB27655033A}"),
    ("{E1094E94-BE93-4EA2-9639-8475C68F3886}", "{339179C3-B303-4AD6-A2E6-B44CE19641C9}"),
    ("{E243AD85-F71B-496B-B17E-B8091CBE93D2}", "{F9D283FF-6FC0-4DD6-9837-2CC6D16A0241}"),
    ("{E3D6DB20-1D83-4829-B5C9-941B31C0C35A}", "{80930D01-E7EC-4585-8DB6-B6F7152CF40D}"),
    ("{E4977F33-F93A-4A0A-9D3C-83DEA0EE8483}", "{2FD3003E-A898-4D13-9858-B8A9247FF0C2}"),
    ("FD2FCCA9-BB8F-4485-8F70-A0621B84A7F4", "F393DA1E-4598-433B-ACCC-31A04FCFA199"),
]
CMAKELISTS = [
    ("{E314A650-DCA4-416E-974E-18EA37C213EA}", "{03CD6587-9968-428F-9C0F-8C40037951C9}"),
    ('"1E62D59A-6EA4-476C-B707-4A32E88ED822"', '"763AB5DD-0EB0-44B5-8785-8EFD1CBBA442"'),
    ('"6FF9B5B6-389F-444A-9FDD-A286C36EA079"', '"ACCFE93D-5C64-4E0B-88A9-A8FEEA2B57FE"'),
    ('set( APPLICATION_URI_HANDLER_SCHEME "nc")', 'set( APPLICATION_URI_HANDLER_SCHEME "smarta-ai")'),
]


def patch(path, changes):
    text = path.read_text()
    for old, new in changes:
        if text.count(old) != 1:
            sys.exit(f"brand.py: {path.name}: «{old}» found {text.count(old)} times, not once")
        text = text.replace(old, new)
    path.write_text(text)


def main(src):
    src = pathlib.Path(src)
    patch(src / "NEXTCLOUD.cmake", CMAKE)
    patch(src / "CMakeLists.txt", CMAKELISTS)
    logo, colored = pathlib.Path(__file__).parent / "theme" / "logo.svg", src / "theme" / "colored"
    for name in (f"{ICON}-icon.svg", f"{ICON}-w10startmenu.svg", "wizard_logo.svg"):
        shutil.copyfile(logo, colored / name)
    # The Start menu tile, named after the program (the build makes its pictures from the w10startmenu icon).
    (src / "theme" / f"{EXE}.VisualElementsManifest.xml").write_text(
        "<Application xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'>\n"
        f'  <VisualElements ForegroundText="light" ShowNameOnSquare150x150Logo="on" BackgroundColor="#171717"\n'
        f'    Square150x150Logo="visualelements\\150-{ICON}-w10startmenu.png"\n'
        f'    Square70x70Logo="visualelements\\70-{ICON}-w10startmenu.png"/>\n</Application>\n')


if __name__ == "__main__":
    main(*sys.argv[1:])
