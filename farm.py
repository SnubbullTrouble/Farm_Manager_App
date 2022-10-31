from dataclasses import field
import logging
from resources import Singleton, Coords
from field import Field
from math import floor

class Farm(Singleton):
    def __init__(self):
        self._fields = {}

    def create_field(self, plot_type, num_rows, num_cols):
        '''
        Creates a field using the given arguments

            Parameters:
                plot_type (type): type of the plot for the field
                num_rows (int): number of plot rows in the field
                num_cols (int): number of plot columns in the field
        '''
        field = Field(plot_type, num_rows, num_cols)
        self._fields[len(self._fields)] = field

    def get_space_col_from_field_col(self, field_num, field_col):
        '''
        Converts field col into the plot col, space col

            Parameters: 
                field_num (int): field number
                field_col (int): the number of the col in the field scope

            Returns:
                [plot_col, space_col] (list<int,int>):  plot_col: index of the plot the space is int
                                                        space_col: col_num number of the col in the plot
        '''
        plot_type = self._fields[field_num].get_plot_type()
        num_plot_cols = plot_type().get_plot_size()[1]
        return [floor(field_col / num_plot_cols), field_col % num_plot_cols]

    def get_space_location_from_field_location(self, field_num, field_coords):
        '''
        Gets the exact plot location, space location of the space in the field

            Parameters:
                field_num (int): field number
                field_coords (Coords): row, and col of the space in the field

            Returns:
                [plot_coords, space_coords] (list<Coords,Coords>):  plot_coords: plot location in the field
                                                                    space_coords: space location in the plot
        '''
        row_dat = self.get_space_row_from_field_row(field_num, field_coords.row)
        col_dat = self.get_space_col_from_field_col(field_num, field_coords.col)
        return [Coords(row_dat[0], col_dat[0]), Coords(row_dat[1], col_dat[1])]

    def get_space_row_from_field_row(self, field_num, field_row):
        '''
        Converts field row into the plot row, space row

            Parameters: 
                field_num (int): field number
                field_row (int): the number of the row in the field scope

            Returns:
                [plot_num, row_num] (list<int,int>):    plot_num: index of the plot the space is int
                                                        row_num: row_num number of the row in the plot
        '''
        plot_type = self._fields[field_num].get_plot_type()
        num_plot_rows = plot_type().get_plot_size()[0]
        return [floor(field_row / num_plot_rows), field_row % num_plot_rows]

    def get_space(self, field_num, field_coords):
        '''
        Gets the crop in a single space given the location of the space

            Parameters:
                field_num (int): The index of the field in self._fields
                field_coords (resources.Coords): The coordinates of the space in the field

            Returns:
                space (Crop): the crop at the given location
        '''
        coords = self.get_space_location_from_field_location(field_num, Coords(field_coords.row, field_coords.col))
        plot_coords, space_coords = coords[0], coords[1]
        return self._fields[field_num].get_plot(plot_coords).get_space(space_coords)

    #sets a single space with a crop field
    def set_space(self, crop, field_num, field_coords):
        '''
        Sets a single space with a crop.

            Parameters:
                crop (Crop): The crop to place
                field_num (int): The index of the field in self._fields
                field_coords (resources.Coords): The coordinates of the space in the field
        '''
        coords = self.get_space_location_from_field_location(field_num, field_coords)
        plot_coords, space_coords = coords[0], coords[1]
        self._fields[field_num].get_plot(plot_coords).set_space(crop, space_coords)

    def set_crop_col(self, crop, field_num, field_col):
        '''
        Sets the entire column in a field with crop.

            Parameters:
                crop (Crop): The crop to place
                field_num (int): The index of the field in self._fields
                field_col (int): Which column of the field to plant in
        '''
        cols = self.get_space_col_from_field_col(field_num, field_col)
        plot_col, space_col = cols[0], cols[1]
        for row in range(self._fields[field_num].get_field_size()[0]):
            self._fields[field_num].get_plot(Coords(row, plot_col)).set_col(crop, space_col)

    def set_crop_row(self, crop, field_num, field_row):
        '''
        Sets the entire row in a field with a crop.

            Parameters:
                crop (Crop): The crop to place
                field_num (int): The index of the field in self._fields
                field_row (int): Which row of the field to plant in
        '''
        rows = self.get_space_row_from_field_row(field_num, field_row)
        plot_row, space_row = rows[0], rows[1]
        plots = self._fields[field_num].get_row(plot_row)
        for plot in plots.values():
            plot.set_row(crop, space_row)

    def sum_crops(self):
        '''
        Sums up the type of each crop in the field
        '''
        crop_sums = {}
        #field
        for field in self._fields.values():
            for plot_row_num in range(field.get_field_size()[0]):
                #plots
                plot_row = field.get_row(plot_row_num)
                for plot in plot_row.values():
                    for space_row_num in range(plot.get_plot_size()[0]):
                        space_row = plot.get_row(space_row_num)
                        for space in space_row.values():
                            if type(space) in crop_sums.keys():
                                crop_sums[type(space)] +=1
                            else:
                                crop_sums[type(space)] = 1
        return crop_sums

            
 
    
        
    

    