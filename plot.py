from abc import ABC
import logging
from resources import Coords, PlotLog, PlotErrors
from farm_exceptions import DataException, PlotException
from crop import Crop, Reserved

#one square of a field. essentially a sprinkler and the area it covers
class Plot(ABC):
    def __init__(self) -> None:
        '''
        Initializes the plot class
        '''
        self._num_rows = None
        self._num_cols = None
        self._spaces = {0: {}}
        self._reserved_spaces = []
        self.empty = True

    #compares two plots returns 0 if equivalent
    def compare(self, plot_spaces: dict) -> int:
        '''
        Compares two plots to see if they have all the same values. (Debug only)

            Parameters:
                plot (Plot): A field to compare self to

            Returns:
                result (int):   0 if congruent\n
                                -1 if keys are different\n
                                -2 if values are different
        '''
        try:
            #all space keys are in plot
            for row in self._spaces.keys():
                col = plot_spaces[row]
                #all space col keys are in the plot col
                for key in self._spaces[row]:
                    val = col[key]
                    if type(val) != type(self._spaces[row][key]):
                        raise ValueError
            #all plot keys are in space
            for row in plot_spaces.keys():
                col = self._spaces[row]
                #all plot col keys are in the space col
                for key in plot_spaces[row]:
                    val = col[key]
                    if type(val) != type(plot_spaces[row][key]):
                        raise ValueError
            return 0
        except KeyError:
            return -1
        except ValueError:
            return -2

    #empties the plot of all crops. skips initialized reserved spaces
    def clear_plot(self) -> None:
        '''
        Clears the entire plot of all crop types. Skips reserved spaces.
        '''
        #for all items in the plot
        for row in self._spaces.keys():
            for col in self._spaces[row].keys():
                coords = Coords(row, col)
                if type(self.get_space(coords)) == type(Reserved()):
                    if not self.is_default_reserved(coords):
                        logging.info(PlotLog.reserve_skipped.value.format(coords.row, coords.col))
                    else:
                        pass
                else:
                    self.clear_space(coords)

    #clears the crop at the given plot space. throws an error if the space is 
    #an initialized reserve space (no-touchy)
    def clear_space(self, coords: Coords) -> None:
        '''
        Clears the space at the given coordinates.

            Parameters:
                coords (Coords): Coordinates of the space to clear
        '''
        #if the space is reserved....
        if type(self.get_space(coords)) == type(Reserved()):
            logging.error(PlotLog.reserve_skipped.value.format(coords.row, coords.col))
            raise PlotException(PlotErrors.is_reserved_space.value.format(coords.row, coords.col))
        else:
            self.set_space(None, coords)

    #creates the dictionary structure that holds all the plot spaces
    def _create_spaces(self) -> None:
        '''
        Creates the data structure that holds the crop data.
        '''
        logging.info(PlotLog.creating_plot.value)
        for row in range(self._num_rows):
            self._spaces[row] = {}
            for col in range(self._num_cols):
                self._spaces[row][col] = None

    def get_plot_size(self) -> list:
        '''
        Returns the plot size

            Returns:
                [num_rows, num_cols] (list<int,int>): tuple of the number of rows and columns
        '''
        return [self._num_rows, self._num_cols]

    #returns row number as a list (starts at 0)
    def get_row(self, row_number: int) -> dict:
        '''
        Gets the set of spaces of the plot in the specified row.

            Parameters:
                row_number (int): Index of the desired row number

            Returns:
                row (dict): The row of crops at the given row number
        '''
        return self._spaces[row_number]

    #returns the item in the given space (starts at 0)
    def get_space(self, coords: Coords) -> Crop:
        '''
        Gets the space at the specified plot coordinates.

            Parameters:
                coords (Coords): coordinates of the space

            Returns:
                crop (Crop): crop at the specificed location
        '''
        return self._spaces[coords.row][coords.col]
        
    #places a reserved "crop" in each reserved location
    def _initialize_reserved_spaces(self) -> None:
        '''
        Initializes reserved spaces in the plot.
        '''
        for coord in self._reserved_spaces:
            self.set_space(Reserved(), Coords(coord.row, coord.col))

    #checks if a space an initialized reserved space
    def is_default_reserved(self, coords: Coords) -> bool:
        '''
        Checks whether the space at the specified coordinates is reserved.

            Parameters:
                coords (Coords): coordinates of the space

            Returns:
                isReserved (bool): True if reserved, False if not
        '''
        for coord in self._reserved_spaces:
            if coord.compare(coords):
                return True
        return False

    #returns boolean based on if all spaces in the plot are None
    def is_empty(self, skip_reserved: bool = True) -> bool:
        '''
        Checks to see whether any crops are in the plot. The plot is empty if 
        all spaces are None. Ignores reserved spaces by default.

            Parameters:
                skip_reserved (bool): sets the flag to skip reserved spaces (True by default)

            Returns:
                isEmpty (bool): True if empty, False if non-empty
        '''
        for row in self._spaces:
            for col in self._spaces[row].keys():
                if self._spaces[row][col] is not None:
                    #if we aren't skipping reserved spaces
                    if not skip_reserved:
                        return False
                    #if we're ignoring reserved spaces and it's not reserved
                    elif type(self._spaces[row][col]) != type(Reserved()):
                        return False
                    #if it's reserved
                    else:
                        pass

                else:
                    pass
        return True

    def set_col(self, crop: Crop, col: int) -> None:
        '''
        Sets each space of a column with the specified crop.

            Parameters:
                crop (Crop): crop to place in each space
                col (int): column to plant in
        '''
        for row in self._spaces.keys():
            if type(self.get_space(Coords(row, col))) is not type(Reserved()):
                self.set_space(crop, Coords(row, col))
            else:
                logging.info(PlotLog.space_skipped.value)

    #sets each space in the row to crop, skipping reserved spaces
    def set_row(self, crop: Crop, row: int) -> None:
        '''
        Sets each space of a row with the specified crop.

            Parameters:
                crop (Crop): crop to place in each space
                row (int): row to plant in
        '''
        for space in self._spaces[row].keys():
            if type(self.get_space(Coords(row, space))) is not type(Reserved()):
                self.set_space(crop, Coords(row, space))
            else:
                logging.info(PlotLog.space_skipped.value)

    #puts a crop in the given space (starts at 0) if the space is not reserved
    def set_space(self, crop: Crop, coords: Coords) -> None:
        '''
        Sets the space at the coordinates to the specified crop.

            Paramters:
                crop (Crop): crop to place at the coordinates
                coords (Coords): coordinates of the space
        '''
        if type(self.get_space(coords)) != type(Reserved()):
            self._spaces[coords.row][coords.col] = crop
            logging.info(PlotLog.space_set.value.format(str(type(crop)), coords.row, coords.col))
        else:
            logging.error(PlotErrors.is_reserved_space.value.format(coords.row, 
                coords.col))
            raise PlotException(PlotErrors.is_reserved_space.value.format(coords.row, 
                coords.col))

#5x5 plots (24 empty spaces)
class LargePlot(Plot):
    def __init__(self) -> None:
        super().__init__()
        self._num_rows = 5
        self._num_cols = 5
        self._spaces = {}
        self._reserved_spaces = [Coords(2, 2)]
        self._create_spaces()
        self._initialize_reserved_spaces()

#3x3 plots (8 empty spaces)
class MediumPlot(Plot):
    def __init__(self) -> None:
        super().__init__()
        self._num_rows = 3
        self._num_cols = 3
        self._spaces = {}
        self._reserved_spaces = [Coords(1, 1)]
        self._create_spaces()
        self._initialize_reserved_spaces()

#3x3 plots (4 empty spaces)
class SmallPlot(Plot):
    def __init__(self) -> None:
        super().__init__()
        self._num_rows = 3
        self._num_cols = 3
        self._spaces = {}
        self._reserved_spaces = [Coords(0, 0), Coords(0, 2), 
            Coords(1, 1), Coords(2, 0), Coords(2, 2)]
        self._create_spaces()
        self._initialize_reserved_spaces()

