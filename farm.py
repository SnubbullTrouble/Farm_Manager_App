from dataclasses import field
import logging
from resources import Singleton
from field import Field
from plot import MediumPlot

class Farm():
    def __init__(self):
        self._fields = {0:Field()}

    def create_field(self, plot_type, num_rows, num_cols):
        new_key = len(self._fields)
        field = Field(plot_type, num_rows, num_cols)
        self._fields[len(self._fields)] = field

    #sets a single space with a crop field
    def set_crop(self, crop, field, plot_coords, space_coords):
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
 
        
    

    