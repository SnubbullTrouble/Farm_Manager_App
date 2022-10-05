from resources import GeneralMessages

class DataException(Exception):
    def __init__(self, message = None):
        self.message = GeneralMessages.no_data_provided.value if message is None else message
        super().__init__(self.message)

class PlotException(Exception):
    def __init__(self, message = None):
        self.message = GeneralMessages.no_data_provided.value if message is None else message
        super().__init__(self.message)