import logging
from resources import Coords, FieldLog, FieldErrors
from plot import *

#collection of plots
class Field():
    def __init__(self, plot_type, num_rows, num_cols):
        '''
        Initializes the Field class.

            Parameters:
                plot_type (type): The plot type for the field
                num_rows (int): The number of rows in the field
                num_cols (int): The number of columns in the field
        '''
        self._plots = {0:{0: Plot()}}
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._plot_type = plot_type
        self._create_plots(self._plot_type)

    def _compare(self, field):
        '''
        Compares two fields to see if they are the same. (Debug only)

            Parameters:
                field (Field): A field to compare self to

            Returns:
                result (int):   0 if congruent
                                -1 if keys are different
                                -2 if values are different
        '''
        try:
            #all plot keys are in field
            for row in self._plots.keys():
                col = field._plots[row]
                #all plot col keys are in the field col
                for key in self._plots[row]:
                    val = col[key]
                    if type(val) != type(self._plots[row][key]):
                        raise ValueError
            #all field keys are in plots
            for row in field._plots.keys():
                col = self._plots[row]
                #all field col keys are in the plot col
                for key in field._plots[row]:
                    val = col[key]
                    if type(val) != type(field._plots[row][key]):
                        raise ValueError
            return 0
        except KeyError:
            return -1
        except ValueError:
            return -2

    #creates the plot using the number of rows and columns
    def _create_plots(self, plot_type):
        '''
        Creates all the plots in the field based on field size

        Parameters:
            plot_type (type): The type of Plot for the field
        '''
        self._plots = {}
        for row in range(self._num_rows):
            self._plots[row] = {}
            for col in range(self._num_cols):
                self._plots[row][col] = plot_type()

    #adds a column to each row
    def add_column(self):
        '''
        Adds a column to the field (One more plot for each row)

            Returns:
                new_key (int): The new column key
        '''
        self._num_cols += 1
        new_key = self._num_cols - 1
        for row in self._plots.keys():
            self._plots[row][new_key] = self._plot_type()
        logging.info("".join([FieldLog.new_col_added.value, str(new_key)]))
        return new_key

    #adds new row
    def add_row(self):
        '''
        Adds a row to the field

            Returns:
                new_key (int): The new row key
        '''
        self._num_rows += 1
        new_key = self._num_rows - 1
        self._plots[new_key] = {}
        logging.info("".join([FieldLog.new_row_added.value, str(new_key)]))
        for col in range(self._num_cols):
            self._plots[new_key][col] = self._plot_type()
            logging.info(FieldLog.set_col_to.value.format(str(new_key), str(self._plot_type)))
        return new_key

    #searches each row for an available plot. 
    def get_next_empty_plot(self):
        '''
        Gets the coordinates of the next empty plot

            Returns:
                coords (Coords):    Row, Column of the next empty plot
                                    -1 if there are not empty plots
        '''
        #check each row by key number
        for row in self._plots.keys():
            #check each column by key number
            for col in self._plots[row].keys():
                if self._plots[row][col].is_empty():
                    logging.info(FieldLog.next_empty_found.value.format(row, col))
                    return Coords(row, col)
            else:
                pass
        logging.error(FieldErrors.next_empty_msg.value)
        return -1

    #gets the plot at the specified coordinates
    def get_plot(self, coords):
        '''
        Returns the plot at the provided coordinates

            Parameters:
                coords (Coords): Row, Col of the desired plot

            Returns:
                plot (Plot): Plot at location Row, Col
        '''
        return self._plots[coords.row][coords.col]

    #gets all the plots in a row
    def get_row(self, row):
        '''
        Returns the row of plots from row number

            Parameters:
                row (int): Row number

            Returns:
                plots (dict(Plot)): Dictionary of plots (integer keys)
        '''
        return self._plots[row]

    #sets the plot at the location provided, if coords not provided, place at the 
    #next available plot
    def _set_plot(self, plot, coords = None):
        '''
        Sets the plot at the provided coordinates (Debug Only)

            Parameters:
                plot (Plot): Plot to be used
                coords (Coords) : Row, Col of the desired plot
        '''
        #if initializing an empty plot
        if coords is None:
            next_avail = self.get_next_empty_plot()
            if next_avail != -1:
                self._plots[next_avail.row][next_avail.col] = plot
                logging.info(FieldLog.new_plot_added.value.format(str(type(plot)), 
                    next_avail.row, next_avail.col))
            else:
                pass
        else:
            self._plots[coords.row][coords.col] = plot
            logging.info(FieldLog.new_plot_added.value.format(str(type(plot)), 
               coords.row, coords.col))

