STORAGE_PARTIALS = "/tmp/gameworm_data_partials"
STORAGE_RAW = "/tmp/gameworm_data_raw"


GENRES = [
    ("All Categories", 0),
    ("Action", 54),
    ("Action >> Arcade", 289),
    ("Action >> Beat-'Em-Up", 318),
    ("Action >> Beat-'Em-Up >> 2D", 160),
    ("Action >> Beat-'Em-Up >> 3D", 216),
    ("Action >> Fighting", 57),
    ("Action >> Fighting >> 2D", 86),
    ("Action >> Fighting >> 3D", 87),
    ("Action >> General", 250),
    ("Action >> Pinball", 114),
    ("Action >> Platformer", 56),
    ("Action >> Platformer >> 2D", 84),
    ("Action >> Platformer >> 3D", 85),
    ("Action >> Rhythm", 63),
    ("Action >> Rhythm >> Dancing", 158),
    ("Action >> Rhythm >> Music", 159),
    ("Action >> Shooter", 55),
    ("Action >> Shooter >> First-Person", 79),
    ("Action >> Shooter >> First-Person >> Arcade", 152),
    ("Action >> Shooter >> First-Person >> Tactical", 156),
    ("Action >> Shooter >> Light Gun", 239),
    ("Action >> Shooter >> Rail", 81),
    ("Action >> Shooter >> Shoot-'Em-Up", 313),
    ("Action >> Shooter >> Shoot-'Em-Up >> Horizontal", 185),
    ("Action >> Shooter >> Shoot-'Em-Up >> Top-Down", 272),
    ("Action >> Shooter >> Shoot-'Em-Up >> Vertical", 83),
    ("Action >> Shooter >> Third-Person", 80),
    ("Action >> Shooter >> Third-Person >> Arcade", 182),
    ("Action >> Shooter >> Third-Person >> Tactical", 187),
    ("Action Adventure", 163),
    ("Action Adventure >> General", 290),
    ("Action Adventure >> Linear", 293),
    ("Action Adventure >> Open-World", 292),
    ("Action Adventure >> Sandbox", 291),
    ("Action Adventure >> Survival", 164),
    ("Adventure", 50),
    ("Adventure >> 3D", 77),
    ("Adventure >> 3D >> First-Person", 190),
    ("Adventure >> 3D >> Third-Person", 192),
    ("Adventure >> General", 251),
    ("Adventure >> Point-and-Click", 295),
    ("Adventure >> Text", 262),
    ("Adventure >> Visual Novel", 294),
    ("Miscellaneous", 49),
    ("Miscellaneous >> Application", 277),
    ("Miscellaneous >> Board / Card Game", 227),
    ("Miscellaneous >> Compilation", 233),
    ("Miscellaneous >> Demo Disc", 280),
    ("Miscellaneous >> Edutainment", 275),
    ("Miscellaneous >> Exercise / Fitness", 287),
    ("Miscellaneous >> Gambling", 113),
    ("Miscellaneous >> General", 256),
    ("Miscellaneous >> Party / Minigame", 181),
    ("Miscellaneous >> Trivia / Game Show", 224),
    ("Puzzle", 173),
    ("Puzzle >> Action", 282),
    ("Puzzle >> General", 281),
    ("Puzzle >> Hidden Object", 286),
    ("Puzzle >> Logic", 285),
    ("Puzzle >> Matching", 283),
    ("Puzzle >> Stacking", 284),
    ("Racing", 47),
    ("Racing >> Arcade", 314),
    ("Racing >> Arcade >> Automobile", 232),
    ("Racing >> Arcade >> Futuristic", 139),
    ("Racing >> Arcade >> Other", 235),
    ("Racing >> General", 252),
    ("Racing >> Simulation", 315),
    ("Racing >> Simulation >> Automobile", 138),
    ("Racing >> Simulation >> Other", 274),
    ("Role-Playing", 48),
    ("Role-Playing >> Action RPG", 73),
    ("Role-Playing >> General", 257),
    ("Role-Playing >> Japanese-Style", 71),
    ("Role-Playing >> Massively Multiplayer", 75),
    ("Role-Playing >> Roguelike", 296),
    ("Role-Playing >> Trainer", 297),
    ("Role-Playing >> Western-Style", 72),
    ("Simulation", 46),
    ("Simulation >> Flight", 68),
    ("Simulation >> Flight >> Civilian", 157),
    ("Simulation >> Flight >> Combat", 130),
    ("Simulation >> General", 255),
    ("Simulation >> Marine", 317),
    ("Simulation >> Marine >> Civilian", 126),
    ("Simulation >> Marine >> Combat", 125),
    ("Simulation >> Space", 69),
    ("Simulation >> Space >> Civilian", 133),
    ("Simulation >> Space >> Combat", 132),
    ("Simulation >> Vehicle", 316),
    ("Simulation >> Vehicle >> Civilian", 298),
    ("Simulation >> Vehicle >> Combat", 124),
    ("Simulation >> Vehicle >> Train", 259),
    ("Simulation >> Virtual", 311),
    ("Simulation >> Virtual >> Career", 300),
    ("Simulation >> Virtual >> Pet", 299),
    ("Simulation >> Virtual >> Virtual Life", 242),
    ("Sports", 43),
    ("Sports >> General", 254),
    ("Sports >> Individual", 92),
    ("Sports >> Individual >> Athletics", 231),
    ("Sports >> Individual >> Biking", 103),
    ("Sports >> Individual >> Billiards", 112),
    ("Sports >> Individual >> Bowling", 243),
    ("Sports >> Individual >> Combat", 312),
    ("Sports >> Individual >> Combat >> Boxing / Martial Arts", 104),
    ("Sports >> Individual >> Combat >> Wrestling", 93),
    ("Sports >> Individual >> Golf", 98),
    ("Sports >> Individual >> Golf >> Arcade", 206),
    ("Sports >> Individual >> Golf >> Sim", 207),
    ("Sports >> Individual >> Horse Racing", 278),
    ("Sports >> Individual >> Nature", 108),
    ("Sports >> Individual >> Nature >> Fishing", 109),
    ("Sports >> Individual >> Nature >> Hunting", 110),
    ("Sports >> Individual >> Other", 246),
    ("Sports >> Individual >> Skate / Skateboard", 102),
    ("Sports >> Individual >> Ski / Snowboard", 273),
    ("Sports >> Individual >> Surf / Wakeboard", 238),
    ("Sports >> Individual >> Tennis", 101),
    ("Sports >> Team", 91),
    ("Sports >> Team >> Baseball", 94),
    ("Sports >> Team >> Baseball >> Arcade", 200),
    ("Sports >> Team >> Baseball >> Sim", 201),
    ("Sports >> Team >> Basketball", 95),
    ("Sports >> Team >> Basketball >> Arcade", 202),
    ("Sports >> Team >> Basketball >> Sim", 203),
    ("Sports >> Team >> Cricket", 258),
    ("Sports >> Team >> Football", 97),
    ("Sports >> Team >> Football >> Arcade", 204),
    ("Sports >> Team >> Football >> Sim", 205),
    ("Sports >> Team >> Futuristic", 107),
    ("Sports >> Team >> Ice Hockey", 99),
    ("Sports >> Team >> Ice Hockey >> Arcade", 208),
    ("Sports >> Team >> Ice Hockey >> Sim", 209),
    ("Sports >> Team >> Other", 310),
    ("Sports >> Team >> Rugby", 244),
    ("Sports >> Team >> Soccer", 100),
    ("Sports >> Team >> Soccer >> Arcade", 210),
    ("Sports >> Team >> Soccer >> Management", 212),
    ("Sports >> Team >> Soccer >> Sim", 211),
    ("Sports >> Team >> Volleyball", 105),
    ("Strategy", 45),
    ("Strategy >> General", 253),
    ("Strategy >> Management", 60),
    ("Strategy >> Management >> Business / Tycoon", 220),
    ("Strategy >> Management >> Government", 123),
    ("Strategy >> Real-Time", 58),
    ("Strategy >> Real-Time >> Command", 302),
    ("Strategy >> Real-Time >> Defense", 303),
    ("Strategy >> Real-Time >> General", 301),
    ("Strategy >> Real-Time >> MOBA", 288),
    ("Strategy >> Real-Time >> Tactics", 304),
    ("Strategy >> Turn-Based", 59),
    ("Strategy >> Turn-Based >> 4X", 306),
    ("Strategy >> Turn-Based >> Artillery", 307),
    ("Strategy >> Turn-Based >> Card Battle", 240),
    ("Strategy >> Turn-Based >> General", 305),
    ("Strategy >> Turn-Based >> Tactics", 308)]


GENRES_AS_TREE = {
    # Created using genres_as_tree

    "Action": {
        "code": 54,
        "sub": {
            "Arcade": {
                "code": 289,
            },
            "Beat-'Em-Up": {
                "code": 318,
                "sub": {
                    "2D": {
                        "code": 160,
                    },
                    "3D": {
                        "code": 216,
                    }
                }
            },
            "Fighting": {
                "code": 57,
                "sub": {
                    "2D": {
                        "code": 86,
                    },
                    "3D": {
                        "code": 87,
                    }
                }
            },
            "General": {
                "code": 250,
            },
            "Pinball": {
                "code": 114,
            },
            "Platformer": {
                "code": 56,
                "sub": {
                    "2D": {
                        "code": 84,
                    },
                    "3D": {
                        "code": 85,
                    }
                }
            },
            "Rhythm": {
                "code": 63,
                "sub": {
                    "Dancing": {
                        "code": 158,
                    },
                    "Music": {
                        "code": 159,
                    }
                }
            },
            "Shooter": {
                "code": 55,
                "sub": {
                    "First-Person": {
                        "code": 79,
                        "sub": {
                            "Arcade": {
                                "code": 152,
                            },
                            "Tactical": {
                                "code": 156,
                            }
                        }
                    },
                    "Light Gun": {
                        "code": 239,
                    },
                    "Rail": {
                        "code": 81,
                    },
                    "Shoot-'Em-Up": {
                        "code": 313,
                        "sub": {
                            "Horizontal": {
                                "code": 185,
                            },
                            "Top-Down": {
                                "code": 272,
                            },
                            "Vertical": {
                                "code": 83,
                            }
                        }
                    },
                    "Third-Person": {
                        "code": 80,
                        "sub": {
                            "Arcade": {
                                "code": 182,
                            },
                            "Tactical": {
                                "code": 187,
                            }
                        }
                    }
                }
            }
        }
    },
    "Action Adventure": {
        "code": 163,
        "sub": {
            "General": {
                "code": 290,
            },
            "Linear": {
                "code": 293,
            },
            "Open-World": {
                "code": 292,
            },
            "Sandbox": {
                "code": 291,
            },
            "Survival": {
                "code": 164,
            }
        }
    },
    "Adventure": {
        "code": 50,
        "sub": {
            "3D": {
                "code": 77,
                "sub": {
                    "First-Person": {
                        "code": 190,
                    },
                    "Third-Person": {
                        "code": 192,
                    }
                }
            },
            "General": {
                "code": 251,
            },
            "Point-and-Click": {
                "code": 295,
            },
            "Text": {
                "code": 262,
            },
            "Visual Novel": {
                "code": 294,
            }
        }
    },
    "All Categories": {
        "code": 0,
    },
    "Miscellaneous": {
        "code": 49,
        "sub": {
            "Application": {
                "code": 277,
            },
            "Board / Card Game": {
                "code": 227,
            },
            "Compilation": {
                "code": 233,
            },
            "Demo Disc": {
                "code": 280,
            },
            "Edutainment": {
                "code": 275,
            },
            "Exercise / Fitness": {
                "code": 287,
            },
            "Gambling": {
                "code": 113,
            },
            "General": {
                "code": 256,
            },
            "Party / Minigame": {
                "code": 181,
            },
            "Trivia / Game Show": {
                "code": 224,
            }
        }
    },
    "Puzzle": {
        "code": 173,
        "sub": {
            "Action": {
                "code": 282,
            },
            "General": {
                "code": 281,
            },
            "Hidden Object": {
                "code": 286,
            },
            "Logic": {
                "code": 285,
            },
            "Matching": {
                "code": 283,
            },
            "Stacking": {
                "code": 284,
            }
        }
    },
    "Racing": {
        "code": 47,
        "sub": {
            "Arcade": {
                "code": 314,
                "sub": {
                    "Automobile": {
                        "code": 232,
                    },
                    "Futuristic": {
                        "code": 139,
                    },
                    "Other": {
                        "code": 235,
                    }
                }
            },
            "General": {
                "code": 252,
            },
            "Simulation": {
                "code": 315,
                "sub": {
                    "Automobile": {
                        "code": 138,
                    },
                    "Other": {
                        "code": 274,
                    }
                }
            }
        }
    },
    "Role-Playing": {
        "code": 48,
        "sub": {
            "Action RPG": {
                "code": 73,
            },
            "General": {
                "code": 257,
            },
            "Japanese-Style": {
                "code": 71,
            },
            "Massively Multiplayer": {
                "code": 75,
            },
            "Roguelike": {
                "code": 296,
            },
            "Trainer": {
                "code": 297,
            },
            "Western-Style": {
                "code": 72,
            }
        }
    },
    "Simulation": {
        "code": 46,
        "sub": {
            "Flight": {
                "code": 68,
                "sub": {
                    "Civilian": {
                        "code": 157,
                    },
                    "Combat": {
                        "code": 130,
                    }
                }
            },
            "General": {
                "code": 255,
            },
            "Marine": {
                "code": 317,
                "sub": {
                    "Civilian": {
                        "code": 126,
                    },
                    "Combat": {
                        "code": 125,
                    }
                }
            },
            "Space": {
                "code": 69,
                "sub": {
                    "Civilian": {
                        "code": 133,
                    },
                    "Combat": {
                        "code": 132,
                    }
                }
            },
            "Vehicle": {
                "code": 316,
                "sub": {
                    "Civilian": {
                        "code": 298,
                    },
                    "Combat": {
                        "code": 124,
                    },
                    "Train": {
                        "code": 259,
                    }
                }
            },
            "Virtual": {
                "code": 311,
                "sub": {
                    "Career": {
                        "code": 300,
                    },
                    "Pet": {
                        "code": 299,
                    },
                    "Virtual Life": {
                        "code": 242,
                    }
                }
            }
        }
    },
    "Sports": {
        "code": 43,
        "sub": {
            "General": {
                "code": 254,
            },
            "Individual": {
                "code": 92,
                "sub": {
                    "Athletics": {
                        "code": 231,
                    },
                    "Biking": {
                        "code": 103,
                    },
                    "Billiards": {
                        "code": 112,
                    },
                    "Bowling": {
                        "code": 243,
                    },
                    "Combat": {
                        "code": 312,
                        "sub": {
                            "Boxing / Martial Arts": {
                                "code": 104,
                            },
                            "Wrestling": {
                                "code": 93,
                            }
                        }
                    },
                    "Golf": {
                        "code": 98,
                        "sub": {
                            "Arcade": {
                                "code": 206,
                            },
                            "Sim": {
                                "code": 207,
                            }
                        }
                    },
                    "Horse Racing": {
                        "code": 278,
                    },
                    "Nature": {
                        "code": 108,
                        "sub": {
                            "Fishing": {
                                "code": 109,
                            },
                            "Hunting": {
                                "code": 110,
                            }
                        }
                    },
                    "Other": {
                        "code": 246,
                    },
                    "Skate / Skateboard": {
                        "code": 102,
                    },
                    "Ski / Snowboard": {
                        "code": 273,
                    },
                    "Surf / Wakeboard": {
                        "code": 238,
                    },
                    "Tennis": {
                        "code": 101,
                    }
                }
            },
            "Team": {
                "code": 91,
                "sub": {
                    "Baseball": {
                        "code": 94,
                        "sub": {
                            "Arcade": {
                                "code": 200,
                            },
                            "Sim": {
                                "code": 201,
                            }
                        }
                    },
                    "Basketball": {
                        "code": 95,
                        "sub": {
                            "Arcade": {
                                "code": 202,
                            },
                            "Sim": {
                                "code": 203,
                            }
                        }
                    },
                    "Cricket": {
                        "code": 258,
                    },
                    "Football": {
                        "code": 97,
                        "sub": {
                            "Arcade": {
                                "code": 204,
                            },
                            "Sim": {
                                "code": 205,
                            }
                        }
                    },
                    "Futuristic": {
                        "code": 107,
                    },
                    "Ice Hockey": {
                        "code": 99,
                        "sub": {
                            "Arcade": {
                                "code": 208,
                            },
                            "Sim": {
                                "code": 209,
                            }
                        }
                    },
                    "Other": {
                        "code": 310,
                    },
                    "Rugby": {
                        "code": 244,
                    },
                    "Soccer": {
                        "code": 100,
                        "sub": {
                            "Arcade": {
                                "code": 210,
                            },
                            "Management": {
                                "code": 212,
                            },
                            "Sim": {
                                "code": 211,
                            }
                        }
                    },
                    "Volleyball": {
                        "code": 105,
                    }
                }
            }
        }
    },
    "Strategy": {
        "code": 45,
        "sub": {
            "General": {
                "code": 253,
            },
            "Management": {
                "code": 60,
                "sub": {
                    "Business / Tycoon": {
                        "code": 220,
                    },
                    "Government": {
                        "code": 123,
                    }
                }
            },
            "Real-Time": {
                "code": 58,
                "sub": {
                    "Command": {
                        "code": 302,
                    },
                    "Defense": {
                        "code": 303,
                    },
                    "General": {
                        "code": 301,
                    },
                    "MOBA": {
                        "code": 288,
                    },
                    "Tactics": {
                        "code": 304,
                    }
                }
            },
            "Turn-Based": {
                "code": 59,
                "sub": {
                    "4X": {
                        "code": 306,
                    },
                    "Artillery": {
                        "code": 307,
                    },
                    "Card Battle": {
                        "code": 240,
                    },
                    "General": {
                        "code": 305,
                    },
                    "Tactics": {
                        "code": 308,
                    }
                }
            }
        }
    }
}

SYSTEM_SLUG_TRANSLATION = {
    "3do": ("3DO", "3DO"),
    "3ds": ("3DS", "3DS"),
    "arch": ("Acorn Archimedes", ""),
    "avision": ("Adventurevision", ""),
    "firetv": ("Amazon Fire TV", ""),
    "amiga": ("Amiga", "AMI"),
    "cd32": ("Amiga CD32", "CD32"),
    "cpc": ("Amstrad CPC", "CPC"),
    "android": ("Android", "AND"),
    "apf1000": ("APF-*1000/IM", "APF"),
    "appleii": ("Apple II", "APL2"),
    "arcade": ("Arcade Games", "ARC"),
    "a2k1": ("Arcadia 2001", ""),
    "astrocade": ("Astrocade", "AST"),
    "atari2600": ("Atari 2600", "2600"),
    "atari5200": ("Atari 5200", "5400"),
    "atari7800": ("Atari 7800", "7800"),
    "atari8bit": ("Atari 8-bit", "A800"),
    "ast": ("Atari ST", "ST"),
    "pippin": ("Bandai Pippin", "PIP"),
    "bbc": ("BBC Micro", "BBC"),
    "bbs": ("BBS Door", "BBS"),
    "blackberry": ("BlackBerry", "BB"),
    "loopy": ("Casio Loopy", ""),
    "ecv": ("Cassette Vision", "ECV"),
    "cdi": ("CD-I", "CDI"),
    "channelf": ("Channel F", "FAIR"),
    "colecovision": ("Colecovision", "CVIS"),
    "c64": ("Commodore 64", "C64"),
    "pet": ("Commodore PET", ""),
    "cps": ("CPS Changer", ""),
    "cvision": ("CreatiVision", ""),
    "dreamcast": ("Dreamcast", "DC"),
    "ds": ("DS", "DS"),
    "dvd": ("DVD Player", "DVD"),
    "ereader": ("e-Reader", "ERDR"),
    "cg2000": ("EACA Colour Genie 2000", ""),
    "famicomds": ("Famicom Disk System", "FDS"),
    "flash": ("Flash", "FLA"),
    "fmtowns": ("FM Towns", "FMT"),
    "fm7": ("FM-7", "FM7"),
    "gameboy": ("Game Boy", "GB"),
    "gba": ("Game Boy Advance", "GBA"),
    "gbc": ("Game Boy Color", "GBC"),
    "gamecom": ("Game.com", "GCOM"),
    "gamecube": ("GameCube", "GC"),
    "gamegear": ("GameGear", "GG"),
    "genesis": ("Genesis", "GEN"),
    "gizmondo": ("Gizmondo", "GIZ"),
    "gp32": ("GP32", "GP32"),
    "intellivision": ("Intellivision", "INTV"),
    "vc4000": ("Interton VC4000", ""),
    "iphone": ("iOS (iPhone/iPad)", "IOS"),
    "jaguar": ("Jaguar", "JAG"),
    "jaguarcd": ("Jaguar CD", "JCD"),
    "laser": ("LaserActive", ""),
    "unixlinux": ("Linux", "LNX"),
    "lynx": ("Lynx", "LYNX"),
    "mac": ("Macintosh", "MAC"),
    "aquarius": ("Mattel Aquarius", ""),
    "microvision": ("Microvision", ""),
    "mobile": ("Mobile", "MOBI"),
    "msx": ("MSX", "MSX"),
    "ngage": ("N-Gage", "NGE"),
    "pc88": ("NEC PC88", "PC88"),
    "pc98": ("NEC PC98", "PC98"),
    "neogeocd": ("Neo-Geo CD", "NGCD"),
    "neo": ("NeoGeo", "NEO"),
    "ngpc": ("NeoGeo Pocket Color", "NGPC"),
    "nes": ("NES", "NES"),
    "n64": ("Nintendo 64", "N64"),
    "n64dd": ("Nintendo 64DD", ""),
    "switch": ("Nintendo Switch", "NS"),
    "nuon": ("Nuon", "NUON"),
    "odyssey": ("Odyssey", ""),
    "odyssey2": ("Odyssey^2", "O2"),
    "webonly": ("Online/Browser", "WEB"),
    "oric1": ("Oric 1/Atmos", ""),
    "os2": ("OS/2", "OS2"),
    "ouya": ("Ouya", "OUYA"),
    "palmos": ("Palm OS Classic", "POS"),
    "palm-webos": ("Palm webOS", "WOS"),
    "pc": ("PC", "PC"),
    "pcfx": ("PC-FX", "PCFX"),
    "pinball": ("Pinball", ""),
    "playdia": ("Playdia", ""),
    "ps": ("PlayStation", "PS"),
    "ps2": ("PlayStation 2", "PS2"),
    "ps3": ("PlayStation 3", "PS3"),
    "ps4": ("PlayStation 4", "PS4"),
    "vita": ("PlayStation Vita", "VITA"),
    "psp": ("PSP", "PSP"),
    "studio2": ("RCA Studio II", ""),
    "redemption": ("Redemption", ""),
    "saturn": ("Saturn", "SAT"),
    "sega32x": ("Sega 32X", ""),
    "segacd": ("Sega CD", "SCD"),
    "sms": ("Sega Master System", "SMS"),
    "sg1000": ("SG-1000", "SG1"),
    "x1": ("Sharp X1", "X1"),
    "x68000": ("Sharp X68000", "X68"),
    "sinclair": ("Sinclair ZX81/Spectrum", "ZX"),
    "sordm5": ("Sord M5", ""),
    "scv": ("Super Cassette Vision", "SCV"),
    "snes": ("Super Nintendo", "SNES"),
    "svision": ("SuperVision", "SV"),
    "coco": ("Tandy Color Computer", ""),
    "ti99": ("TI-99/4A", "TI"),
    "tutor": ("Tomy Tutor", ""),
    "turbocd": ("Turbo CD", "TCD"),
    "tg16": ("TurboGrafx-16", "TG16"),
    "vectrex": ("Vectrex", ""),
    "vic20": ("VIC-20", ""),
    "virtualboy": ("Virtual Boy", "VBOY"),
    "wii": ("Wii", "WII"),
    "wii-u": ("Wii U", "WIIU"),
    "windows-mobile": ("Windows Mobile", "WINM"),
    "wonderswan": ("WonderSwan", "WS"),
    "wsc": ("WonderSwan Color", "WSC"),
    "xbox": ("Xbox", "XBOX"),
    "xbox360": ("Xbox 360", "X360"),
    "xboxone": ("Xbox One", "XONE"),
    "zeebo": ("Zeebo", ""),
    "zod": ("Zodiac", "ZOD"),
}


def genres_as_tree(node, genres):
    for gen, code in genres:
        if gen not in genres:
            if " >> " in gen:
                spl = gen.split(" >> ", 1)
                genres_as_tree(
                    node[spl[0]]["sub"],
                    [(spl[1], code,)]
                )
            else:
                node.update({gen: {"code": code, "sub": {}}})


def tree_to_json(root):
    import json
    fh = open("genres.tree.json", "w")
    fh.write(json.dumps(root))
    fh.close()


if __name__ == "__main__":
    root = {}
    genres_as_tree(root, GENRES)
    tree_to_json(root)
