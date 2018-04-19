"""quick and dirt grouping."""

PLATFORM_ALIASES = {
    "ARC": ["ARC", "Arcade", "Arcade game", "arcade", "CP System II", "Taito Type X", "Sega Mega-Tech", "Mega-Tech",
            "Sega X Board", "X Board", "Arcade version", "Neo Geo MVS", "Sega NAOMI"],

    # SEGA
    "SG1": ["SG-1000", "SG1"],
    "32X": ["32X", "Sega 32X"],
    "SCD": ["SCD", "Sega CD", "Mega-CD"],
    "SMS": ["Master System", "SMS", "Sega Master System", "Sega Mark III/Master System", "Sega Mark III"],
    "GEN": ["GEN", "Gen", "MD", "MD/Gen", "Mega Drive", "Genesis", "Sega Genesis", "Sega Mega Drive",
            "Mega Drive/Genesis", "Sega Mega Drive/Genesis", "Mega Drive / Genesis", "Mega CD"],
    "GG": ["GG", "Game Gear", "GameGear", "Sega Game Gear"],
    "SAT": ["SAT", "Saturn", "Sega Saturn", "Satakore"],
    "DC": ["DC", "Dreamcast", "Sega Dreamcast", "Sega DC"],


    # NINTENDO
    "NES": ["NES", "Famicom", "Family Computer", "NES/Famicom", "Nintendo/Famicom", "Nintendo Entertainment System",
            "Nintendo Famicom"],
    "FDS": ["FDS", "Famicom Disk System", "Family Computer Disk System"],
    "SNES": ["SNES", "Super Famicom", "Super NES", "SFC", "Super Nintendo", "Super Nintendo Entertainment System"],
    "N64": ["Nintendo 64", "N64", "64DD", "N64DD"],
    "GC": ["GC", "NGC", "GameCube", "Gamecube", "Nintendo GameCube", "GCN", "Nintendo Gamecube"],
    "GB": ["GB", "Game Boy", "Gameboy"],
    "GBC": ["GBC", "Game Boy Color", "Gameboy Color"],
    "GBA": ["GBA", "Game Boy Advance", "Gameboy Advance"],
    "DS": ["DS", "NDS", "Nintendo DS", "Nintendo DSi", "DSiWare"],
    "3DS": ["3DS", "Nintendo 3DS", "3DS Virtual Console", "Nintendo 3DS Virtual Console", "3DS eShop",
            "New Nintendo 3DS", "3DS Ambassador Program", "3D Classics"],
    "WII": ["Wii", "Nintendo Wii", "WiiWare", "Wii Virtual Console", "Virtual Console", "Wii VC"],
    "WII U": ["Wii U", "Wii U eShop", "Nintendo Wii U", "Wii U Virtual Console", "Wii U VC"],
    "NS": ["Nintendo Switch", "Switch"],
    "VB": ["Virtual Boy"],

    # SONY
    "PS": ["PS", "PS1", "PSX", "PSOne", "PlayStation", "Playstation", "Sony PlayStation"],
    "PS2": ["PS2", "PlayStation 2", "Playstation2", "Playstation 2"],
    "PS3": ["PS3", "PlayStation 3", "PlayStation 3 (PSN)", "PSN", "Playstation 3"],
    "PS4": ["PS4", "PlayStation 4", "PlayStation 4 (PSN)", "PlayStation Network", "PlayStation Store", "PSOne Classic",
            "PS2 Classic"],
    "PSP": ["PSP", "PlayStation Portable", "PSP Store", "PlayStation Minis", "PS Minis", "PlayStation Mini",
            "Playstation Portable", "UMD"],
    "PSV": ["PSV", "Vita", "PS Vita", "PSVita", "PlayStation Vita", "VITA"],

    "TVS": ["Apple TV", "Amazon Fire TV", "tvOS"],

    # APPLE
    "APL2": ["Apple", "Apple II", "Apple IIGS", "Apple IIgs", "GS"],
    "MAC": ["Macintosh", "Mac", "MAC", "Classic Mac OS", "Mac OS", "MacOS", "macOS", "OSX", "OS X", "Mac App Store",
            "Mac OS X", "Mac OS 9", "Macintosh Computer"],
    "IOS": ["iPhone", "iPhone OS", "iPhone / iPod Touch", "iPad", "iPod Touch, iPhone", "iPhone", "iOS",
            "Apple App store", "App Store", "iPod", "iPod Touch", "iPod classic", "iOS Devices"],

    # Microsoft/x86 PC
    "PC": ["DOS", "MS-DOS", "PC", "Win", "Windows", "Microsoft Windows", "CD-ROM", "Steam", "GOG",
           "Computer conversions", "Windows 95", "Windows 3", "Windows 3.x", "Windows 8", "Windows 10",
           "Windows Store", "OnLive", "Onlive", "Windows Games on Demand", "WGoD", "WIN", "Windows 9x",
           "GameTap", "Windows Computers", "GFWL"],
    "XONE": ["XONE", "Xbox One"],
    "X360": ["360", "X360", "Xbox 360", "XBLA", "Xbox Live Arcade", "XBLIG"],
    "XBOX": ["Xbox", "Xbox Originals", "Xbox Games Store"],
    "WP": ["Windows Phone", "Windows Phone 7", "Windows Phone 8", "Windows Mobile"],
    "LNX": ["Linux"],
    "PDA": ["Pocket PC"],

    # Android and other generic mobile platforms
    "AND": ["Android", "Google Play", "Android Market", "Kindle Fire", "Amazon App Store", "Nvidia Shield",
            "PlayStation Mobile"],
    "WEB": ["Web", "Flash", "Flash player", "Silverlight", "Browser", "Web browser", "Chrome Web Store"],
    "MOBI": ["Mobile", "Mobile phones", "Mobile phone", "Cell phone", "Mobile Phone", "J2ME", "Java ME",
             "Symbian OS", "N-Gage 2.0", "Series 40", "S40", "Bada OS", "MeeGo", "i-mode", "Yahoo Mobile",
             "EZweb", "Mobile Phones", "NTT DoCoMo", "DoCoMo", "BREW", "SoftBank", "mobile phone", "Mobile Devices"],
    "EREA": ["Nook Color"],
    "POS": ["Palm", "Palm Pre", "Palm OS", "Palm WebOS"],
    "BB": ["BlackBerry", "BlackBerry 10", "BlackBerry PlayBook"],

    "VR": ["HTC Vive"],

    # ATARI
    "AST": ["Atari ST", "ST"],
    "LYN": ["Atari Lynx", "Lynx"],
    "JAG": ["Atari Jaguar", "Atari Jaguar CD", "Jaguar"],
    "2600": ["2600", "Atari 2600", "Atari", "Atari 8-bit", "Atari 8-Bit"],
    "5200": ["5200", "Atari 5200"],
    "7800": ["Atari 7800", "7800"],

    # NEOGEO
    "NG": ["Neo-Geo", "Neo Geo", "Neo Geo AES"],
    "NGP": ["Neo Geo Pocket Color", "Neo-Geo Pocket Color"],
    "NGCD": ["NGCD", "Neo-Geo CD", "Neo Geo CD"],
    "NGX": ["Neo Geo X"],

    # MISC OLD CONSOLES AND HANDHELDS
    "O2": ["Odyssey²", "Odyssey 2", "Magnavox Odyssey²"],
    "3DO": ["3DO", "3DO Interactive Multiplayer"],
    "VEC": ["Vectrex"],
    "CVIS": ["ColecoVision"],
    "GIZ": ["Gizmondo"],
    "WSC": ["Wonderswan", "WonderSwan Color"],
    "GW": ["Game & Watch", "Game %26 Watch"],
    "NGE": ["N-Gage", "Nokia N-Gage"],
    "INT": ["Intellivision", "IntelliVision"],
    "ZOD": ["Zodiac", "Tapwave Zodiac"],
    "ZEE": ["Zeebo"],
    "OUY": ["Ouya", "OUYA"],
    "DBL": ["DigiBlast", "digiBlast"],
    "IQE": ["iQue Player"],

    # OLD COMPUTERS
    "BBC": ["BBC", "BBC Micro", "Acorn Electron", "Electron"],
    "AMI": ["Amiga", "Commodore Amiga", "Commodore plus", "Commodore 16", "AmigaOS", "OCS", "ECS", "Amiga AGA"],
    "CD32": ["Amiga CD32", "Amiga CDTV", "CD32"],
    "V20": ["VIC-20", "Commodore VIC-20"],
    "ARCH": ["Archimedes", "Acorn Archimedes"],
    "CPC": ["Amstrad CPC", "Amstrad", "Amstrad PCW", "CPC"],
    "C64": ["C64", "Commodore 64"],
    "CDI": ["CD-i", "CDi", "Philips CD-i"],
    "HP3": ["HP3000", "HP-3000"],
    "FMT": ["FM Towns", "FM-Towns", "FM-7", "FM7", "FM77AV", "77AV", "Fujitsu FM Towns"],
    "IBM PC": ["IBM PC", "IBM PC compatible"],
    "RISC": ["Risc PC"],
    "NEC": ["NEC PC", "NEC PC88", "PC-88", "PC-98", "NEC PC-9801", "NEC PC-6001", "NEC PC-8801", "NEC PC-8801mkII SR",
            "PC-6601", "PC-8801", "PC-9801", "9801", "PC-FX", "NEC PC-FX", "PC-6001", "PC-8801mkII SR"],
    "MSX": ["MSX", "MSX2"],
    "T16": ["PC Engine", "PCE", "PC Engine/TurboGrafx-16", "TurboGrafx-16", "TG16", "TG-16", "Turbografx-16",
            "SuperGrafx", "PC-Engine"],
    "TCD": ["PC Engine CD-ROM", "PC Engine CD", "TurboGrafx-CD", "PC Engine CD-ROM²", "Super CD-ROM²"],
    "SAM": ["SAM Coupé"],
    "X1": ["Sharp X1", "X1"],
    "X68K": ["Sharp X68000", "X68000"],
    "TRS": ["TRS-80", "TRS-80 CoCo"],
    "ZX": ["ZX Spectrum", "Spectrum", "ZX"],
}
