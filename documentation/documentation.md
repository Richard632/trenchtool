**Requirements**

Python 3

Arcpy

**Inputs**

-   **Specification of trench layout size**

-   **Specification of folders-output and location of data files**

-   **Limit of excavation -LOE (shapefile of the site boundary)**

-   **Features -- shapefiles of features**

-   **Larger LOE -- Shapefile of larger area around LOE (**This area
    larger than LOE is a circular shapefile with a radius the length of
    the distance of the central point to the furthest edge of the site
    area, plus twice the maximum distance between trenches. This
    circular layout larger than the LOE is to allow for rotation and
    movement of the grid after generation giving unique layouts with
    each iteration of the model.)

-   **periodcolumn1A-** this refers to the meta data in the shapefile of
    features that is of interest i.e period or monument type

-   **periodcolumn1B-** this refers to the meta data in the shapefile of
    features that is of interest i.e period or monument type

**Running the Code**

this approach creates multiple trenching layouts and assesses how well
the trenching results reflect the archaeological population within an
area. This approach builds on the work of Hey and Lacey, (2001),
Verhagen and Borsboom, (2009) and Hancea et al (2016). The GIS models
were constructed in Python 2.7 and uses Arcpy. This GIS analysis has
been updated for Python 3 as the earlier software is out of use.

The simulation approach generates multiple iterations of one of three
separate evaluation trenching arrays, either Standard Grid Herringbone
or Continuous layouts (Figure 1).

![Diagram Description automatically
generated](figures/figure1.jpg){width="7.045083114610674in"
height="2.8567475940507436in"}

*Figure 1. Evaluation trench layouts (from left to right): Standard Grid
(2 by 30m trench), Herringbone (2 by 30m trench), Continuous (4m wide
continuous trenches), at 5% coverage.*

The trench area is defined by the width and length input. For Continuous
trenching width is most important with length merely defining the
distance between trenches. Though the model can technically generate
layouts of any imputed trench dimension, The approach tested in this
model are when trenches imputed were 2m wide and 30m long or 4m for
Continuous trenching.

The percentages tested are imputed by the p list as a cdic for each site
imputed which is a dictionary which fills as percentage values are met.

The percentages of the trench coverage tested in this model that were
investigated were 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 and 15%
coverage of the imputed archaeological site area. For this reason, the
Standard Grid trenching layout was unable to be made at percentage
coverage much higher than 15% without being made closer than 1m apart.
Figure 2 demonstrates how close the layout of 15% trenches at 2 by 30 m
would be (the bottom right-hand corner).

The pdict defines the minimum and maximum coverage of percentage
acceptable for each coverage.

*table showing the max and min of the range of trench coverage
simulations for each simulation in the 3^rd^ model*

  ------------ ------- ------ ------ ------ ------ ------ ------ ------ ------ ------- ------- ------- ------- ------- -------
  Percentage   1       2      3      4      5      6      7      8      9      10      11      12      13      14      15
  coverage of                                                                                                          
  site                                                                                                                 

  Range to     1.15    2.15   3.15   4.15   5.15   6.15   7.15   8.15   9.15   10.15   11.15   12.15   13.15   14.15   15.15
  allow for                                                                                                            
  record max                                                                                                           

  Range to     0.8.5   1.85   2.85   3.85   4.85   5.85   6.85   7.85   8.85   9.85    10.85   11.85   12.85   13.85   14.85
  allow for                                                                                                            
  record min                                                                                                           
  ------------ ------- ------ ------ ------ ------ ------ ------ ------ ------ ------- ------- ------- ------- ------- -------

![Calendar Description automatically
generated](figures/figure2.jpg){width="7.903089457567804in"
height="5.411911636045494in"}

*Figure 3. Showing 1 to 15 percent trench coverage of Standard Grid
trenches*

Figure 3 shows a flow chart of the stages of the model.

![Diagram Description automatically
generated](figures/figure3.jpg){width="5.792168635170603in"
height="7.525651793525809in"}

*Figure 6.14. Simplified flow chart of the process of the sampling
model. Shapefiles of features and the LOE along with the percentage
coverage analysed and the number of repeats is imputed. Multiple layouts
of grid are made and then moved and rotated to made unique trenching
layouts over a site which is then sampled, and the periods of the
intersecting features are recorded.*

The first step is a layout of points that are generated across an area
larger than the LOE, using the *arcpy.GenerateTessellation_management*
tool. The maximum distance was calculated by finding what distance
between trenches would generate less than 1% trench coverage of the
site.

Once the points are generated, they act as the central point for each
trench. Figure 4 shows the grid of points across a portion of a site
area.

![A picture containing diagram, text, screenshot, map Description
automatically generated](figures/figure4.jpg){width="5.85in"
height="3.4in"}

*Figure 4. Grid points across an area of Heathrow terminal 5 landscape
at a distance that is soon to make a 5% coverage*

As grid points act as central points for each trench. The minimum
distance of the grid points was specified as half the length of one
trench plus two metres. This makes the minimum distance in the
simulations 1m, between Standard Grid (of trenches 30m by 2m) where
trenches alternate between horizontal and vertical. This is because as
the grid point is the centre of the trench, the boundary of the trench
would be 1m from the vertical trench and half the length of the
horizontal trench leaving 1m metre gap between them.

Once the grid is made, around each grid central point corner coordinates
are added according to the length and width of the trench dimensions.
From these corner coordinates rectangular polygon shapefiles
representing the evaluation trenches are generated. For Standard Grid
horizontal and vertical trenches are generated, while with Herringbone
trenches with alternating symmetry of 135 and 45 degrees are generated,
and Continuous Trenches are generated vertically across the entire site.
Figure 5 shows the Standard Grid Trenching of 5% coverage generated from
the grid points.

![A close-up of a map Description automatically generated with low
confidence](figures/figure5.jpg){width="6.268055555555556in"
height="3.4166666666666665in"}

*Figure 5. Showing Standard Grid layout of 5% across an area of Heathrow
terminal 5 landscape.*

The grid of the shapefiles is then randomly assigned any value in the
range of minus the maximum distance between trenches to the maximum
distance between trenches. This value is either plus or minus in the x
or y value. This moves the trench layout to a unique location, but as
each layout is a repeating grid made over a larger location each part of
the site has an equal chance of being sampled.

The orientation of the grid of trench shapefiles is rotated in angle as
well as position. The angle is randomly selected from an angle list (0,
19, 35, 51, 67, 83, 99, 115, 131, 147, 163, 179, 195, 211, 227, 243,
259, 275, 291, 307, 323, 339, 355); these angles were used as not all
angles worked in the model at higher percentage coverage of trenches due
to the closeness of trenches in the layout some angles caused overlap.
This angle list was worked out through trial and error. With the layout
of trenches positioned and orientated, the trenching layout is then
clipped to the limit of the site and the percentage coverage of the
trenches is calculated. If a layout fits within a range close to a
percentage the sample is recorded.

Once the grid layouts of different percentages are generated the
shapefiles are then clipped to the shapefiles of the features in that
area. The features that intersect with the trench layouts are recorded,
both by number of features and by area. The model records which category
of feature is detected, how many and the area, allowing for assessment
of whether different periods of features and different feature types and
sizes are sampled differently.

The simulations were only able to assess whether layouts of trenching
intersected (i.e. crossed over) archaeological features.

For this reason, in this model of detection, it was assumed that if a
trench intersected with a feature, then it was correctly identified by
the hypothetical excavation team, even if only a small part of the
feature is intersected.

However, it was assumed that with intersection, there is discovery with
period and type of feature identified; in essence it modelled the
best-case scenario of conducting an archaeological evaluation
excavation.

Each iteration of the model is recorded in a excel sheet within a
workbook.At each percentage coverage (1-15%) a record was made of:

> a\) the number of features (shapefiles) detected;
>
> b\) the number of feature intersections (differing from detection as a
> feature could be intersected more than once by different trenches);
>
> c\) area of features intersected by trenches;
>
> d\) number of features detected as a percentage of features on site;
> e) the area of features detected as a percentage of total features on
> site.

The different types of data above were recorded for the total number of
features detected and the different categories of features on site. The
categories are defined by the periodcolumn1A and periodcolumn1B for each
imputed site. This refers to column in the attribute table of features
that you wish to analyse for example feature period or feature type.
Figure 6 shows an example results sheet for column (periodcolumn1A) that
contains 4 periods of features type 1 to 4.

![A screenshot of a computer Description automatically
generated](figures/figure6b.jpg){width="6.216666666666667in"
height="3.1416666666666666in"}

*Figure 6. shows the example of the results*
