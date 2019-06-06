from shapely.geometry.polygon import Polygon


# ####################
# TRACK BORDER 1
# ####################
line00_bis = [(100, 100), (247, 99)]

line00 = [(100, 100), (118, 240)]
line01 = [(118, 240), (239, 336)]
line02 = [(239, 336), (405, 350)]
line03 = [(405, 350), (534, 287)]
line04 = [(534, 287), (568, 299)]
line05 = [(568, 299), (584, 439)]
line06 = [(584, 439), (485, 503)]
line07 = [(485, 503), (268, 468)]
line08 = [(268, 468), (63, 520)]
line09 = [(63, 520), (90, 637)]
line10 = [(90, 637), (237, 698)]
line11 = [(237, 698), (488, 726)]
line12 = [(488, 726), (675, 709)]
line13 = [(675, 709), (766, 611)]
# ####################
# TRACK BORDER 2
# ####################
line14 = [(247, 99), (249, 224)]
line15 = [(249, 224), (401, 243)]
line16 = [(401, 243), (515, 176)]
line17 = [(515, 176), (675, 157)]
line18 = [(675, 157), (736, 240)]
line19 = [(736, 240), (758, 359)]
line20 = [(758, 359), (746, 461)]
line21 = [(746, 461), (618, 564)]
line22 = [(618, 564), (444, 595)]
line23 = [(444, 595), (394, 572)]
line24 = [(394, 572), (213, 571)]
line25 = [(213, 571), (221, 590)]
line26 = [(221, 590), (312, 630)]
line27 = [(312, 630), (487, 644)]
line28 = [(487, 644), (645, 581)]
line29 = [(645, 581), (700, 517)]

# ########################################
# Lines for fitness zones
# ########################################

# line30 = [(565, 323), (749, 262)]
# line31 = [(562, 316), (736, 224)]
# line30 = [(565, 314), (737, 224)]

line30_2 = [(88, 77), (260, 81)]
line30 = [(92, 113), (260, 115)]
line31 = [(260, 146), (97, 180)]
line32 = [(107, 234), (254, 186)]
line33 = [(261, 216), (167, 289)]
line34 = [(207, 319), (277, 224)]
line35 = [(298, 226), (273, 349)]
line36 = [(336, 351), (347, 227)]
line37 = [(391, 235), (388, 358)]
line38 = [(432, 344), (414, 224)]
line39 = [(451, 199), (489, 321)]
line40 = [(517, 306), (504, 167)]
line41 = [(571, 162), (542, 298)]
line42 = [(563, 312), (702, 171)]
line43 = [(736, 224), (563, 315)]
line44 = [(565, 326), (755, 298)]
line45 = [(764, 354), (567, 357)]
line46 = [(571, 390), (762, 414)]
line47 = [(756, 454), (568, 407)]
line48 = [(567, 423), (695, 506)]
line49 = [(663, 532), (554, 445)]
line50 = [(524, 465), (587, 585)]
line51 = [(506, 598), (480, 483)]
line52 = [(444, 479), (417, 589)]
line53 = [(351, 583), (367, 472)]
line54 = [(297, 458), (301, 578)]
line55 = [(259, 579), (228, 469)]
line56 = [(187, 473), (240, 580)]
line57 = [(232, 577), (92, 504)]
line58 = [(63, 555), (223, 582)]
line59 = [(229, 587), (137, 664)]
line60 = [(190, 688), (255, 598)]
line61 = [(292, 614), (277, 711)]
line62 = [(370, 722), (382, 627)]
line63 = [(465, 635), (460, 731)]
line64 = [(544, 731), (523, 623)]
line65 = [(585, 594), (622, 721)]
line66 = [(687, 707), (638, 572)]
line67 = [(674, 533), (753, 644)]
line68 = [(783, 609), (704, 503)]


def get_track():
    all_border_lines = [
        line00_bis,
        line00, line01, line02, line03, line04, line05, line06, line07, line08, line09,
        line10, line11, line12, line13, line14, line15, line16, line17, line18, line19,
        line20, line21, line22, line23, line24, line25, line26, line27, line28, line29,
    ]

    # all_border_lines.extend([
    #     line30,
    #     line31,
    #     line32,
    #     line33,
    #     line34,
    #     line35,
    #     line36,
    #     line37,
    #     line38,
    #     line39,
    #     line40,
    #     line41,
    #     line42,
    #     line43,
    #     line43_bis,
    #     line44,
    #     line45,
    #     line46,
    #     line47,
    #     line48,
    #     line49,
    #     line50,
    #     line51,
    #     line52,
    #     line53,
    #     line54,
    #     line55,
    #     line56,
    #     line57,
    #     line58,
    #     line59,
    #     line60,
    #     line61,
    #     line62,
    #     line63,
    #     line64,
    #     line65,
    #     line66,
    #     line67,
    #     line68,
    # ])
    return all_border_lines


def get_zones():
    zones = [
        [line30_2[0], line30_2[1], line30[0], line30[1]],
        [line30[0], line30[1], line31[0], line31[1]],
        [line31[0], line31[1], line32[0], line32[1]],
        [line32[0], line32[1], line33[0], line33[1]],
        [line33[0], line33[1], line34[0], line34[1]],
        [line34[0], line34[1], line35[0], line35[1]],
        [line35[0], line35[1], line36[0], line36[1]],
        [line36[0], line36[1], line37[0], line37[1]],
        [line37[0], line37[1], line38[0], line38[1]],
        [line38[0], line38[1], line39[0], line39[1]],
        [line39[0], line39[1], line40[0], line40[1]],
        [line40[0], line40[1], line41[0], line41[1]],
        [line41[0], line41[1], line42[0], line42[1]],
        [line42[0], line42[1], line43[0], line43[1]],
        [line43[0], line43[1], line44[0], line44[1]],
        [line44[0], line44[1], line45[0], line45[1]],
        [line45[0], line45[1], line46[0], line46[1]],
        [line46[0], line46[1], line47[0], line47[1]],
        [line47[0], line47[1], line48[0], line48[1]],
        [line48[0], line48[1], line49[0], line49[1]],
        [line49[0], line49[1], line50[0], line50[1]],
        [line50[0], line50[1], line51[0], line51[1]],
        [line51[0], line51[1], line52[0], line52[1]],
        [line52[0], line52[1], line53[0], line53[1]],
        [line53[0], line53[1], line54[0], line54[1]],
        [line54[0], line54[1], line55[0], line55[1]],
        [line55[0], line55[1], line56[0], line56[1]],
        [line56[0], line56[1], line57[0], line57[1]],
        [line57[0], line57[1], line58[0], line58[1]],
        [line58[0], line58[1], line59[0], line59[1]],
        [line59[0], line59[1], line60[0], line60[1]],
        [line60[0], line60[1], line61[0], line61[1]],
        [line61[0], line61[1], line62[0], line62[1]],
        [line62[0], line62[1], line63[0], line63[1]],
        [line63[0], line63[1], line64[0], line64[1]],
        [line64[0], line64[1], line65[0], line65[1]],
        [line65[0], line65[1], line66[0], line66[1]],
        [line66[0], line66[1], line67[0], line67[1]],
        [line67[0], line67[1], line68[0], line68[1]],
    ]
    return zones

def get_zones_limits():
    zones_limits = [
        line30_2,
        line30,
        line31,
        line32,
        line33,
        line34,
        line35,
        line36,
        line37,
        line38,
        line39,
        line40,
        line41,
        line42,
        line43,
        line44,
        line45,
        line46,
        line47,
        line48,
        line49,
        line50,
        line51,
        line52,
        line53,
        line54,
        line55,
        line56,
        line57,
        line58,
        line59,
        line60,
        line61,
        line62,
        line63,
        line64,
        line65,
        line66,
        line67,
        line68
    ]
    return zones_limits


def get_polygon_zones():
    zones = get_zones()
    polygons = [Polygon((z[0], z[1], z[2], z[3])) for z in zones]
    return polygons


