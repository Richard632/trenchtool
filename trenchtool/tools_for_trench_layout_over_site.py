# -*- coding: utf-8 -*-
"""
Tools used to perform simulation of shapefile trenches over shapefile of archaeological site and features

Author Richard Higham March 2023
"""

import arcpy
import math
import random
import os
import shutil
import xlwt 
import xlrd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import gc
import subprocess



# this line of code allows arcpy to overwirte files.
arcpy.env.overwriteOutput = 1

def shift_features(in_features, x_shift, y_shift, angle,ox,oy):
        

        """
        Shifts features by rotateing and then by an x and/or y value. The shift values are in
        the units of the in_features coordinate system.
 
        Parameters:
        in_features: string
        An existing feature class or feature layer.  If using a
        feature layer with a selection, only the selected features
        will be modified.
 
        x_shift: float
        The distance the x coordinates will be shifted.
         
        y_shift: float
        The distance the y coordinates will be shifted.


        angle: the amount the cordinates will be rotated

        ox: x cordiante of central point 
        oy: y cordiante of central point 
        """
        r=math.radians(angle)

 
        with arcpy.da.UpdateCursor(in_features, ['SHAPE@XY']) as cursor:
                for row in cursor:
                        cursor.updateRow([[((ox + math.cos(r) * ((row[0][0]+(x_shift or 0))- ox) - math.sin(angle) * ((row[0][1]+(y_shift or 0)) - oy))), 
                                         (oy + math.sin(r) * ((row[0][0]+(x_shift or 0))- ox) + math.cos(angle) * ((row[0][1]+(y_shift or 0)) - oy))]])


                        


              
        return


def creatinggrids(angle,LOE_extent,number,length,width,squaredistance,grid_layout_specification):

        

        """
        This function creates a number of grid layouts of shapefiles in_memory. These shape files are used to represent the trenches of a archaeological
        evaluation. The fucntion also returns the central corrinate of these layouts so that they can be rotated around it later
        

 
        Parameters:
        in_features: string
        An existing feature class or feature layer.  If using a
        feature layer with a selection, only the selected features
        will be modified.
 
        x_shift: float
        The distance the x coordinates will be shifted.
         
        y_shift: float
        The distance the y coordinates will be shifted.


        angle: the amount the cordinates will be rotated

        ox: x cordiante of central point 
        oy: y cordiante of central point 
        
        """

        total_number_of_trenches_list=[]
        
        total_number_of_trenches_list.append(number)    

        ox,oy=create_grid(LOE_extent,number,length,width,grid_layout_specification,squaredistance,angle)
        
        #### A grid of trenches is generated over the layout of the larger LOE. Two
        #trench layouts are generated with different layouts of trenches. At this point the
        #highest coverage of percentage is generated with the distance between points at its lowest.
        #layout 1 is the maximum percantage layout form there the trenches re spaced wider apart

        #The table of the shapefile analysised is converted to an array, which then allows the values to be analysised and manipulated. In this case the sum is calculated.


        ####. The first layout that has its percentage caluclted is the grid layout with the
        #maximum percentage layout.
 
        ####. The folders in which the files used to make the grid percentage are
        #deleted leaving only the final product of the shape file of the gridlayout.

        while squaredistance < 80 :

            print (datetime.datetime.now())
        


            ####.14. The process is repeatted with more spaced out grid layouts made over and over.(the layouts increase in size due to sqaure
            #distance increaseing.Each one is checked until every percentage in cdic includes one value. once this has happend 15 grid layouts of
            # each with a  differnt percentage coverage of the site will have been saved. 

            number=number+1
            total_number_of_trenches_list.append(number)

            squaredistance=squaredistance+1





            ox,oy=create_grid(LOE_extent,number,length,width,grid_layout_specification,squaredistance,angle)

            
            

            
        print ("we've made the treches!")
        return ox,oy,total_number_of_trenches_list
        


    
def comanfordifferntworkbooks(wb,wb1,wb2,feature,featurename,periodcolumn1,periodcolumn2,counterofloops,p,LOEname,LOE,
                               summary_table_path_period,summary_table_path_size,summary_table_path_size_in_period,angle):

        """

        Description: This function performs data analysis and processing across different workbooks, it makes sheets and then fills tham with the data
        that each percentaeg (p) of trenching would identify when the features on site feature is overlapped (clip_features_to_grid_and_write())by the trenching layouts.

        Parameters:
        - wb: Main workbook object (e.g., Excel file) containing data.
        - wb1: Workbook object for intermediate results.
        - wb2: Workbook object for additional intermediate results.
        - feature:  shapefile format.
        - featurename: Name or identifier for the spatial feature.
        - periodcolumn1: Name of the column representing the first period.
        - periodcolumn2: Name of the column representing the second period.
        - counterofloops: A counter indicating the number of loops or iterations.
        - p: An iterable representing percentage
        - LOEname: Name of site (LOE).
        - LOE: Shapefile of site boundary.
        - summary_table_path_period: Path to summary table for a specific period.
        - summary_table_path_size: Path to summary table for feature sizes.
        - summary_table_path_size_in_period: Path to summary table for feature sizes in periods.
        - angle: integer indicating an angle 

        Returns: None

        Note: This function appears to perform various data manipulation tasks such as calculating areas, creating dictionaries, generating sheets in workbooks,
        and performing clipping operations.

        Usage: Making different work books and imputing clipped data .

        """






                        
        
                            

                        add_area_values(LOE)

                        Area_of_total_features=calculate_total_areas(feature,2)

                        Totalnumberoffeatures=count_the_values_in_shapefile(feature)
                        
                        featurelayerdictionary,featuresumarea,featurelayerdictionary_size,featuresumarea_size = create_dict_from_polygontable(feature,periodcolumn1,periodcolumn2)

                        sheetname1_,sheetname2_,sheetname3_=create_sheets_of_period_size_and_periodsize(counterofloops,featurelayerdictionary,featurelayerdictionary_size,p,
                                                                        summary_table_path_period,summary_table_path_size,summary_table_path_size_in_period,LOEname,wb,wb1,wb2)
                        colof1st1 = 1
                        colof2nd1 =1
                        colof3rdsheet1 =2
                        Counter_for_percent_colof1st1 =1
                        Counter_for_percent_colof2nd1 =1
                        Counter_for_percent_colof3rdsheet1 =1



                        #The Counter_for_percent gives the values of the column from which the percentage is calulated

                        for i in (p):
   
                            clip_features="in_memory/finalpercentage_{}__{}".format(LOEname,i)
                            if arcpy.Exists(clip_features):

                                    colof1st1,colof2nd1,colof3rdsheet1,Counter_for_percent_colof1st1,Counter_for_percent_colof2nd1,Counter_for_percent_colof3rdsheet1=clip_features_to_grid_and_write(i,feature,periodcolumn1,periodcolumn2,
                                                                    summary_table_path_period,summary_table_path_size,summary_table_path_size_in_period,
                                                                    colof1st1,colof2nd1,colof3rdsheet1,Counter_for_percent_colof1st1,Counter_for_percent_colof2nd1,Counter_for_percent_colof3rdsheet1,
                                                                    Area_of_total_features,Totalnumberoffeatures,wb,wb1,wb2,featurelayerdictionary,featuresumarea,
                                                                    featurelayerdictionary_size,featuresumarea_size,LOEname,counterofloops,sheetname1_,sheetname2_,sheetname3_,clip_features)
                                    
          
                            else:
                                    print ("not there{}_{}".format(LOEname,i))

                        del featuresumarea
                        del featurelayerdictionary_size
                        del featuresumarea_size
                        del featurelayerdictionary
                                    

                                    


                                    
                               

def clip_features_to_grid_and_write(i,features_,periodcolumn1,periodcolumn2,summary_table_path_period,summary_table_path_size,summary_table_path_size_in_period,
                                    colof1st,colof2nd,colof3rdsheet,Counter_for_percent_colof1st,Counter_for_percent_colof2nd,Counter_for_percent_colof3rdsheet,Area_of_total_features,
                                    Totalnumberoffeatures,wb,wb1,wb2,featurelayerdictionary,featuresumarea,featurelayerdictionary_size,featuresumarea_size,identifier,counterofloops,
                                    sheetname1,sheetname2,sheetname3,clip_features):

                        """
                        This makes the uses select_clip_extract_by_grid() to clip features to trenching layouts and extract dictionaries continaing which
                        featrues are identified. These are then writen into the differnt workbooks either wb wb1 or wb2

                        """
    
                        ###here three different work books are made for whichever site is imputed

                        workbookofdifferntfeatures_period=summary_table_path_period+identifier+".xls"
                        workbookofdifferntfeatures_size=summary_table_path_size+identifier+".xls"
                        workbookofdifferntfeatures_sizeinperiod=summary_table_path_size_in_period+identifier+".xls"

                        
                        ###select clip extract by grid is undertaken where the features are clipped to the trench layouts  the values are placed in dictionaries and written into sheets
 
                        countvaluesdictionary,layerdictionary,sumareadictionary,countvaluesdictionary_size,layerdictionary_size,sumareadictionary_size,countfeaturelayerdictionarysize,sum_featurelayersize,layerdictionary_in_size=select_clip_extract_by_grid(i,features_,periodcolumn1,periodcolumn2,identifier,clip_features)

                        dict_list = ["countvaluesdictionary",
                                 "layerdictionary",
                                 "sumareadictionary",
                                 "percentage_of_values",
                                 "percentage_of_Areas"]
                        dict_list2 = ["countvaluesdictionary_size",
                                 "layerdictionary_size",
                                 "sumareadictionary_size",
                                 "percentage_of_values",
                                 "percentage_of_Areas"]
                        dict_list3 = ["countfeaturelayerdictionarysize",
                                 "layerdictionary_in_size","sum_featurelayersize",
                                 "percentage_of_values",
                                 "percentage_of_Areas"] 

                        ########writing in the values for sheet of periods########################
                        
                        for dic in dict_list:
                            # the from the excel files of the cliped archaeoligcal features the values are countd and placed in the dictionarys of {countvaluesdictionary},{layerdictionary},
                            #,{sumareadictionary} this uses the count_layers_based_on_column_value functions, sum_of_areas_based_on_column_valueand the  which is used within Select_Clip_-
                            #-Extract_By_Random_numbers.
                            #Now that the information is writen into the dictionary's the dictionary information has to be writen into the correct rows in the summary table.
                            write_in_summary_row(dic, colof1st, Counter_for_percent_colof1st,
                                                 sheetname1, featurelayerdictionary,
                                                 featuresumarea,
                                                 countvaluesdictionary,
                                                 layerdictionary,
                                                 sumareadictionary)
                            #The total of each column can be calculated and writen in to the summary sheet now that the select_clip_extract_function has filled the dictionaries
                            write_sum_formula(dic, colof1st, sheetname1,
                                              Totalnumberoffeatures,
                                              Area_of_total_features,
                                              countvaluesdictionary,
                                              layerdictionary,sumareadictionary,featurelayerdictionary)

                            colof1st = colof1st + 1
                            if dic == "percentage_of_values":
                                Counter_for_percent_colof1st = Counter_for_percent_colof1st + 2
                            if dic == "percentage_of_Areas":
                                Counter_for_percent_colof1st = Counter_for_percent_colof1st + 3
                        

                        summarytable=wb.save(workbookofdifferntfeatures_period)
                            
                            


                    #######
                    #SHEET of SIZE The writing of an excel file process is repeated so that a differnt excel sheet containing a differnt varible of data
                    ####################################################################################################################


                        for dic in dict_list2:
                            # the from the excel files of the cliped archaeoligcal features the values are countd and placed in the dictionarys of {countvaluesdictionary},{layerdictionary},
                            #,{sumareadictionary} this uses the count_layers_based_on_column_value functions, sum_of_areas_based_on_column_valueand the  which is used within Select_Clip_-
                            #-Extract_By_Random_numbers.
                            #Now that the information is writen into the dictionary's the dictionary information has to be writen into the correct rows in the summary table.
                            write_in_summary_row(dic, colof2nd, Counter_for_percent_colof2nd,
                                                 sheetname2, featurelayerdictionary_size,
                                                 featuresumarea_size,
                                                 countvaluesdictionary_size,
                                                 layerdictionary_size,sumareadictionary_size)
                            #The total of each column can be calculated and writen in to the summary sheet now that the select_clip_extract_function has filled the dictionaries
                            write_sum_formula(dic, colof2nd, sheetname2,
                                              Totalnumberoffeatures,
                                              Area_of_total_features,
                                              countvaluesdictionary_size,
                                              layerdictionary_size,sumareadictionary_size,featurelayerdictionary_size)


                            colof2nd=colof2nd+1
                            if dic == "percentage_of_values":
                                Counter_for_percent_colof2nd = Counter_for_percent_colof2nd + 2
                            if dic == "percentage_of_Areas":
                                Counter_for_percent_colof2nd = Counter_for_percent_colof2nd + 3

                        summarytablesize=wb1.save(workbookofdifferntfeatures_size)

        


                        for dic in dict_list3:
                                
                            
                            # the from the excel files of the cliped archaeoligcal features the values are countd and placed in the dictionarys of {countvaluesdictionary},{layerdictionary},
                            #,{sumareadictionary} this uses the count_layers_based_on_column_value functions, sum_of_areas_based_on_column_valueand the  which is used within Select_Clip_-
                            #-Extract_By_Random_numbers.
                            #Now that the information is writen into the dictionary's the dictionary information has to be writen into the correct rows in the summary table.

                            write_in_summary_row_for_double_dict(dic,colof3rdsheet,Counter_for_percent_colof3rdsheet,sheetname3,
                                             featurelayerdictionary,featuresumarea,featurelayerdictionary_size,featuresumarea_size,
                                                                 countfeaturelayerdictionarysize,sum_featurelayersize,layerdictionary_in_size,
                                                                 countvaluesdictionary,sumareadictionary)

                            
                            
                            colof3rdsheet= colof3rdsheet + 1
                            if dic == "percentage_of_values":
                                Counter_for_percent_colof3rdsheet = Counter_for_percent_colof3rdsheet + 2
                            if dic == "percentage_of_Areas":
                                Counter_for_percent_colof3rdsheet = Counter_for_percent_colof3rdsheet + 3
                        
                        


                        ####Here all the sheets are saves now that the values have been writen into them


                        
                        summarytable=wb2.save(workbookofdifferntfeatures_sizeinperiod)

                        # Delete dictionaries and lists
                        del countvaluesdictionary
                        del layerdictionary
                        del sumareadictionary
                        del countvaluesdictionary_size
                        del layerdictionary_size
                        del sumareadictionary_size
                        del countfeaturelayerdictionarysize
                        del sum_featurelayersize
                        del layerdictionary_in_size
                        del dict_list
                        del dict_list2
                        del dict_list3


                                                
                        
                        return colof1st,colof2nd,colof3rdsheet,Counter_for_percent_colof1st,Counter_for_percent_colof2nd,Counter_for_percent_colof3rdsheet

                            

def create_sheets_of_period_size_and_periodsize(counterofloops,featurelayerdictionary,featurelayerdictionary_size,p,
                                                summary_table_path_period,summary_table_path_size,summary_table_path_size_in_period,identifier,wb,wb1,wb2):
                """

                Function: create_sheets_of_period_size_and_periodsize

                Description: This function generates sheets in Excel workbooks, each containing specific information related to different analysis aspects such as periods, feature sizes, and percentages. It populates these sheets with headers and values derived from the provided dictionaries and input parameters.

                Parameters:
                - counterofloops: An integer counter indicating the number of loops or iterations.
                - featurelayerdictionary: A dictionary containing spatial feature information.
                - featurelayerdictionary_size: A dictionary containing spatial feature size information.
                - p: An iterable representing specific iterations or percentage values.
                - summary_table_path_period: Path to save the summary table for a specific period.
                - summary_table_path_size: Path to save the summary table for feature sizes.
                - summary_table_path_size_in_period: Path to save the summary table for feature sizes in periods.
                - identifier: An identifier used for naming sheets and summary tables.
                - wb, wb1, wb2: Excel workbook objects where sheets will be created.

                Returns: Names of the created sheets: sheetname1, sheetname2, sheetname3

                Note: This function generates Excel sheets in three separate workbooks. It fills the sheets with various headers, percentages, and information extracted from the dictionaries. The code snippet uses the `xlwt` library to create and save Excel workbooks.

                Usage: Call this function with appropriate parameters to create and populate Excel sheets with relevant information related to analysis aspects, sizes, and percentages.
                """

     
                #################################################################################################################### 
                
                sheetname1="sheet_period_{}_{}".format(counterofloops,identifier)  
                # add_sheet is used to create sheet the name changes with each counter 
                sheetname1 = wb.add_sheet(sheetname1, cell_overwrite_ok=True)

                sheetname2="sheet_size_{}_{}".format(counterofloops,identifier)  
                # add_sheet is used to create sheet the name changes with each counter 
                sheetname2 = wb1.add_sheet(sheetname2, cell_overwrite_ok=True)

                sheetname3="sheet_period_size{}_{}".format(counterofloops,identifier)    
                # add_sheet is used to create sheet the name changes with each counter 
                sheetname3 = wb2.add_sheet(sheetname3, cell_overwrite_ok=True)

                
                #The layout for the summery tables is automated so that the summeray table adapts to the imputs of the features and the perctages analysied. Feature layer dictionary
                #- and p dictate what is writen in the summary table.
                
                write(0,0,sheetname1,"Period of Feature")
                write(0,0,sheetname2,"Type of Feature")
                write(0,0,sheetname3,"Period of Feature")
                b=1
                c=1
                e=1
                
                for key in featurelayerdictionary:     
                    write(b,0,sheetname1,key)
                    b+=1
                    
                    write(c,0,sheetname3,key)
                    
                    for key in featurelayerdictionary_size:   
                        write(c,1,sheetname3,key)
                        c+=1

                for key in featurelayerdictionary_size:
                    write(e,0,sheetname2,key)
                    e+=1
                    
                write(b,0,sheetname1,"Total")
                write(e,0,sheetname2,"Total")
                write(c,0,sheetname3,"Total")
                d=1
                f=2
                
                for i in p:
                    write(0,d,sheetname1,"{}%_Features_detected".format(i))
                    write(0,d,sheetname2,"{}%_Features_detected".format(i))
                    write(0,f,sheetname3,"{}%_Features_detected".format(i))
                    d+=1
                    f+=1
                    write(0,d,sheetname1,"{}%_interections".format(i))
                    write(0,d,sheetname2,"{}%_interections".format(i))
                    write(0,f,sheetname3,"{}%_interections".format(i))
                    d+=1
                    f+=1
                    write(0,d,sheetname1,"{}%_Area_of_Features_found".format(i))
                    write(0,d,sheetname2,"{}%_Area_of_Features_found".format(i))
                    write(0,f,sheetname3,"{}%_Area_of_Features_found".format(i))
                    d+=1
                    f+=1
                    write(0,d,sheetname1,"{}%_as_percentage_of_total_Features".format(i))
                    write(0,d,sheetname2,"{}%_as_percentage_of_total_Features".format(i))
                    write(0,f,sheetname3,"{}%_as_percentage_of_total_Features".format(i))
                    f+=1
                    d+=1
                    write(0,d,sheetname1,"{}%_as_percentage_of_total_area_of_Features".format(i))
                    write(0,d,sheetname2,"{}%_as_percentage_of_total_area_of_Features".format(i))
                    write(0,f,sheetname3,"{}%_as_percentage_of_total_area_of_Features".format(i))
                    f+=1
                    d+=1
  
                workbookofdifferntfeatures_period=summary_table_path_period+identifier+".xls"
                workbookofdifferntfeatures_size=summary_table_path_size+identifier+".xls"
                workbookofdifferntfeatures_sizeinperiod=summary_table_path_size_in_period+identifier+".xls"
                
                summarytableperiod=wb.save(workbookofdifferntfeatures_period)
                summarytablesize=wb1.save(workbookofdifferntfeatures_size) 
                summarytablesizeinperiod=wb2.save(workbookofdifferntfeatures_sizeinperiod)
                
                return sheetname1,sheetname2,sheetname3



def _create_Standard_Grid_trench_shp(shp_id, sorteddf_cordinatesand_hv_vh, yvalueslist,crs_str,dataframe_csv="C:/Users/rh363/Documents/SEAHA/PHD Year 1/PythonLocation/dataframe.csv"):


        
        """
            Creates a polyline shapefile and then converts it into a trench polygon shapefile.

            Args:
                * shp_id (str): ID number for shapefile filename.
                * output_dir (str): Path to directory to write shapefiles to.
                * numberofrows (int): Number of rows in the trench layout.
                * sorteddf_cordinatesand_hv_vh (pandas.DataFrame): A dataframe containing coordinates and values of 'HV' or 'VH' for each point of the grid.
                * yvalueslist (list): A list of Y values for each row in the trench layout.
                * crs_str (str): Coordinate reference system string for the output shapefile.
                * LOE (float): The length of the electrodes (in meters).
                * counterofloops (int): Counter for the number of loops through the while loop.
                * numberofrepeats (int): Number of times the while loop should repeat.
                * maxpercentage (float): Maximum percentage of electrode length for trench width.
                * length (float): Length of the trench (in meters).
                * width (float): Width of the trench (in meters).
                * pdict (dict): A dictionary containing parameters for the 'polyline' shapefile.
                * cdiclist (list): A list of dictionaries containing parameters for the 'trench' shapefile.
                * dataframe_csv (str): Path to CSV file to write master dataframe to.
                * y_listcounter (int): Counter for the number of times the while loop has looped through Y values of trench layout.
                * x_listcounter (int): Counter for the number of times the while loop has looped through X values of trench layout.
            
            Returns:
                * Path to trench shapefile
        """


        xvalueslist=sorteddf_cordinatesand_hv_vh['POINT_X'].unique()

        y_values_even=yvalueslist[::2]
        y_values_odd=yvalueslist[1::2]
        x_values_even=xvalueslist[::2]
        x_values_odd=xvalueslist[1::2]



        #y_even=sorteddf_cordinatesand_hv_vh[sorteddf_cordinatesand_hv_vh['POINT_Y'].isin(y_values_even)]

        chunks = np.array_split(sorteddf_cordinatesand_hv_vh, 10)

        # Loop over the chunks and perform the query on each chunk
        result = []
        for chunk in chunks:
            result.append(chunk.query('POINT_Y in @y_values_even'))

        # Concatenate the results into a single DataFrame
        y_even = pd.concat(result)

        xy_even=y_even.loc[y_even['POINT_X'].isin(x_values_even)].rename(columns={'VC1_Xvalue':'X1', 'VC1_Yvalue': 'Y1' ,'VC2_Xvalue':'X2', 'VC2_Yvalue': 'Y2' ,'VC3_Xvalue':'X3', 'VC3_Yvalue':'Y3', 'VC4_Xvalue': 'X4' ,'VC4_Yvalue': 'Y4'}).drop(['POINT_X','HV_values','VH_values','POINT_Y','HC1_Xvalue', 'HC1_Yvalue','HC2_Xvalue', 'HC2_Yvalue','HC3_Xvalue', 'HC3_Yvalue','HC4_Xvalue', 'HC4_Yvalue'], axis=1)


        xoddy_even=y_even.loc[y_even['POINT_X'].isin(x_values_odd)].rename(columns={'HC1_Xvalue':'X1', 'HC1_Yvalue': 'Y1' ,'HC2_Xvalue':'X2', 'HC2_Yvalue': 'Y2' ,'HC3_Xvalue':'X3', 'HC3_Yvalue':'Y3', 'HC4_Xvalue': 'X4' ,'HC4_Yvalue': 'Y4'}).drop(['POINT_X','HV_values','VH_values','POINT_Y','VC1_Xvalue', 'VC1_Yvalue','VC2_Xvalue', 'VC2_Yvalue','VC3_Xvalue', 'VC3_Yvalue','VC4_Xvalue', 'VC4_Yvalue'], axis=1)
        masterdf=xy_even.append(xoddy_even, ignore_index=True)


        y_odd=sorteddf_cordinatesand_hv_vh[sorteddf_cordinatesand_hv_vh['POINT_Y'].isin(y_values_odd)]

        xevey_odd=y_odd.loc[y_odd['POINT_X'].isin(x_values_even)].rename(columns={'HC1_Xvalue':'X1', 'HC1_Yvalue': 'Y1' ,'HC2_Xvalue':'X2', 'HC2_Yvalue': 'Y2' ,'HC3_Xvalue':'X3', 'HC3_Yvalue':'Y3', 'HC4_Xvalue': 'X4' ,'HC4_Yvalue': 'Y4'}).drop(['POINT_X','HV_values','VH_values','POINT_Y','VC1_Xvalue', 'VC1_Yvalue','VC2_Xvalue', 'VC2_Yvalue','VC3_Xvalue', 'VC3_Yvalue','VC4_Xvalue', 'VC4_Yvalue'], axis=1)
        masterdf=masterdf.append(xevey_odd, ignore_index=True)

        xoddy_odd= y_odd.loc[y_odd['POINT_X'].isin(x_values_odd)].rename(columns={'VC1_Xvalue':'X1', 'VC1_Yvalue': 'Y1' ,'VC2_Xvalue':'X2', 'VC2_Yvalue': 'Y2' ,'VC3_Xvalue':'X3', 'VC3_Yvalue':'Y3', 'VC4_Xvalue': 'X4' ,'VC4_Yvalue': 'Y4'}).drop(['POINT_X','HV_values','VH_values','POINT_Y','HC1_Xvalue', 'HC1_Yvalue','HC2_Xvalue', 'HC2_Yvalue','HC3_Xvalue', 'HC3_Yvalue','HC4_Xvalue', 'HC4_Yvalue'], axis=1)

        masterdf=masterdf.append(xoddy_odd, ignore_index=True)


        masterdf.to_csv(dataframe_csv, index = False)


        del chunks
        del masterdf
        del xvalueslist

        del y_even
        del xy_even  

        del xoddy_even

        del y_odd

        del xevey_odd
        del xoddy_odd

        del sorteddf_cordinatesand_hv_vh


        _xytopolygone(shp_id,dataframe_csv,crs_str)



def _create_herringbone_trench_shp(shp_id, sorteddf_cordinatesand_hv_vh, yvalueslist,
                       crs_str,dataframe_csv="C:/Users/rh363/Documents/SEAHA/PHD Year 1/PythonLocation/dataframe.csv"):


        
        """
            Creates a polyline shapefile and then converts it into a trench polygon shapefile.

            Args:
                * shp_id (str): ID number for shapefile filename.
                * output_dir (str): Path to directory to write shapefiles to.
                * numberofrows (int): Number of rows in the trench layout.
                * sorteddf_cordinatesand_hv_vh (pandas.DataFrame): A dataframe containing coordinates and values of 'HV' or 'VH' for each point of the grid.
                * yvalueslist (list): A list of Y values for each row in the trench layout.
                * crs_str (str): Coordinate reference system string for the output shapefile.
                * LOE (float): The length of the electrodes (in meters).
                * counterofloops (int): Counter for the number of loops through the while loop.
                * numberofrepeats (int): Number of times the while loop should repeat.
                * maxpercentage (float): Maximum percentage of electrode length for trench width.
                * length (float): Length of the trench (in meters).
                * width (float): Width of the trench (in meters).
                * pdict (dict): A dictionary containing parameters for the 'polyline' shapefile.
                * cdiclist (list): A list of dictionaries containing parameters for the 'trench' shapefile.
                * dataframe_csv (str): Path to CSV file to write master dataframe to.
                * y_listcounter (int): Counter for the number of times the while loop has looped through Y values of trench layout.
                * x_listcounter (int): Counter for the number of times the while loop has looped through X values of trench layout.
            
            Returns:
                * Path to trench shapefile
        """


        xvalueslist=sorteddf_cordinatesand_hv_vh['POINT_X'].unique()

        y_values_even=yvalueslist[::2]
        y_values_odd=yvalueslist[1::2]
        x_values_even=xvalueslist[::2]
        x_values_odd=xvalueslist[1::2]

        ##Herringbone has differnt column values to standardgrd

        y_even=sorteddf_cordinatesand_hv_vh[sorteddf_cordinatesand_hv_vh['POINT_Y'].isin(y_values_even)]
                                                                            
        xy_even=y_even.loc[y_even['POINT_X'].isin(x_values_even)].rename(columns={'HC1_Xvalue':'X1', 'HC1_Yvalue': 'Y1' ,'HC2_Xvalue':'X2', 'HC2_Yvalue': 'Y2' ,'HC3_Xvalue':'X3', 'HC3_Yvalue':'Y3', 'HC4_Xvalue': 'X4' ,'HC4_Yvalue': 'Y4'}).drop(['POINT_X','HV_values','VH_values','POINT_Y','VC1_Xvalue', 'VC1_Yvalue','VC2_Xvalue', 'VC2_Yvalue','VC3_Xvalue', 'VC3_Yvalue','VC4_Xvalue', 'VC4_Yvalue' ], axis=1)

        xoddy_even=y_even.loc[y_even['POINT_X'].isin(x_values_odd)].rename(columns={'HC1_Xvalue':'X1', 'HC1_Yvalue': 'Y1' ,'HC2_Xvalue':'X2', 'HC2_Yvalue': 'Y2' ,'HC3_Xvalue':'X3', 'HC3_Yvalue':'Y3', 'HC4_Xvalue': 'X4' ,'HC4_Yvalue': 'Y4'}).drop(['POINT_X','HV_values','VH_values','POINT_Y','VC1_Xvalue', 'VC1_Yvalue','VC2_Xvalue', 'VC2_Yvalue','VC3_Xvalue', 'VC3_Yvalue','VC4_Xvalue', 'VC4_Yvalue'], axis=1)
        masterdf=xy_even.append(xoddy_even, ignore_index=True)


        y_odd=sorteddf_cordinatesand_hv_vh[sorteddf_cordinatesand_hv_vh['POINT_Y'].isin(y_values_odd)]

        xevey_odd=y_odd.loc[y_odd['POINT_X'].isin(x_values_even)].rename(columns={'VC1_Xvalue':'X1', 'VC1_Yvalue': 'Y1' ,'VC2_Xvalue':'X2', 'VC2_Yvalue': 'Y2' ,'VC3_Xvalue':'X3', 'VC3_Yvalue':'Y3', 'VC4_Xvalue': 'X4' ,'VC4_Yvalue': 'Y4'}).drop(['POINT_X','HV_values','VH_values','POINT_Y','HC1_Xvalue', 'HC1_Yvalue','HC2_Xvalue', 'HC2_Yvalue','HC3_Xvalue', 'HC3_Yvalue','HC4_Xvalue', 'HC4_Yvalue'], axis=1)
        masterdf=masterdf.append(xevey_odd, ignore_index=True)

        xoddy_odd= y_odd.loc[y_odd['POINT_X'].isin(x_values_odd)].rename(columns={'VC1_Xvalue':'X1', 'VC1_Yvalue': 'Y1' ,'VC2_Xvalue':'X2', 'VC2_Yvalue': 'Y2' ,'VC3_Xvalue':'X3', 'VC3_Yvalue':'Y3', 'VC4_Xvalue': 'X4' ,'VC4_Yvalue': 'Y4'}).drop(['POINT_X','HV_values','VH_values','POINT_Y','HC1_Xvalue', 'HC1_Yvalue','HC2_Xvalue', 'HC2_Yvalue','HC3_Xvalue', 'HC3_Yvalue','HC4_Xvalue', 'HC4_Yvalue'], axis=1)

        masterdf=masterdf.append(xoddy_odd, ignore_index=True)


        masterdf.to_csv(dataframe_csv, index = False)



        del masterdf
        del xvalueslist

        del y_even
        del xy_even  

        del xoddy_even

        del y_odd

        del xevey_odd
        del xoddy_odd

        del sorteddf_cordinatesand_hv_vh


        _xytopolygone(shp_id,dataframe_csv,crs_str)

def _create_Continous_trench_shp(shp_id, maxandminy_df,crs_str,dataframe_csv="C:/Users/rh363/Documents/SEAHA/PHD Year 1/PythonLocation/dataframe.csv"):
        
        

        
        """
        Creates a polyline shapefile and then converts it into a trench polygon shapefile.

        Args:
        * shp_id (str): ID number for shapefile filename.
        * output_dir (str): Path to directory to write shapefiles to.
        * numberofrows (int): Number of rows in the trench layout.
        * sorteddf_cordinatesand_hv_vh (pandas.DataFrame): A dataframe containing coordinates and values of 'HV' or 'VH' for each point of the grid.
        * yvalueslist (list): A list of Y values for each row in the trench layout.
        * crs_str (str): Coordinate reference system string for the output shapefile.
        * LOE (float): The length of the electrodes (in meters).
        * counterofloops (int): Counter for the number of loops through the while loop.
        * numberofrepeats (int): Number of times the while loop should repeat.
        * maxpercentage (float): Maximum percentage of electrode length for trench width.
        * length (float): Length of the trench (in meters).
        * width (float): Width of the trench (in meters).
        * pdict (dict): A dictionary containing parameters for the 'polyline' shapefile.
        * cdiclist (list): A list of dictionaries containing parameters for the 'trench' shapefile.
        * dataframe_csv (str): Path to CSV file to write master dataframe to.
        * y_listcounter (int): Counter for the number of times the while loop has looped through Y values of trench layout.
        * x_listcounter (int): Counter for the number of times the while loop has looped through X values of trench layout.
    
        Returns:
        * Path to trench shapefile
        """


        xoddy_odd= maxandminy_df.rename(columns={'HC1_Xvalue':'X1', 'HC1_Yvalue': 'Y1' ,'HC2_Xvalue':'X2', 'HC2_Yvalue': 'Y2' ,'HC3_Xvalue':'X3',  'HC3_Yvalue':'Y3', 'HC4_Xvalue': 'X4' ,'HC4_Yvalue': 'Y4'})

        xoddy_odddrop=xoddy_odd.drop(['POINT_X','POINT_Y'], axis=1)




        masterdf=xoddy_odddrop

        del xoddy_odd
        del xoddy_odddrop


        masterdf.to_csv(dataframe_csv, index = False)


        del masterdf


        _xytopolygone(shp_id,dataframe_csv,crs_str)



def _xytopolygone(shp_id,dataframe_csv,crs_str):
        
        

    """Function: _xytopolygone

        Description: This function converts CSV data containing XY coordinates of trenches into a polygon feature
        in a specific spatial reference system.
        It creates temporary line feature classes in memory, processes the CSV data to create line features,
        merges these lines to generate a polygon feature, and finally saves the resulting polygon feature as a shapefile.

        Parameters:
        - shp_id: An identifier for the resulting polygon shapefile.
        - dataframe_csv: Path to the CSV file containing XY coordinate data.
        - crs_str: The spatial reference system string in which the features are defined.

        Returns: None

        Note: The function creates temporary line feature classes to process and transform
        XY coordinate data into polygons. It utilizes the arcpy library for geospatial processing tasks.

        Usage: Call this function with the appropriate parameters to convert XY coordinate data into a polygon feature and save it as a shapefile.

    """






    # Create line feature classes in memory
    c1_c2_fc = arcpy.CreateFeatureclass_management("in_memory", "c1_c2", "POLYLINE", spatial_reference=crs_str)
    c2_c3_fc = arcpy.CreateFeatureclass_management("in_memory", "c2_c3", "POLYLINE", spatial_reference=crs_str)
    c3_c4_fc = arcpy.CreateFeatureclass_management("in_memory", "c3_c4", "POLYLINE", spatial_reference=crs_str)
    c4_c1_fc = arcpy.CreateFeatureclass_management("in_memory", "c4_c1", "POLYLINE", spatial_reference=crs_str)

    # Convert CSV data to line features
    arcpy.XYToLine_management(in_table=dataframe_csv,
                              out_featureclass=c1_c2_fc,
                              startx_field="X1", starty_field="Y1",
                              endx_field="X2", endy_field="Y2",
                              line_type="GEODESIC", id_field="",
                              spatial_reference=crs_str)
    arcpy.XYToLine_management(in_table=dataframe_csv,
                              out_featureclass=c2_c3_fc,
                              startx_field="X2", starty_field="Y2",
                              endx_field="X3", endy_field="Y3",
                              line_type="GEODESIC", id_field="",
                              spatial_reference=crs_str)
    arcpy.XYToLine_management(in_table=dataframe_csv,
                              out_featureclass=c3_c4_fc,
                              startx_field="X3", starty_field="Y3",
                              endx_field="X4", endy_field="Y4",
                              line_type="GEODESIC", id_field="",
                              spatial_reference=crs_str)
    arcpy.XYToLine_management(in_table=dataframe_csv,
                              out_featureclass=c4_c1_fc,
                              startx_field="X1", starty_field="Y1",
                              endx_field="X4", endy_field="Y4",
                              line_type="GEODESIC", id_field="",
                              spatial_reference=crs_str)

    # Merge line features to create polygon feature
    in_features = [c1_c2_fc, c2_c3_fc, c3_c4_fc, c4_c1_fc]
    
    
    output_fc = arcpy.CreateFeatureclass_management("C:/Users/rh363/Documents/SEAHA/PHD Year 1/Gridlayoutresults/", "trench_{0}.shp".format(shp_id), "POLYGON", spatial_reference=crs_str)


    #made into polygone files however there needs to be a clear up of alternating the layout based on Y values
    arcpy.FeatureToPolygon_management(in_features=in_features,
                              out_feature_class=output_fc,
                              cluster_tolerance="0.3",
                              attributes="ATTRIBUTES",
                              label_features="")

    arcpy.DefineProjection_management(in_dataset=output_fc, coor_system=crs_str)


    # Clean up temporary feature classes
    arcpy.Delete_management(c1_c2_fc)
    arcpy.Delete_management(c2_c3_fc)
    arcpy.Delete_management(c3_c4_fc)
    arcpy.Delete_management(c4_c1_fc)
    arcpy.Delete_management(dataframe_csv)

    



def create_grid(LOE_extent,number,length,width,grid_layout_specification,squaredistance=19,angle=0,
                square_shp="in_memory/square_shp",
                square_points="in_memory/pointsofsqaureshp",
                crs_str="PROJCS['British_National_Grid',GEOGCS['GCS_OSGB_1936',DATUM['D_OSGB_1936',SPHEROID['Airy_1830',6377563.396,299.3249646]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',400000.0],PARAMETER['False_Northing',-100000.0],PARAMETER['Central_Meridian',-2.0],PARAMETER['Scale_Factor',0.9996012717],PARAMETER['Latitude_Of_Origin',49.0],UNIT['Meter',1.0]];-5220400 -15524400 450481592.767097;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision",
                sorted_min="in_memory/_sorted_min",
                sorted_max="in_memory/_sorted_max",
                sorted_min_y="in_memory/_sorted_min_y",
                sorted_max_y="in_memory/_sorted_max_y",
                dataframe_csv = "C:/Users/rh363/Documents/SEAHA/PHD Year 1/PythonLocation/dataframe.csv",
                trench_poly_dir = "C:/Users/rh363/Documents/SEAHA/PHD Year 1/PythonLocation/" ):
    """

    Function: create_grid

    Description: This function generates a grid layout of trench points based on specified parameters, including the area of interest (LOE) extent, trench number, dimensions, grid layout type, and additional parameters for adjustments.

    Parameters:
    - LOE_extent: Area of interest extent.
    - number: Number of trenches.
    - length: Length of the trenches.
    - width: Width of the trenches.
    - grid_layout_specification: Type of grid layout.
    - squaredistance: Distance between trenches (default: 19).
    - angle: Rotation angle (default: 0).
    - square_shp: Path to square shapefile (default: "in_memory/square_shp").
    - square_points: Path to point shapefile of square vertices (default: "in_memory/pointsofsqaureshp").
    - crs_str: Coordinate system string (default: British National Grid).
    - sorted_min: Path to sorted minimum values (default: "in_memory/_sorted_min").
    - sorted_max: Path to sorted maximum values (default: "in_memory/_sorted_max").
    - sorted_min_y: Path to sorted minimum Y values (default: "in_memory/_sorted_min_y").
    - sorted_max_y: Path to sorted maximum Y values (default: "in_memory/_sorted_max_y").
    - dataframe_csv: Path to the CSV file for DataFrame (default: "C:/Users/rh363/Documents/SEAHA/PHD Year 1/PythonLocation/dataframe.csv").
    - trench_poly_dir: Directory for trench polygons (default: "C:/Users/rh363/Documents/SEAHA/PHD Year 1/PythonLocation/").

    Returns:
    - ox: X-coordinate of the origin.
    - oy: Y-coordinate of the origin.

    Note: This function generates a grid layout of trenches within the specified area of interest (LOE) extent.

.
     """
    ##    Firstly, with the function the X min and max, and Y min and max (from the LOE extent) is imputed into the generate a tessellation of squares
    ####    using the generate tessellation function in in arcpy.
    ####    The size of the square is determined by the square distance
    ####     This square distance determines how far apart the trenches are spaced



    
    if os.path.exists(square_shp):
        os.remove(square_shp)
    if os.path.exists(square_points):
        os.remove(square_points)
    if os.path.exists(sorted_min):
        os.remove(sorted_min)
    if os.path.exists(sorted_max):
        os.remove(sorted_max)
    if os.path.exists(sorted_min_y):
        os.remove(sorted_min_y)
    if os.path.exists(sorted_max_y):
        os.remove(sorted_max_y)
    if os.path.exists(dataframe_csv):
        os.remove(dataframe_csv)

    areasqaure=squaredistance**2


    square_shp=arcpy.GenerateTessellation_management(Output_Feature_Class="in_memory/square_shp",
                                          Extent=LOE_extent,
                                          Shape_Type="SQUARE",
                                          Size=areasqaure,
                                          Spatial_Reference=crs_str)

    #Point shapefiles are generated based on the vertices of the tessellated squares using arcpy.FeatureVerticesToPoints_management
    
    square_points=arcpy.FeatureVerticesToPoints_management(in_features=square_shp,
                                             out_feature_class=square_points,
                                             point_location="ALL")

    

    
    
    #XY coordinate data is then added to these points using arcpy.AddXY_management(). These coordinates are the central points of each trench.
    

    arcpy.AddXY_management(in_features=square_points)

    #the identical values created from generateing points from a sqaure layout are deleted so there is only one point for each position

    arcpy.DeleteIdentical_management(in_dataset=square_points,
                                     fields="POINT_X;POINT_Y",
                                     xy_tolerance="",
                                     z_tolerance="0")


    min_value_x = float("inf")
    max_value_x = float("-inf")

    min_value_y = float("inf")
    max_value_y = float("-inf")


    with arcpy.da.SearchCursor(square_points, "POINT_X") as cursor:
        for row in cursor:
            
            value = row[0]
            if value < min_value_x:
                min_value_x = value
            if value > max_value_x:
                max_value_x = value


    with arcpy.da.SearchCursor(square_points, "POINT_Y") as cursor:
        for row in cursor:
            value = row[0]
            if value < min_value_y:
                min_value_y = value
            if value > max_value_y:
                max_value_y = value




    # The centroid of the LOE is calculated for all trenches to be rotated around.The centroid of the site (LOE) is calculated using the minimum and maximum x and y values.
    #This coordinates of the central centroid (ox,oy) is used by the rotate function to rotate the entire grid around a central point. (The rotate function
    #uses random central points to rotate each induvial trench when simulating random layouts. The ox and oy is used when the coordinated of the corners of the trench are generated.

    


    ox=(max_value_x+min_value_x)/2

    oy=(max_value_y+min_value_y)/2

    currentx=min_value_x



    values=[]
    #Using the minimum x value of the coordinates. A while loop is created, looping through the POINT_X coordinates of the points.
    #Till the maximum x coordinate is reached. For each loop an entry is made to two lists. These lists alternate the letters [H and V] and [V and H].
    #These HV and VH values represent the orientation of the trenches in the standard grid layout either vertical or horizontal.
    while currentx <= max_value_x:
        
        values.append(currentx)
        currentx+=squaredistance

    HV=(["H","V"]*(len(values)))
    HVvalues=HV[len(values):]

    VH=(["V","H"]*(len(values)))
    VHvalues=VH[len(values):]



    #then before H or V can be lain out.The attribute table of the grid points is made into a data frame which is rounded to 6
    #decimal palces. this dataframe is round6pointcordiates
    
    
    arr = arcpy.da.TableToNumPyArray(square_points,('POINT_X','POINT_Y'))
    dfverticespoints = pd.DataFrame(arr)
    
    df_pointcordinates=np.round(dfverticespoints,decimals=2)

    #The number of Y values dicates how many times the X values are reapeated 
    yvalueslist=df_pointcordinates['POINT_Y'].unique()
    numberofrows=df_pointcordinates['POINT_Y'].nunique()

    
    times_the_HVrepeats = [i for i in range(0,numberofrows)]

    point_x_values_length=[]
    hv_values_length=[]
    vh_values_length=[]

    for i in times_the_HVrepeats:
        point_x_values_length.extend(values)
        hv_values_length.extend(HVvalues)
        vh_values_length.extend(VHvalues)

    
        
    #These two lists are made into a data frame with the x values (which are now extended to the lenght of how many
    #x values there are in the dataframe.
    #the data frame is then deifned as dfa 
    dictonarya={'POINT_X':point_x_values_length,
                'HV_values':hv_values_length,
                'VH_values':vh_values_length}

 
    
    df_cordinatesand_hv_vh=pd.DataFrame(dictonarya,columns=['POINT_X','HV_values','VH_values'])

    # Two dataframes are made and now the POINT_Y has to be added from df_pointcordinates to df_cordinatesand_hv_vh
    # for this both dataframes are sorted by the POINT_X so that the values match.
    
    sorteddf_cordinatesand_hv_vh=df_cordinatesand_hv_vh.sort_values(by=['POINT_X'])
    sorteddf_pointcordinates=df_pointcordinates.sort_values(by=['POINT_X'])

    #The POINT Y column is then made into a list and that list is made into an array

    POINT_Ylist = sorteddf_pointcordinates['POINT_Y'].values.tolist()

    POINT_Yarray = np.array(POINT_Ylist)

    #The POINT Y column is added to the dataframe

    sorteddf_cordinatesand_hv_vh['POINT_Y']=POINT_Yarray

    
    lengthofcontinous=max_value_y-min_value_y


    if grid_layout_specification == "Standard_Grid":
            Standard_Grid_layout(number,sorteddf_cordinatesand_hv_vh,yvalueslist,length, width,crs_str,ox, oy,angle)
    if grid_layout_specification == "Herringbone":
            Herringbone_layout(number,sorteddf_cordinatesand_hv_vh,yvalueslist,length, width,crs_str,ox, oy,angle)
    if grid_layout_specification == "Continous":
            Continous_layout(number,sorteddf_cordinatesand_hv_vh,yvalueslist,lengthofcontinous, width,crs_str,ox, oy,angle,max_value_y)

            

    return ox,oy
    


def Standard_Grid_layout(number,sorteddf_cordinatesand_hv_vh,yvalueslist,length, width,crs_str,ox, oy,angle):

    """
        Function: Standard_Grid_layout

        Description: This function generates trenches in a standard grid pattern with alternating horotizontal then vertical.
        It calculates the coordinates of horizontal and vertical trenches based on input parameters and rotates them according to the specified angle.
        The resulting trench coordinates are used to create a shapefile representing the trenches.

        Parameters:
        - number: An identifier or counter for the trenches being generated.
        - sorteddf_cordinatesand_hv_vh: A DataFrame containing sorted coordinates and trench information.
        - yvalueslist: A list of Y-values corresponding to trench positions.
        - length: Length of the trenches.
        - width: Width of the trenches.
        - crs_str: The spatial reference system string.
        - ox: X-coordinate of the rotation center.
        - oy: Y-coordinate of the rotation center.
        - angle: Angle of rotation in degrees.

        Returns: None

        Note: This function calculates the coordinates of horizontal and vertical trenches for each trench position in the input DataFrame.
        It then rotates these coordinates based on the specified angle and uses the resulting trench coordinates to create a shapefile representing the trenches in a standard grid pattern.

        Usage: Call this function with appropriate parameters to generate trenches in a standard grid pattern with alternating angles.

    """



    hori_val_name_list = [['HC1_Xvalue', 'HC1_Yvalue'],
                          ['HC2_Xvalue', 'HC2_Yvalue'],
                          ['HC3_Xvalue', 'HC3_Yvalue'],
                          ['HC4_Xvalue', 'HC4_Yvalue']]

    

    # Get coordinates of horizontal trenches
    for n, field in enumerate(hori_val_name_list):
        if n == 0:          
            px = sorteddf_cordinatesand_hv_vh['POINT_X'] + length / 2 
            py = sorteddf_cordinatesand_hv_vh['POINT_Y'] + width / 2 
        if n == 1:
            px = sorteddf_cordinatesand_hv_vh['POINT_X'] + length / 2
            py = sorteddf_cordinatesand_hv_vh['POINT_Y'] - width / 2 
        if n == 2:
            px = sorteddf_cordinatesand_hv_vh['POINT_X'] - length / 2
            py = sorteddf_cordinatesand_hv_vh['POINT_Y'] - width / 2 
        if n == 3:
            px = sorteddf_cordinatesand_hv_vh['POINT_X'] - length / 2 
            py = sorteddf_cordinatesand_hv_vh['POINT_Y'] + width / 2 
        rotatedcordinates=rotate(ox, oy, px, py, angle)
        sorteddf_cordinatesand_hv_vh[hori_val_name_list[n][0]]=rotatedcordinates[0]
        sorteddf_cordinatesand_hv_vh[hori_val_name_list[n][1]]=rotatedcordinates[1]

    vert_val_name_list = [['VC1_Xvalue', 'VC1_Yvalue'],
                          ['VC2_Xvalue', 'VC2_Yvalue'],
                          ['VC3_Xvalue', 'VC3_Yvalue'],
                          ['VC4_Xvalue', 'VC4_Yvalue']]

    # Get coordinates of vertical trenches
    for n, field in enumerate(vert_val_name_list):
        # This is the same as the above loop, but with the vertical trench
        # fields input and the width and length are reverse
        if n == 0:
            px = sorteddf_cordinatesand_hv_vh['POINT_X'] + width / 2 
            py = sorteddf_cordinatesand_hv_vh['POINT_Y'] + length / 2 
        if n == 1:
            px = sorteddf_cordinatesand_hv_vh['POINT_X'] + width / 2 
            py = sorteddf_cordinatesand_hv_vh['POINT_Y'] - length / 2 
        if n == 2:
            px = sorteddf_cordinatesand_hv_vh['POINT_X'] - width / 2 
            py = sorteddf_cordinatesand_hv_vh['POINT_Y'] - length / 2 
        if n == 3:
            px = sorteddf_cordinatesand_hv_vh['POINT_X'] - width / 2 
            py = sorteddf_cordinatesand_hv_vh['POINT_Y'] + length / 2 

        rotatedcordinates=rotate(ox, oy, px, py, angle)
        sorteddf_cordinatesand_hv_vh[vert_val_name_list[n][0]]=rotatedcordinates[0]
        sorteddf_cordinatesand_hv_vh[vert_val_name_list[n][1]]=rotatedcordinates[1]


    # Make trench shapefile for however many values are in `counter` variables
    
        # Create trench shapefile, with iteration in the filename
    _create_Standard_Grid_trench_shp(number, sorteddf_cordinatesand_hv_vh, yvalueslist,crs_str)

def Herringbone_layout(number,sorteddf_cordinatesand_hv_vh,yvalueslist,length, width,crs_str,ox, oy,angle):

   """



   Function: Herringbone_layout

   Description: This function generates trenches in a herringbone pattern, alternating at 45-degree angles. It calculates the coordinates of angled trenches based on input parameters and rotates them according to the specified angle. The resulting trench coordinates are used to create a shapefile representing the herringbone pattern.

   Parameters:
   - number: An identifier or counter for the trenches being generated.
   - sorteddf_cordinatesand_hv_vh: A DataFrame containing sorted coordinates and trench information.
   - yvalueslist: A list of Y-values corresponding to trench positions.
   - length: Length of the trenches.
   - width: Width of the trenches.
   - crs_str: The spatial reference system string.
   - ox: X-coordinate of the rotation center.
   - oy: Y-coordinate of the rotation center.
   - angle: Angle of rotation in degrees.

   Returns: None

   Note: This function calculates the coordinates of trenches in a herringbone pattern by offsetting and adjusting the coordinates of the trench ends. It then rotates these coordinates based on the specified angle and uses the resulting trench coordinates to create a shapefile representing the herringbone pattern.

   Usage: Call this function with appropriate parameters to generate trenches in a herringbone pattern alternating at 45-degree angles.

   """




    cosvalue= math.cos(math.radians(45))

    addition_for_rotatiation=(length/2)*(cosvalue)
    

    addition_for_rotatiation=round(addition_for_rotatiation)

    
    changeinend=round((width/cosvalue)-width)


    hori_val_name_list = [['HC1_Xvalue', 'HC1_Yvalue'],
                          ['HC2_Xvalue', 'HC2_Yvalue'],
                          ['HC3_Xvalue', 'HC3_Yvalue'],
                          ['HC4_Xvalue', 'HC4_Yvalue']]

    


    # Get coordinates of trenches angled to the right // 
    for n, field in enumerate(hori_val_name_list):
        if n == 0:          
            px = sorteddf_cordinatesand_hv_vh['POINT_X'] + (width /2)+ (addition_for_rotatiation) -6
            py = sorteddf_cordinatesand_hv_vh['POINT_Y'] + (addition_for_rotatiation) 
        if n == 1:
            px = sorteddf_cordinatesand_hv_vh['POINT_X'] + (width/ 2) - (addition_for_rotatiation) -6
            py = sorteddf_cordinatesand_hv_vh['POINT_Y'] - (addition_for_rotatiation) 
        if n == 2:
            px = sorteddf_cordinatesand_hv_vh['POINT_X'] - (width / 2) - (addition_for_rotatiation) -6
            py = sorteddf_cordinatesand_hv_vh['POINT_Y'] - (addition_for_rotatiation) + (changeinend) 
        if n == 3:
            px = sorteddf_cordinatesand_hv_vh['POINT_X'] - (width / 2) + (addition_for_rotatiation) -6
            py = sorteddf_cordinatesand_hv_vh['POINT_Y'] + (addition_for_rotatiation) + (changeinend)
        rotatedcordinates=rotate(ox, oy, px, py, angle)
        sorteddf_cordinatesand_hv_vh[hori_val_name_list[n][0]]=rotatedcordinates[0]
        sorteddf_cordinatesand_hv_vh[hori_val_name_list[n][1]]=rotatedcordinates[1]

    vert_val_name_list = [['VC1_Xvalue', 'VC1_Yvalue'],
                          ['VC2_Xvalue', 'VC2_Yvalue'],
                          ['VC3_Xvalue', 'VC3_Yvalue'],
                          ['VC4_Xvalue', 'VC4_Yvalue']]

     # Get coordinates of trenches angled to the left \\
    for n, field in enumerate(vert_val_name_list):
        # This is the same as the above loop, but with the vertical trench
        # fields input and the width and length are reverse

        if n == 0:          
            px = sorteddf_cordinatesand_hv_vh['POINT_X'] + (width /2) - (addition_for_rotatiation) 
            py = sorteddf_cordinatesand_hv_vh['POINT_Y'] + (addition_for_rotatiation) + (changeinend)
        if n == 1:
            px = sorteddf_cordinatesand_hv_vh['POINT_X'] + (width/ 2) + (addition_for_rotatiation)
            py = sorteddf_cordinatesand_hv_vh['POINT_Y'] - (addition_for_rotatiation) +(changeinend)
        if n == 2:
            px = sorteddf_cordinatesand_hv_vh['POINT_X'] - (width / 2) + (addition_for_rotatiation)
            py = sorteddf_cordinatesand_hv_vh['POINT_Y'] - (addition_for_rotatiation) 
        if n == 3:
            px = sorteddf_cordinatesand_hv_vh['POINT_X'] - (width / 2) - (addition_for_rotatiation) 
            py = sorteddf_cordinatesand_hv_vh['POINT_Y'] + (addition_for_rotatiation) 
        rotatedcordinates=rotate(ox, oy, px, py, angle)
        sorteddf_cordinatesand_hv_vh[vert_val_name_list[n][0]]=rotatedcordinates[0]
        sorteddf_cordinatesand_hv_vh[vert_val_name_list[n][1]]=rotatedcordinates[1]
    # Make trench shapefile for however many values are in `counter` variables
    
        # Create trench shapefile, with iteration in the filename
    _create_herringbone_trench_shp(number, sorteddf_cordinatesand_hv_vh, yvalueslist,crs_str)




def Continous_layout(number,sorteddf_cordinatesand_hv_vh,yvalueslist,lengthofcontinous, width,crs_str,ox, oy,angle,min_value_y):

    """
        Function: Continous_layout

        Description: This function generates continuous trenches that run parallel to each other across a site area. The trenches are aligned to a specific Y-value and extend longitudinally across the site. The function calculates the trench coordinates based on input parameters, rotates them according to the specified angle, and creates a shapefile representing the continuous trench layout.

        Parameters:
        - number: An identifier or counter for the trenches being generated.
        - sorteddf_cordinatesand_hv_vh: A DataFrame containing sorted coordinates and trench information.
        - yvalueslist: A list of Y-values corresponding to trench positions.
        - lengthofcontinous: Length of the continuous trenches.
        - width: Width of the trenches.
        - crs_str: The spatial reference system string.
        - ox: X-coordinate of the rotation center.
        - oy: Y-coordinate of the rotation center.
        - angle: Angle of rotation in degrees.
        - min_value_y: The Y-coordinate value to which the continuous trenches are aligned.

        Returns: None

        Note: This function generates trenches that run parallel to each other at a specified Y-coordinate value. It calculates trench coordinates by offsetting the aligned Y-value and extending the trench longitudinally. The function then rotates these coordinates based on the specified angle and uses the resulting trench coordinates to create a shapefile representing the continuous trench layout.

        Usage: Call this function with appropriate parameters to generate continuous trenches parallel to each other across a site area.
        a

    """


    hori_val_name_list = [['HC1_Xvalue', 'HC1_Yvalue'],
                          ['HC2_Xvalue', 'HC2_Yvalue'],
                          ['HC3_Xvalue', 'HC3_Yvalue'],
                          ['HC4_Xvalue', 'HC4_Yvalue']]


   
    maxandminy_df=sorteddf_cordinatesand_hv_vh.loc[sorteddf_cordinatesand_hv_vh['POINT_Y'] == np.round(min_value_y,decimals=2)]

   
    for n, field in enumerate(hori_val_name_list):
        if n == 0:          
            px = maxandminy_df['POINT_X'] + width/2  
            py = maxandminy_df['POINT_Y'] + (100*lengthofcontinous)  
        if n == 1:
            px = maxandminy_df['POINT_X'] + width/ 2 
            py = maxandminy_df['POINT_Y'] - (100*lengthofcontinous) 
        if n == 2:
            px = maxandminy_df['POINT_X'] - width / 2 
            py = maxandminy_df['POINT_Y'] - (100*lengthofcontinous)  
        if n == 3:
            px = maxandminy_df['POINT_X'] - width / 2 
            py = maxandminy_df['POINT_Y'] + (100*lengthofcontinous) 
        rotatedcordinates=rotate(ox, oy, px, py, angle)

        maxandminy_df.loc[:, hori_val_name_list[n][0]]=rotatedcordinates[0]

        maxandminy_df.loc[:, hori_val_name_list[n][1]]=rotatedcordinates[1]
        

    _create_Continous_trench_shp(number, maxandminy_df,crs_str)


    
def repeating_create_trench_func(counterofloops,numberofrepeats,
                                 featurelist,LOElist,
                                 LargerLOE,
                                 length,
                                 width,periodcolumnlist,
                                 squaredistance,
                                 anglelist,
                                 pdict,cdiclist,p,grid_layout_specification,
                                 wbA = xlwt.Workbook(),wb1A = xlwt.Workbook(),wb2A=xlwt.Workbook(),
                                 wbB = xlwt.Workbook(),wb1B = xlwt.Workbook(),wb2B=xlwt.Workbook(),
                                 wbC = xlwt.Workbook(),wb1C = xlwt.Workbook(),wb2C=xlwt.Workbook(),
                                 wbD = xlwt.Workbook(),wb1D = xlwt.Workbook(),wb2D=xlwt.Workbook(),
                                 wbE = xlwt.Workbook(),wb1E = xlwt.Workbook(),wb2E=xlwt.Workbook(),
                                 wbF = xlwt.Workbook(),wb1F = xlwt.Workbook(),wb2F=xlwt.Workbook(),
                                 wbG = xlwt.Workbook(),wb1G = xlwt.Workbook(),wb2G=xlwt.Workbook(),
                                 wbH = xlwt.Workbook(),wb1H = xlwt.Workbook(),wb2H=xlwt.Workbook()):
        """


        Function: repeating_create_trench_func

        Description: This function generates trenches repeatedly for a specified number of loops.
        It iterates through different layout specifications, calculates trench coordinates, clips them to specified areas of interest,
        performs analyses, and stores results in Excel sheets. It acts as a master function for the trenching model

        Parameters:
        - counterofloops: Counter for the current loop.
        - numberofrepeats: Number of times to repeat the trench generation process.
        - featurelist: List of feature datasets.
        - LOElist: List of area of interest (LOE) datasets.
        - LargerLOE: Larger area of interest dataset.
        - length: Length of the trenches.
        - width: Width of the trenches.
        - periodcolumnlist: List of period columns.
        - squaredistance: Distance between grid points for layout creation.
        - anglelist: List of rotation angles.
        - pdict: Dictionary of percentages for analysis.
        - cdiclist: List of dictionaries for different percentage layouts.
        - p: List of percentages.
        - grid_layout_specification: Specification for the grid layout.
        - wbA, wb1A, wb2A, ..., wbH, wb1H, wb2H: Workbook instances for different layout results.

        Returns: None

        Note: This function iterates through different layout specifications and generates trenches based on the given parameters. It clips the generated trenches to specified areas of interest, calculates various metrics, and stores the results in Excel sheets. The function can be used to generate multiple variations of trench layouts and analyze their impact on different metrics.

        Usage: Call this function with appropriate parameters to repeatedly generate and analyze trench layouts for the specified number of loops.

        """

                
        
        
        
    
 

        number=1

        workbook_map = {1: (wbA, wb1A, wb2A), 
                        2: (wbB, wb1B, wb2B), 
                        3: (wbC, wb1C, wb2C), 
                        4: (wbD, wb1D, wb2D), 
                        5: (wbE, wb1E, wb2E), 
                        6: (wbF, wb1F, wb2F), 
                        7: (wbG, wb1G, wb2G), 
                        8: (wbH, wb1H, wb2H)}
            


        summary_table_path_period="C:/Users/rh363/Documents/SEAHA/PHD Year 2/validating layouts/summarytable/summarytableperiod_{}_".format(grid_layout_specification)
        summary_table_path_size="C:/Users/rh363/Documents/SEAHA/PHD Year 2/validating layouts/summarytable/summarytablesize__{}_".format(grid_layout_specification)
        summary_table_path_size_in_period="C:/Users/rh363/Documents/SEAHA/PHD Year 2/validating layouts/summarytable/summarytablesizeinperiod_{}_".format(grid_layout_specification)


        for i,n in zip(featurelist,LOElist):
                

                add_area_values(i)
                add_area_values(n)



        additionlist=range(-140,140)
        angle=random.choice(anglelist)


        LOE_extent=calculate_min_max_values(LargerLOE)

        LOEsum_dict = {}

        # Loop through the LOElist and calculate the LOEsum values
        for LOE in LOElist:
                LOEsum = float(arcpy.da.TableToNumPyArray(LOE, "POLY_AREA", skip_nulls=True)["POLY_AREA"].sum())
                LOEsum_dict[LOE] = LOEsum

            

        ### This while loop allows the process of generateing trench layout out to be reapeated
        ### depending on the specifed number of repeats. Each trench layout is slightly differnt
        ### position due to the chaneging angle of rotation and the random layout of  grid points which
        ###change with additionX additionY
        start_time_of_loop = datetime.datetime.now()
        print ("start time of loops")
        start_time_of_creating_grid = datetime.datetime.now()
        print (start_time_of_creating_grid)


        ox,oy,total_number_of_trenches_list=creatinggrids(angle,LOE_extent,number,length,width,squaredistance,grid_layout_specification)
            
        end_time_of_creatinggrid = datetime.datetime.now()
        duration_of_creatinggrid = end_time_of_creatinggrid - start_time_of_creating_grid
        print ("time it takes to create grid layouts of 1-15% coverage")
        print (duration_of_creatinggrid)


        while counterofloops <= numberofrepeats:
                #the addition list of the Y cordinates must be the height of the site (and the height of the larger LOE must be three times the height of the site)
                #the addition list of the X cordinates must be the width of the site (and the height of the larger LOE must be three times the width of the site)

                additionX=random.choice(additionlist)
                additionY=random.choice(additionlist)

                angle=random.choice(anglelist)


                #### Once every differnt percenage coverage of grid has been made the loop is exited for excel sheets to be made

                ##########now that the grid is made it can be clipped into the differnt LOEs and feature groups 
                counterforworkbooks=1
                ## each work book is for the results of the differnt layouts


                for LOE, feature, period, cdic in zip(LOElist, featurelist, periodcolumnlist,cdiclist):
                        LOEname = LOE[-10:-4]
                        featurename = feature[-10:-4]
                        ##the layouts are clipped so that they overaly the LOE and then made into percentages
                        clipping_and_buffering(LOE,pdict,cdic,LOEsum_dict,additionX,additionY,angle,ox,oy,total_number_of_trenches_list)

                        periodcolumn1 = period[0]
                        periodcolumn2 = period[1]


                        wb, wb1, wb2 = workbook_map[counterforworkbooks]

                        comanfordifferntworkbooks(wb, wb1, wb2, feature, featurename, periodcolumn1, periodcolumn2, 
                                                      counterofloops, p, LOEname, LOE, summary_table_path_period, 
                                                      summary_table_path_size, summary_table_path_size_in_period, angle)

                        arcpy.Delete_management("in_memory")

                        counterforworkbooks += 1



                
                    ####Each run of percentages (p) for eaxample 1%,5% and 15% sampling the results of this analysis  is placed into an excel sheet. When this process is repeated a new-
                    #-sheet is created. 

                cdic1= {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0}
                cdic2 = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0}
                cdic3= {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0}
                cdic4 = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0}
                cdic5= {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0}
                cdic6 = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0}
                cdic7= {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0}
                cdic8 = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0}

                cdiclist=[cdic1,cdic2,cdic3,cdic4,cdic5,cdic6,cdic7,cdic8]

                number=1

                counterofloops+=1


                delete_contents_of_folder("C:/Users/rh363/Documents/SEAHA/PHD Year 1/PythonLocation")
                end_time_of_loop = datetime.datetime.now()

                duration_of_loop = end_time_of_loop - start_time_of_loop


        delete_contents_of_folder("C:/Users/rh363/Documents/SEAHA/PHD Year 1/PythonLocation")
        arcpy.Delete_management("in_memory")
        print ("finally ended!!!!")




def calculate_min_max_values(LargerLOE):
    """
    Calculate min max values creates an array containing the min max values for each polygon of the site area. A large
    shapefile (LargerLOE) that is includes the site (LOE) and some surrounding areas, is imputed. This large shapefile
    (LargerLOE) is used rather than the site area shapefile (LOE) so that the grid layout is generated much larger then
    the site area (LOE) to allow for the grid to be rotated over the site without leaving blank spaces when clipped to the
    extent of the site (LOE) in the function clipping and buffering. 
    To Calculate the extent values, first an empty array is produced to store the points (arr).Then for every polygone
    within the LOE extent(row).
    The feilds are queryed and the extent calculated and added to the array. The collected
    points are converted to a multipoint (mp) and the extent of all the polygones is determined (mp.extent).For the
    moment the total site extent (LOE_extent) is used though extent values of each individual polygon (which
    represent each area of the site) are not used at the moment this could come in useful for different work.


    Uses: arcpy.da.SearchCursor(LargerLOE,['FID','SHAPE@']).  Geometry properties of the polygons are accessed by specifying the token SHAPE@ in the list of fields.
    Code sources: https://community.esri.com/t5/python-questions/what-means-typeerror-row-object-does-not-support-indexing/td-p/598927
    Imputs: LargerLOE (a shapefile covering the area in which a grid of trenches will be made this must be bigger than the desired site to allow for rotation)
    Outputs: LOEextent ( The minimum and maximum x and y coordinates of an area)
    """
    
    arr = arcpy.Array()
    
    with arcpy.da.SearchCursor(LargerLOE,['FID','SHAPE@']) as cur:  
        for row in cur:
            ext = row[1].extent  
            p0 = ext.lowerLeft; p1 = ext.upperRight
            arr.add(p0)  
            arr.add(p1)  
        mp = arcpy.Multipoint(arr)
        LOE_extent=mp.extent

    return LOE_extent
        


def add_area_values(Shape, area="AREA", length_unit="", area_unit="",
                    crs_str="PROJCS['British_National_Grid',GEOGCS['GCS_OSGB_1936',DATUM['D_OSGB_1936',SPHEROID['Airy_1830',6377563.396,299.3249646]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',400000.0],PARAMETER['False_Northing',-100000.0],PARAMETER['Central_Meridian',-2.0],PARAMETER['Scale_Factor',0.9996012717],PARAMETER['Latitude_Of_Origin',49.0],UNIT['Meter',1.0]]",
                    verbose=False):
`   """
    ##Add area values calculates and adds each area value to each polygon within a shapefile.
    #For the Total area of the sum of all the polygones to be generated Area values must be added
    #first a feild is added to the attribute table of the polygone. This feild is titled POLY_AREA then the shape area is calcaulted giving the area values for each polygone
    """


    lstFields = arcpy.ListFields(Shape)

    x = False

    for field in lstFields:
        if field.name == "POLY_AREA":
            
            x = True

    if x == False:
    
        arcpy.AddGeometryAttributes_management(Input_Features=Shape,
                                           Geometry_Properties=area,
                                           Length_Unit=length_unit,
                                           Area_Unit=area_unit,
                                           Coordinate_System=crs_str)


def calculate_total_area(LOEsum, gridunitssum):
    """
    This function calculates what the is the percentage coverage of each potential  grid layout. This is done by calculating the sum of the side area (LOE area)
    and the sum of the trench areas (gridunitssum). These two outputs are then used to calculate the percentage coverage of each grid layout (percentageoflayout).
    Inputs: The sum of the "POLY_AREA" field from the shapefiles of the site area (LOEsum) and the shapefiles of the trench layout (gridunitssum)
    Outputs: percentage coverage of the trench layouts (percentageoflayout)
    """
    percentageoflayout = (gridunitssum / LOEsum) * 100

    return percentageoflayout

def calculate_total_areas(Shape,identifier):
    """
    This earlier function also calculates the total areas of shapefiles with many different polygons. This function is used to  This is used to calculate
    the site area (LOEsum). From this the number of sample units can be made using the calculate number of sample units function (This is used in test pit layout code)
    The number of sample units is the total number of test pit squares that can potentially be selected as samples. This function uses an identifier to perform different
    specific tasks. it also calculates the area of the test pits (gridunits) and features (Area_of_total_features). 
    Imputs: The shapefiles of the site area (LOE) or features (features) and the shapefiles of the gridunits that will potentially be sampled (gridunits)
    Outputs: area of site (LOEsum), area of trench layouts (gridunitsum),  the area of all the features combined (Area_of_total_features).
    """

    if identifier ==0:
        
        #The table of the shapefile analysised is converted to an array, which then allows the values to be analysised and manipulated. In this case the sum is calculated.
        field = arcpy.da.TableToNumPyArray(Shape, "POLY_AREA", skip_nulls=True)
        LOEsum = field["POLY_AREA"].sum()

        Calculate_Number_of_sample_units(LOEsum)
        
    if identifier==1:

        #The table of the shapefile analysised is converted to an array, which then allows the values to be analysised and manipulated. In this case the sum is calculated.
        field = arcpy.da.TableToNumPyArray (Shape, "POLY_AREA", skip_nulls=True)
    
        gridunitssum = field["POLY_AREA"].sum()

        
    if identifier==2:
        
        field = arcpy.da.TableToNumPyArray(Shape, "POLY_AREA", skip_nulls=True)
    
        Area_of_total_features = field["POLY_AREA"].sum()

        return Area_of_total_features 


def delete_contents_of_folder(filelocation):
    """
    this deletes contents of the folder
    """
    selectionfolder = filelocation
    for filename in os.listdir(selectionfolder):
        file_path = os.path.join(selectionfolder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)                
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def rotate(ox,oy,px,py, angle=0):
    """
    Rotate function rotates one coordinate (px,py) counter clockwise around another coordinate (ox and oy).

    With grid function the points around which the points are rotated are all the same (the central point of the site)
    While with random layout each polygone is rotated around a random centre point. 
    ox and oy are the x and y origin points around which the 
    rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in radians so is converted.
    """
    

    #The angle should be given in radians so the imputed degrees are made into radians
    r=math.radians(angle)

    qx = ox + math.cos(r) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(r) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def create_dict_from_polygontable(shape_path, period_column, period_column_size):
    """
    Creates dictionaries from a polygon shapefile attribute table.

    Inputs:
    - shape_path: path to the shapefile
    - period_column: column title which contains the period values in any feature shapefile's attribute table 
    - period_column_size: column title which contains the size values in any feature shapefile's attribute table

    Outputs:
    - featurelayerdictionary: dictionary of count of features based on period column value
    - featuresumarea: dictionary of sum of areas based on period column value
    - featurelayerdictionary_size: dictionary of count of features based on period column size value
    - featuresumarea_size: dictionary of sum of areas based on period column size value
    """
    # create a list of the fields in the attribute table
    fields = [f.name for f in arcpy.ListFields(shape_path)]

    # create an empty list to store the attribute table records
    attribute_table = []

    # use a search cursor to loop through the rows in the attribute table and add each row to the list
    with arcpy.da.SearchCursor(shape_path, fields) as cursor:
        for row in cursor:
            attribute_table.append(row)

    # convert the attribute table to a pandas dataframe
    df = pd.DataFrame(attribute_table, columns=fields)

    # Group the dataframe by the Type column and count the number of occurrences of each unique value, generating a dictionary
    featurelayerdictionary = df[period_column].value_counts().to_dict()

    # Group the dataframe by the Type column and sum the POLY_AREA column, generating a dictionary
    featuresumarea = df.groupby(period_column)['POLY_AREA'].sum().to_dict()

    # Count the values in the specified column and generate a dictionary
    featurelayerdictionary_size = df[period_column_size].value_counts().to_dict()

    # Group the dataframe by the Type column and sum the POLY_AREA column, generating a dictionary
    featuresumarea_size = df.groupby(period_column_size)['POLY_AREA'].sum().to_dict()

    return featurelayerdictionary, featuresumarea, featurelayerdictionary_size, featuresumarea_size

 
def select_clip_extract_by_grid(i,features,periodcolumn,periodcolumnsize,LOEname,trenchestoclip,
                                clipped_dir="in_memory/",
                                crs_str="PROJCS['British_National_Grid',GEOGCS['GCS_OSGB_1936',DATUM['D_OSGB_1936',SPHEROID['Airy_1830',6377563.396,299.3249646]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',400000.0],PARAMETER['False_Northing',-100000.0],PARAMETER['Central_Meridian',-2.0],PARAMETER['Scale_Factor',0.9996012717],PARAMETER['Latitude_Of_Origin',49.0],UNIT['Meter',1.0]]"):
    """
    this uses the grid shapefiles and clips the features with them. providing a result of excel files containg the clipped features

    The purpose of the code is to extract information about the areas and counts of polyggon features in a given input dataset, based on values in certain columns.

    The code starts by clipping the input features with a grid shapefile, and adding attributes to the resulting clipped features,
    including the area and part count of each feature. It then converts the clipped features to an Excel file and reads the data into a Pandas dataframe.

    Next, the code uses several functions to extract information from the dataframe based on values in two specified columns: "periodcolumn" and "periodcolumnsize".
    The functions include "count_layers_based_on_column_value", "sum_of_areas_based_on_column_value", "count_layers_in_layers_based_on_column_value",
    and "sum_layers_in_layers_based_on_column_value". These functions likely summarize the data in the dataframe and return dictionaries of results.

    The final step is to store the results of these operations in several dictionaries, including "countvaluesdictionary", "layerdictionary", "sumareadictionary",
    "countvaluesdictionary_size", "layerdictionary_size", "sumareadictionary_size", "countfeaturelayerdictionarysize", "sum_featurelayersize", and "layerdictionary_in_size".


    """

		
    #clipping the features by selected layers
    clipname="clip{}_{}".format(LOEname,i)
    
    clipped_path = os.path.join(clipped_dir, clipname)
    
    arcpy.Clip_analysis(in_features=features, clip_features=trenchestoclip,
                        out_feature_class=clipped_path, cluster_tolerance="0.01")
    #adding a feild showing the area of the features identified
    arcpy.Delete_management(trenchestoclip)

    arcpy.AddGeometryAttributes_management(Input_Features=clipped_path,
                                           Geometry_Properties="AREA",
                                           Length_Unit="", Area_Unit="",
                                           Coordinate_System=crs_str)
    #adding a count of all the polygones in one layer
    arcpy.AddGeometryAttributes_management(Input_Features=clipped_path,
                                           Geometry_Properties="PART_COUNT",
                                           Length_Unit="METERS", Area_Unit="",
                                           Coordinate_System="")

    # create a list of the fields in the attribute table
    fields = [f.name for f in arcpy.ListFields(clipped_path)]

    # create an empty list to store the attribute table records
    attribute_table = []

    # use a search cursor to loop through the rows in the attribute table and add each row to the list
    with arcpy.da.SearchCursor(clipped_path, fields) as cursor:
        for row in cursor:
            attribute_table.append(row)

    # convert the attribute table to a pandas dataframe
    df = pd.DataFrame(attribute_table, columns=fields)

    arcpy.Delete_management(clipped_path)
    
    # Group the dataframe by the Type column and count the number of occurrences of each unique value, generating a dictionary
    countvaluesdictionary = df[periodcolumn].value_counts().to_dict()

    # Group the dataframe by the Type column and sum the POLY_AREA and PART_COUNT column, generating a dictionary
    layerdictionary = df.groupby(periodcolumn)['PART_COUNT'].sum().to_dict()

    sumareadictionary = df.groupby(periodcolumn)['POLY_AREA'].sum().to_dict()

    # Count the values in the specified column and generate a dictionary
    countvaluesdictionary_size = df[periodcolumnsize].value_counts().to_dict()

    # Group the dataframe by the Type column and sum the POLY_AREA column, generating a dictionary

    layerdictionary_size=df.groupby(periodcolumnsize)['PART_COUNT'].sum().to_dict()
    sumareadictionary_size = df.groupby(periodcolumnsize)['POLY_AREA'].sum().to_dict()


    countfeaturelayerdictionarysize = df.groupby([periodcolumn, periodcolumnsize]).size().to_dict()
    sum_featurelayersize = df.groupby([periodcolumn, periodcolumnsize])['POLY_AREA'].sum().to_dict()
    layerdictionary_in_size = df.groupby([periodcolumn, periodcolumnsize])['PART_COUNT'].sum().to_dict()


    return countvaluesdictionary,layerdictionary,sumareadictionary,countvaluesdictionary_size,layerdictionary_size,sumareadictionary_size,countfeaturelayerdictionarysize,sum_featurelayersize,layerdictionary_in_size



def count_the_values_in_shapefile(Shape):
    """
    Shapefiles are imputed to give the total number of values. This is either the total number of features or the total number of grid units (either test pits or trenches).
    Features layers are imputed to give the total number of features which gives a total number of features which allows the percentage of features found for each type to be
    calculated. 
    Uses: arcpy.GetCount_management()
    Imputs: The shapefiles features (features) 
    Outputs: The count of the number of features (Totalnumberoffeatures) 
    """

    #by using the arcpy function get count the number of possible units to sample from is generated. (As it includes the 0 value the number is count-1)
    count=arcpy.GetCount_management(in_rows=Shape).getOutput(0)
    Totalnumberoffeatures=int(count)-1
    return Totalnumberoffeatures

def write (c1,c2,sheetname,info):
    """
    Write allows the code to write informatio into excel
    """

    sheetname.write(c1,c2,info)

def write_sum_formula(dictionaryname,column,sheetname,Totalnumberoffeatures,Area_of_total_features,countvaluesdictionary,layerdictionary,sumareadictionary,featurelayerdictionary):
    """
    Write formla is for imputing formulas into an excel file useing the stupid AA AB numbering system of excel. This then allow total values ect to be calucaulted-
    As the calculations done in excel are unable to be read by the plot function that makes graphs the write sum formaula function is no longer used.
    """

    if dictionaryname=="countvaluesdictionary_size":
        totalvalue=sum(countvaluesdictionary.values())
        rowvalue=len(featurelayerdictionary)+1
        write(rowvalue,column,sheetname,float(totalvalue))
              
    if dictionaryname=="layerdictionary_size":
        totalvalue=sum(layerdictionary.values())
        rowvalue=len(featurelayerdictionary)+1
        write(rowvalue,column,sheetname,float(totalvalue))
 
    if dictionaryname=="sumareadictionary_size":
        totalvalue=sum(sumareadictionary.values())
        rowvalue=len(featurelayerdictionary)+1
        write(rowvalue,column,sheetname,float(totalvalue))


    if dictionaryname=="countvaluesdictionary":
        totalvalue=sum(countvaluesdictionary.values())
        rowvalue=len(featurelayerdictionary)+1
        write(rowvalue,column,sheetname,float(totalvalue))
              
    if dictionaryname=="layerdictionary":
        totalvalue=sum(layerdictionary.values())
        rowvalue=len(featurelayerdictionary)+1
        write(rowvalue,column,sheetname,float(totalvalue))
 
    if dictionaryname=="sumareadictionary":
        totalvalue=sum(sumareadictionary.values())
        rowvalue=len(featurelayerdictionary)+1
        write(rowvalue,column,sheetname,float(totalvalue))

    if dictionaryname=="percentage_of_values":
        rowvalue=len(featurelayerdictionary)+1    
        totalsumvalue=sum(countvaluesdictionary.values())
        columndividing=float(totalsumvalue)/float(Totalnumberoffeatures)
        percetangecountvalue=round(columndividing*100,2)
        write(rowvalue,column,sheetname,float(percetangecountvalue))

    if dictionaryname=="percentage_of_Areas":
        rowvalue=len(featurelayerdictionary)+1    
        totalareavalue=sum(sumareadictionary.values())
        columndividing=float(totalareavalue)/float(Area_of_total_features)
        percetangeareavalue=round(columndividing*100,2)        
        write(rowvalue,column,sheetname,float(percetangeareavalue))

def write_in_summary_row(dictionaryname,column,Counter_for_percent,sheetname,featurelayerdictionary,featuresumarea,countvaluesdictionary,layerdictionary,sumareadictionary):   
    """
    To put the values of the dictionaries in the right columns of the table. The dictionaries must be read with a for in loop. For each value of the dictionary the featurelist (which-
    dictates the order of the rows in the summary table) is read making the dictionay write it in the correct order.
    """

    
    
    c=1
    d=1
    e=1
    f=1
    g=2
    h=1
    j=2

    if dictionaryname=="countvaluesdictionary_size":
        for x in featurelayerdictionary:
            for p in countvaluesdictionary:
                if x==p:
                    write(c,column,sheetname,float(countvaluesdictionary[p]))
            c+=1

    if dictionaryname=="layerdictionary_size":
        for x in featurelayerdictionary:            
            for p in layerdictionary:
                if x==p:
                    write(d,column,sheetname,float(layerdictionary[p]))                    
            d+=1

    if dictionaryname=="sumareadictionary_size":
        for x in featurelayerdictionary:            
            for p in sumareadictionary:
                if x==p:
                    write(e,column,sheetname,float(sumareadictionary[p]))
            e+=1

    
    if dictionaryname=="countvaluesdictionary":
        for x in featurelayerdictionary:
            for p in countvaluesdictionary:
                if x==p:
                    write(c,column,sheetname,float(countvaluesdictionary[p]))
            c+=1

    if dictionaryname=="layerdictionary":
        for x in featurelayerdictionary:            
            for p in layerdictionary:
                if x==p:
                    write(d,column,sheetname,float(layerdictionary[p]))                    
            d+=1

    if dictionaryname=="sumareadictionary":
        for x in featurelayerdictionary:            
            for p in sumareadictionary:
                if x==p:
                    write(e,column,sheetname,float(sumareadictionary[p]))
            e+=1

    if dictionaryname=="percentage_of_values":
        for x in featurelayerdictionary:
            for p in countvaluesdictionary:
                if x==p:
                    percentagevalue=float(countvaluesdictionary[p])/float(featurelayerdictionary[x])                                     
                    percentagevalue=round(percentagevalue*100,2)
                    write(f,column,sheetname,percentagevalue)
            f+=1
               
    if dictionaryname=="percentage_of_Areas":
        for x in featuresumarea:
            for p in sumareadictionary:
                if x==p:
                    percentagearea=sumareadictionary[p]/featuresumarea[x]
                    percentagearea=round(percentagearea*100,2)
                    write(h,column,sheetname,percentagearea)
            h+=1


def write_in_summary_row_for_double_dict(dictionaryname,column,Counter_for_percent,sheetname,featurelayerdictionary,featuresumarea,featurelayerdictionaryofsize,featuresumareaofsize,
                                         countfeaturelayerdictionarysize,sum_featurelayersize,layerdictionary_in_size,countvaluesdictionary,sumareadictionary):   
    """
    To put the values of the dictionaries in the right columns of the table. The dictionaries must be read with a for in loop.
    For each value of the dictionary the featurelist (which-
    dictates the order of the rows in the summary table) is read making the dictionay write it in the correct order.
    """

    
    
    c=1
    d=1
    e=1
    f=1
    g=2
    h=1
    j=2
    
        
    if dictionaryname=="countfeaturelayerdictionarysize":
        for x in featurelayerdictionary:
            for y in featurelayerdictionaryofsize:
                for p,q in countfeaturelayerdictionarysize:
                    if x==p:
                        if y==q:
                            write(c,column,sheetname,float(countfeaturelayerdictionarysize[p,q]))
                c+=1

    if dictionaryname=="layerdictionary_in_size":

        for x in featurelayerdictionary:
            for y in featurelayerdictionaryofsize:
                for p,q in layerdictionary_in_size:
                    
                    if x==p:
                        if y==q:

                            write(d,column,sheetname,float(layerdictionary_in_size[p,q]))                    
                d+=1

    if dictionaryname=="sum_featurelayersize":

        for x in featurelayerdictionary:
            for y in featurelayerdictionaryofsize:
                for p,q in sum_featurelayersize:
                    if x==p:
                        if y==q:
                            write(e,column,sheetname,float(sum_featurelayersize[p,q]))
                e+=1

    if dictionaryname=="percentage_of_values":
        
        for x in featurelayerdictionary:
            for y in featurelayerdictionaryofsize:
                for p,q in countfeaturelayerdictionarysize:
                    if x==p:
                        if y==q:
                            percentagevalue=float(countfeaturelayerdictionarysize[p,q])/float(featurelayerdictionary[x])
                            percentagearea= round(percentagevalue*100,2)
                            write(f,column,sheetname,percentagearea)
                f+=1
               
    if dictionaryname=="percentage_of_Areas":
        for x in featuresumarea:
            for y in featuresumareaofsize:
                for p,q in sum_featurelayersize:
                    if x==p:
                        if y==q:
                            percentagevalue=float(sum_featurelayersize[p,q])/float(featuresumarea[x])
                            percentagearea=round(percentagevalue*100,2)
                            write(h,column,sheetname,percentagearea)
                h+=1
    

def clipping_and_buffering(LOE,pdict,cdic,LOEsum_dict,additionX,additionY,angle,ox,oy,total_number_of_trenches_list,
                          crs_str="PROJCS['British_National_Grid',GEOGCS['GCS_OSGB_1936',DATUM['D_OSGB_1936',SPHEROID['Airy_1830',6377563.396,299.3249646]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',400000.0],PARAMETER['False_Northing',-100000.0],PARAMETER['Central_Meridian',-2.0],PARAMETER['Scale_Factor',0.9996012717],PARAMETER['Latitude_Of_Origin',49.0],UNIT['Meter',1.0]]"):
        
    """

    Function: clipping_and_buffering

    Description: This function clips generated trench layouts to specified areas of interest, adjusts their positions, and calculates coverage percentages over the areas of interest.

    Parameters:
    - LOE: Area of interest (LOE) dataset for clipping and buffering.
    - pdict: Dictionary of percentage ranges for analysis.
    - cdic: Dictionary of closest percentage matches.
    - LOEsum_dict: Dictionary of LOE area sums.
    - additionX: X-coordinate addition for position adjustment.
    - additionY: Y-coordinate addition for position adjustment.
    - angle: Rotation angle for position adjustment.
    - ox: X-coordinate of the origin for rotation.
    - oy: Y-coordinate of the origin for rotation.
    - total_number_of_trenches_list: List of trench layout numbers.
    - crs_str: Coordinate system string (defaulted to British National Grid).

    Returns: None

    Note: This function iterates through trench layouts, adjusts their positions and rotations, clips them to specified areas of interest (LOEs), and calculates the coverage percentages over the LOEs. The function compares the calculated percentages with the defined percentage ranges and determines the closest match to save.

    Usage: Call this function with appropriate parameters to clip, adjust, and analyze trench layouts based on the specified LOE and percentage ranges.
    """
      



    LOEname=LOE[-10:-4]
    LOEsum = LOEsum_dict[LOE]



    ##This function makes takes the layouts made previously into memory by the create grid function and checks for
    ##the layout most apropriate for the plist making 15 layouts over the LOE



    for i in total_number_of_trenches_list:


            Layout="C:/Users/rh363/Documents/SEAHA/PHD Year 1/Gridlayoutresults/trench_{0}.shp".format(i)

            ###the list of LOE's are inserted so that the large trench layouts are clipped against the differnt LOEs of the real site data making sure each trench layout has the percentage
            ###layout spesific for each sites LOE 

            trenches="in_memory/layout{}_{}".format(LOEname,i)

            moved_trenches="in_memory/moved_layout{}_{}".format(LOEname,i)


            ##tfirst the layout is moved and rotated so it is unique

            arcpy.CopyFeatures_management(in_features=Layout, out_feature_class=moved_trenches, config_keyword="", spatial_grid_1="0",spatial_grid_2="0", spatial_grid_3="0")

            arcpy.DefineProjection_management(in_dataset=moved_trenches, coor_system=crs_str)

            shift_features(moved_trenches,additionX,additionY,angle,ox,oy)

            # the trench layouts are then cliped to the size of the site
            arcpy.Clip_analysis(in_features=moved_trenches, clip_features=LOE, out_feature_class=trenches, cluster_tolerance="")

            try:
                    
                    arcpy.RepairGeometry_management(trenches)
            except:
                           
                    if arcpy.Exists(trenches):
                            print ("here but not working?")
                            continue
                    else:
                            print ("just not here")
                            continue
                           

            
            arcpy.DefineProjection_management(in_dataset=trenches, coor_system=crs_str)

            # the area is calculated
            add_area_values(trenches)

            gridunitssum = float(arcpy.da.TableToNumPyArray(trenches, "POLY_AREA", skip_nulls=True)["POLY_AREA"].sum())

            maxpercentage = calculate_total_area(LOEsum, gridunitssum)


            """
            percentage layout is caluclted then used to select whether or not the layout fits within the percentages we are analysising.
            The percentage coverage of this trench layout (layout{}.shp) over the LOE is then calculated using the calculate_total_area() function.
            The percentage area checked whether it is within the range of one of the percentage dictionaries(pdict). As the layouts are made with
            larger and larger square distance gradually the percentage coverage gets smaller. Each time a grid layout is made and fund to be within
            the dictionary’s (pdicts range) it is saved as its number of percentage coverage (either 1-15%) in the file labelled Gridpercentages. As
            the change in the size of grid square changes the percentage coverage only very slightly, each time a new percentage is made within the
            dictionary it is compared to the previous entry and the layout closest to the key (ie 1-15%) is elected. This makes the layouts very close
            to the actual percentage coverage.
            """

            for key in pdict:
                    
                                     
                    value=pdict[key]
                    
                    

                    if maxpercentage >= value[0] and maxpercentage <= value[1]:
                                                   
                                                
                            
                            currentclosest=cdic[key]
                            one=key-maxpercentage
                            two=key-currentclosest
                            if one<two:
                                    cdic[key]=maxpercentage

                                    print ("IT WAS MADE AT__{}_trenches_FOR_LOE {}_AT_PERCENTAGE_{}".format(i,LOEname,key))

                                    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script

                                    percentagegridlayout = "in_memory/finalpercentage_{}__{}".format(LOEname,key)
                                    arcpy.CopyFeatures_management(in_features=trenches, out_feature_class=percentagegridlayout, config_keyword="", spatial_grid_1="0",spatial_grid_2="0", spatial_grid_3="0")
                                    arcpy.DefineProjection_management(in_dataset=percentagegridlayout, coor_system=crs_str)

            arcpy.Delete_management(trenches)

            arcpy.Delete_management(moved_trenches)

      

            

