from enum import Enum

#row, column pair for interfacing with plot and field collections
class Coords():
    def __init__(self, row, col):
        self.row = row
        self.col = col

    #returns true if the two are the same
    def compare(self, coords):
        return True if coords.row == self.row and coords.col == self.col else False

class Singleton():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

class FieldErrors(Enum):
    next_empty_msg = "Unable to find next empty plot."
    max_rows_reached = """Maximum number of rows reached. Raise the 
        maximum number of rows in the field to add a new row."""
    max_cols_reached = """Maximum number of columns reached. Raise the  
        maximum number of rows in the field to add a new column."""

class FieldLog(Enum):
    creating_field = "Creating new field."
    new_row_added = "Created a new row. Row number:"
    next_empty_found = "Found next empty plot at: Row {0}, Col {1}"
    next_empty_is = "Next Empty plot is at: Row {0}, Col {1}"
    new_plot_added = "New {0} plot added at: Row {1}, Col {2}"
    new_col_added = "Created a new column. Col number:"
    plot_cleared = "Plot spaces cleared"
    set_col_to = "Set column Col:{0} to {1}"
    set_plot = "Setting plot to {0}"

class GeneralMessages(Enum):
    no_data_provided = "<No data provided>"

class PlotErrors(Enum):
    is_reserved_space = "Row {0}, Col {1} is a reserved space."
    space_data_error = "Invalid number of items in space Row {0}, Col {1}"

class PlotLog(Enum):
    creating_plot = "Creating new plot."
    space_cleared = "Space at Row {0}, Col {1} cleared."
    space_set = "{0} space set at Row {1}, Col {2}"
    space_skipped = "Space at Row {0}, Col {1} skipped."
    reserve_skipped = "Reserve space at Row {0}, Col {1} skipped."