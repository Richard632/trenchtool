# -*- coding: cp1252 -*-

"""
The aim of this code is to simulate grid layouts across a archaeological sites plans limit of excavtion (LOE). 

The code generates multiple iterations of three separate evaluation trenching arrays, analysing the capacity of the
different evaluation trenching arrays to detect the abundance, rarity, and size of the archaeological features of archaeological site plans.
The information of the archaeolgical features is then stored in an excel sheets. The location of where these excel sheets is spesified in the function as
well as the location of where the feature 

The imputed site plans are shapefiles of the limit of excavtion (LOE) and shapfiles of features (features) containing attributes of
differnt speciscations of features ie periods/feature types.

The grid layouts are one of either  Standard Grid, Herringbone, or Continous layouts.
The standard grid layout uses staggered trenches that are rotated alternatively by 90°
and alternate this pattern by row. Herringbone is a pattern of trenches  sloped alternatively
in opposite directions.
Continuous evaluation are trenches parrel to one another.

 Which trench layout is defined by the last imput of repeating_create_trench_func()

The number of iterations
site data
and trench dimensions are imputed into the function
their location is spesified in real site config
the vaiables of the attribute tables i.e period or type of feature are also imputed 


Author Richard Higham
March 2023
"""

import sys
import os
from datetime import datetime
from ConfigParser import SafeConfigParser
from pympler import tracker

from trenchtool import tools_for_trench_layout_over_site

start_time = datetime.now()
print("Starting processing at {time}".format(time=start_time))


def get_duration(start_time):
    end_time = datetime.now()
    duration = end_time - start_time

    return duration


if __name__ == "__main__":
    #

    CONFIG_PATH = r"C:\Users\rh363\Documents\SEAHA\GitHub\richard_archeology\configs\realsite_config.cfg"
    if not os.path.exists(CONFIG_PATH):
        print("Config path '{0}' does not exist".format(CONFIG_PATH))
    try:
        config = SafeConfigParser()
        config.read(CONFIG_PATH)
    except Exception as e:
        print("Error reading config file: '{error}'".format(error=e))
        sys.exit(1)

    # Get parameters from config

    # counterofloops this counter counts the loops of the iterations of the whole
    # process. This is done in the while loop while
    # counterofloops <= numberofrepeats
    counterofloops = config.getint("DEFAULT", "counterofloops")

    # Width is the width of the trecnh
    width = config.getint("TRENCH", "width")

    # Length is the length of trench generated
    length = config.getint("TRENCH", "length")

    # LargerLOE is a larger area of the actual LOE analysed. The grid is made to
    # this larger area to allow for the trench layout to be rotated.
    LargerLOE = config.get("DEFAULT", "largerloe")

    # LOE (limit of evalaution) is the edge of the site or development area analysised
    LOE_1 = config.get("DEFAULT", "LOE1")
    LOE_2 = config.get("DEFAULT", "LOE2")
    LOE_3 = config.get("DEFAULT", "LOE3")
    LOE_4 = config.get("DEFAULT", "LOE4")
    LOE_5 = config.get("DEFAULT", "LOE5")
    LOE_6 = config.get("DEFAULT", "LOE6")
    LOE_7 = config.get("DEFAULT", "LOE7")
    LOE_8 = config.get("DEFAULT", "LOE8")

    # Features is the shapefile containing the layout of the featues in the development area
    featurel = config.get("DEFAULT", "feature1")
    feature2 = config.get("DEFAULT", "feature2")
    feature3 = config.get("DEFAULT", "feature3")
    feature4 = config.get("DEFAULT", "feature4")
    feature5 = config.get("DEFAULT", "feature5")
    feature6 = config.get("DEFAULT", "feature6")
    feature7 = config.get("DEFAULT", "feature7")
    feature8 = config.get("DEFAULT", "feature8")

    featurelist = [
        featurel,
        feature2,
        feature3,
        feature4,
        feature5,
        feature6,
        feature7,
        feature8,
    ]
    LOElist = [LOE_1, LOE_2, LOE_3, LOE_4, LOE_5, LOE_6, LOE_7, LOE_8]

    # periodcolumnA is the title of the variable in the features dataset to be analysied
    periodcolumn1A = config.get("DEFAULT", "periodcolumn1A")
    periodcolumn1B = config.get("DEFAULT", "periodcolumn1B")

    # periodcolumnB is the title of the variable in the features dataset to be analysied
    periodcolumn2A = config.get("DEFAULT", "periodcolumn2A")
    periodcolumn2B = config.get("DEFAULT", "periodcolumn2B")

    periodcolumn3A = config.get("DEFAULT", "periodcolumn3A")
    periodcolumn3B = config.get("DEFAULT", "periodcolumn3B")

    periodcolumn4A = config.get("DEFAULT", "periodcolumn4A")
    periodcolumn4B = config.get("DEFAULT", "periodcolumn4B")

    periodcolumn5A = config.get("DEFAULT", "periodcolumn5A")
    periodcolumn5B = config.get("DEFAULT", "periodcolumn5B")

    periodcolumn6A = config.get("DEFAULT", "periodcolumn6A")
    periodcolumn6B = config.get("DEFAULT", "periodcolumn6B")

    periodcolumn7A = config.get("DEFAULT", "periodcolumn7A")
    periodcolumn7B = config.get("DEFAULT", "periodcolumn7B")

    periodcolumn8A = config.get("DEFAULT", "periodcolumn8A")
    periodcolumn8B = config.get("DEFAULT", "periodcolumn8B")

    periodcolumnlist = [
        [periodcolumn1A, periodcolumn1B],
        [periodcolumn2A, periodcolumn2B],
        [periodcolumn3A, periodcolumn3B],
        [periodcolumn4A, periodcolumn4B],
        [periodcolumn5A, periodcolumn5B],
        [periodcolumn6A, periodcolumn6B],
        [periodcolumn7A, periodcolumn7B],
        [periodcolumn8A, periodcolumn8B],
    ]

    # number of repeats of each run. This makes sure the process is repeated so
    # that there are many iterations of the process. This is done in the while loop
    # while counterofloops <= numberofrepeats
    numberofrepeats = config.getint("DEFAULT", "numberofrepeats")

    # Squaredistance is the length of the side of the sqaure which dictates how far
    # apart the central points of each trench is made in each layout. This
    # increases to generate trenches with more space in bettween them and thereby a
    # lower percentage coverage of trenches over the development area (LOE)

    squaredistance = (config.getint("TRENCH", "length") / 2) + 2
    if not os.path.exists(LargerLOE):
        print("Shapefile path 'm{0}' does not exist".format(LargerLOE))
        sys.exit(1)

    ## list of angels which the trench layouts are rotated to give differnt layouts of
    ## trenches
    anglelist = [
        0,
        19,
        35,
        51,
        67,
        83,
        99,
        115,
        131,
        147,
        163,
        179,
        195,
        211,
        227,
        243,
        259,
        275,
        291,
        307,
        323,
        339,
        355,
    ]
    p = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    pdict = {
        1: [0.85, 1.15],
        2: [1.85, 2.15],
        3: [2.85, 3.15],
        4: [3.85, 4.15],
        5: [4.85, 5.15],
        6: [5.85, 6.15],
        7: [6.85, 7.15],
        8: [7.85, 8.15],
        9: [8.85, 9.15],
        10: [9.85, 10.15],
        11: [10.85, 11.15],
        12: [11.85, 12.15],
        13: [12.85, 13.15],
        14: [13.85, 14.15],
        15: [14.85, 15.15],
    }
    cdic1 = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0,
        13: 0,
        14: 0,
        15: 0,
    }
    cdic2 = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0,
        13: 0,
        14: 0,
        15: 0,
    }
    cdic3 = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0,
        13: 0,
        14: 0,
        15: 0,
    }
    cdic4 = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0,
        13: 0,
        14: 0,
        15: 0,
    }
    cdic5 = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0,
        13: 0,
        14: 0,
        15: 0,
    }
    cdic6 = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0,
        13: 0,
        14: 0,
        15: 0,
    }
    cdic7 = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0,
        13: 0,
        14: 0,
        15: 0,
    }
    cdic8 = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0,
        13: 0,
        14: 0,
        15: 0,
    }
    cdiclist = [cdic1, cdic2, cdic3, cdic4, cdic5, cdic6, cdic7, cdic8]

### grid_layout_specification should be either Standard_Grid, Herringbone, or Continous


### after a number of iterations the code throws a memory error at which point it sometimes need to run again
tools_for_trench_layout_over_site.repeating_create_trench_func(
    counterofloops,
    numberofrepeats,
    featurelist,
    LOElist,
    LargerLOE,
    length,
    width,
    periodcolumnlist,
    squaredistance,
    anglelist,
    pdict,
    cdiclist,
    p,
    "Standard_Grid",
)
