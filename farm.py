from dataclasses import field
import logging
from resources import Singleton
from field import Field
from math import floor

class Farm(Singleton):
    def __init__(self):
        self._fields = {0:Field()}
        self._crop_sums = {}

    def create_field(self, plot_type, num_rows, num_cols):
        new_key = len(self._fields)
        field = Field(plot_type, num_rows, num_cols)
        self._fields[len(self._fields)] = field

    def get_space_location_from_field_row(self, field, field_row):
        '''
        Converts field row into the plot, space location

            Parameters: 
                field (int): field number
                field_row (int): the number of the row in the field scope

            Return:
                plot_num, row_num (list<int,int>):  plot_num: index of the plot the space is int
                                                    row_num: row_num number of the row in the plot
        '''
        num_plot_rows = field.get_plot_type().get_plot_size()[0]
        return [field_row / num_plot_rows, field_row % num_plot_rows]

    def get_space(self, field, plot_coords, space_coords):
        '''
        Gets the crop in a single space given the location of the space

            Parameters:
                field (int): The index of the field in self._fields
                plot_coords (resources.Coords): The coordinates of the plot in the field
                space_coords (resources.Coords): The coordinates of the space in the plot

            Returns:
                space (Crop): the crop at the given location
        '''
        return self._fields[field].get_plot(plot_coords).get_space(space_coords)

    #sets a single space with a crop field
    def set_space(self, crop, field, plot_coords, space_coords):
        '''
        Sets a single space with a crop.

            Parameters:
                crop (Crop): The crop to place
                field (int): The index of the field in self._fields
                plot_coords (resources.Coords): The coordinates of the plot in the field
                space_coords (resources.Coords): The coordinates of the space in the plot
        '''
        self._fields[field].get_plot(plot_coords).set_space(crop, space_coords)

    def set_crop_row(self, crop, field, plot_row, space_row):
        '''
        Sets the entire row in a field with a crop.

            Parameters:
                crop (Crop): The crop to place
                field (int): The index of the field in self._fields
                plot_row (int): Which row of plots to plant in
                space_row (int): Which row of spaces to plant in
        '''
        plots = self._fields[field].get_row(plot_row)
        for plot in plots.values():
            plot.set_row(crop, space_row)

    

    def sum_crops(self):
        '''
        Sums up the type of each crop in the field
        '''
        #field
        for field in self._fields.values():
            for plot_row_num in range(field.get_field_size()[0]):
                #plots
                plot_row = field.get_row(plot_row_num)
                for plot in plot_row.values():
                    for space_row_num in range(plot.get_plot_size()[0]):
                        space_row = plot.get_row(space_row_num)
                        for space in space_row.values():
                            if type(space) in self._crop_sums.keys():
                                self._crop_sums[type(space)] +=1
                            else:
                                self._crop_sums[type(space)] = 1
 
    
        
    

    