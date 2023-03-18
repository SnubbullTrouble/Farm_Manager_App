from cgitb import small
import unittest
from plot import *
from testing_resources import TestCrop

class Test_Plot(unittest.TestCase):
    
    def test_compare(self):
        p1, p2 = SmallPlot(), SmallPlot()
        self.assertTrue(p1.compare(p2._spaces) == 0)

        p1, p2 = MediumPlot(), MediumPlot()
        self.assertTrue(p1.compare(p2._spaces) == 0)

        p1, p2 = LargePlot(), LargePlot()
        self.assertTrue(p1.compare(p2._spaces) == 0)

        p1, p2 = SmallPlot(), MediumPlot()
        self.assertTrue(p1.compare(p2._spaces) == -2)

        p1, p2 = SmallPlot(), LargePlot()
        self.assertTrue(p1.compare(p2._spaces) == -2)

        p1, p2 = MediumPlot(), LargePlot()
        self.assertTrue(p1.compare(p2._spaces) == -2)

        p1, p2 = SmallPlot(), SmallPlot()
        self.assertTrue(p1.compare(p2._spaces) == 0)
        p1.set_space(TestCrop(), Coords(0, 1))
        self.assertFalse(p1.compare(p2._spaces) == 0)

    def test_set_space(self):
        p1 = SmallPlot()
        self.assertRaises(PlotException, p1.set_space, Reserved(), Coords(0,0))

        p1 = MediumPlot()
        coords = Coords(0,2)
        p1.set_space(TestCrop(), coords)
        self.assertTrue(type(p1.get_space(coords)) == type(TestCrop()))
        coords = Coords(0,2)
        p1.set_space(TestCrop(), coords)
        self.assertTrue(type(p1.get_space(coords)) == type(TestCrop()))
        
        p1 = MediumPlot()
        coords = Coords(0,1)
        p1.set_space(TestCrop(), coords)
        self.assertTrue(type(p1.get_space(coords)) == type(TestCrop()))
        coords = Coords(0,2)
        p1.set_space(TestCrop(), coords)
        self.assertTrue(type(p1.get_space(coords)) == type(TestCrop()))
        self.assertFalse(p1._spaces[0][1] == p1._spaces[0][2])

    def test_set_row(self):
        p1 = SmallPlot()
        p1.set_row(Reserved(), 0)
        self.assertTrue(type(p1.get_space(Coords(0,1))) == type(Reserved()))

        #TODO:swap test crop with an actual crop
        p1 = SmallPlot()
        p1.set_row(TestCrop(), 0)
        self.assertTrue(type(p1.get_space(Coords(0,1))) == type(TestCrop()))
    
        p1 = MediumPlot()
        row = 0
        p1.set_row(TestCrop(), row)
        self.assertTrue(type(p1.get_space(Coords(row,0))) == type(TestCrop()))
        self.assertTrue(type(p1.get_space(Coords(row,1))) == type(TestCrop()))
        self.assertTrue(type(p1.get_space(Coords(row,2))) == type(TestCrop()))
        
        p1 = MediumPlot()
        row = 2
        p1.set_row(TestCrop(), row)
        self.assertTrue(type(p1.get_space(Coords(row,0))) == type(TestCrop()))
        self.assertTrue(type(p1.get_space(Coords(row,1))) == type(TestCrop()))
        self.assertTrue(type(p1.get_space(Coords(row,2))) == type(TestCrop()))
        
        #TODO: add more testing when crops are added

    def test_instantiation(self):
        p1, p2 = SmallPlot(), SmallPlot()
        self.assertFalse(p1 == p2)
        self.assertTrue(p1.compare(p2._spaces) == 0)
        p3 = SmallPlot()
        p3._spaces = {0: {0: Reserved(), 1: None, 2: Reserved()},
                    1: {0: None, 1: Reserved(), 2: None},
                    2: {0: Reserved(), 1: None, 2: Reserved()}}
        self.assertTrue(p1.compare(p3._spaces) == 0)
        self.assertTrue(p2.compare(p3._spaces) == 0)

        p1, p2 = MediumPlot(), MediumPlot()
        self.assertFalse(p1 == p2)
        self.assertTrue(p1.compare(p2._spaces) == 0)
        p3 = MediumPlot()
        p3._spaces = {0: {0: None, 1: None, 2: None,},
                    1: {0: None, 1: Reserved(), 2:None},
                    2: {0: None, 1: None, 2: None}}
        self.assertTrue(p1.compare(p3._spaces) == 0)
        self.assertTrue(p2.compare(p3._spaces) == 0)

        p1, p2 = LargePlot(), LargePlot()
        self.assertFalse(p1 == p2)
        self.assertTrue(p1.compare(p2._spaces) == 0)
        p3 = LargePlot()
        p3._spaces = {0: {0: None, 1: None, 2: None, 3: None, 4: None},
                    1: {0: None, 1: None, 2: None, 3: None, 4: None},
                    2: {0: None, 1: None, 2: Reserved(), 3: None, 4: None},
                    3: {0: None, 1: None, 2: None, 3: None, 4: None},
                    4: {0: None, 1: None, 2: None, 3: None, 4: None}}
        self.assertTrue(p1.compare(p3._spaces) == 0)
        self.assertTrue(p2.compare(p3._spaces) == 0)

    def test_is_empty(self):
        p1 = SmallPlot()
        self.assertTrue(p1.is_empty() == True)
        self.assertFalse(p1.is_empty(False) == True)

        p1 = SmallPlot()
        p1.set_space(TestCrop(), Coords(0, 1))
        self.assertTrue(p1.is_empty() == False)
        self.assertTrue(p1.is_empty(False) == False)
        p1.set_space(None, Coords(0, 1))
        self.assertTrue(p1.is_empty() == True)
        self.assertFalse(p1.is_empty(False) == True)

        p1 = MediumPlot()
        self.assertTrue(p1.is_empty() == True)
        self.assertFalse(p1.is_empty(False) == True)

        p1 = MediumPlot()
        p1.set_space(Reserved(), Coords(2, 2))
        self.assertTrue(p1.is_empty() == True)
        self.assertFalse(p1.is_empty(False) == True)
        p1.set_space(TestCrop(), Coords(0, 2))
        self.assertTrue(p1.is_empty() == False)
        self.assertTrue(p1.is_empty(False) == False)

        p1 = LargePlot()
        self.assertTrue(p1.is_empty() == True)
        self.assertFalse(p1.is_empty(False) == True)
        p1.set_row(TestCrop(), 2)
        self.assertTrue(p1.is_empty() == False)
        self.assertTrue(p1.is_empty(False) == False)
        p1.set_row(None, 2)
        self.assertTrue(p1.is_empty() == True)
        self.assertFalse(p1.is_empty(False) == True)

    def test_clear_space(self):
        p1 = SmallPlot()
        coords = Coords(1, 1)
        self.assertTrue(type(p1.get_space(coords)) == type(Reserved()))
        self.assertRaises(PlotException, p1.clear_space, coords)

        p1 = SmallPlot()
        coords = Coords(0, 1)
        self.assertTrue(type(p1.get_space(coords)) == type(None))
        p1.set_space(Reserved(), coords)
        self.assertTrue(type(p1.get_space(coords)) == type(Reserved()))
        self.assertRaises(PlotException, p1.clear_space, coords)

        p1 = MediumPlot()
        coords = Coords(2, 2)
        self.assertTrue(p1.is_empty() == True)
        p1.set_space(TestCrop(), coords)
        self.assertFalse(p1.is_empty() == True)
        p1.clear_space(coords)
        self.assertTrue(p1.is_empty() == True)

        p1 = LargePlot()
        self.assertTrue(p1.is_empty() == True)
        p1.set_row(TestCrop(), 2)
        self.assertFalse(p1.is_empty() == True)
        coords = Coords(2, 0)
        next_cords = Coords(2, 1)
        self.assertTrue(type(p1.get_space(coords)) == type(TestCrop()))
        p1.clear_space(coords)
        self.assertTrue(type(p1.get_space(coords)) == type(None))
        self.assertTrue(type(p1.get_space(next_cords)) == type(TestCrop()))
        coords = Coords(2, 1)
        next_cords = Coords(2, 2)
        p1.clear_space(coords)
        self.assertTrue(type(p1.get_space(coords)) == type(None))
        self.assertTrue(type(p1.get_space(next_cords)) == type(Reserved()))
        #skip reserved space
        coords = Coords(2, 3)
        next_cords = Coords(2, 4)
        p1.clear_space(coords)
        self.assertTrue(type(p1.get_space(coords)) == type(None))
        self.assertTrue(type(p1.get_space(next_cords)) == type(TestCrop()))
        coords = Coords(2, 4)
        p1.clear_space(coords)
        self.assertTrue(type(p1.get_space(coords)) == type(None))
        self.assertTrue(p1.is_empty() == True)

    def test_clear_plot(self):
        p1 = SmallPlot()
        self.assertTrue(p1.is_empty() == True)
        p1.clear_plot()
        self.assertTrue(p1.is_empty() == True)

        p1 = SmallPlot()
        p1.set_space(TestCrop(), Coords(0,1))
        self.assertTrue(p1.is_empty() == False)
        p1.clear_plot()
        self.assertFalse(p1.is_empty() == False)

        p1 = MediumPlot()
        p1.set_row(Reserved(), 0)
        self.assertTrue(p1.is_empty() == True)
        p1.set_space(TestCrop(), Coords(2, 0))
        self.assertFalse(p1.is_empty() == True)
        p1.clear_plot()
        self.assertTrue(p1.is_empty() == True)

        p1 = LargePlot()
        self.assertTrue(p1.is_empty() == True)
        p1.set_row(TestCrop(), 1)
        self.assertFalse(p1.is_empty() == True)
        p1.clear_plot()  
        self.assertTrue(p1.is_empty() == True)      

    def test_set_col(self):
        p1 = SmallPlot()
        p1.set_col(TestCrop(), 1)
        self.assertTrue(type(p1.get_space(Coords(0, 0))) == type(Reserved()))
        self.assertTrue(type(p1.get_space(Coords(0, 1))) == type(TestCrop()))
        self.assertTrue(type(p1.get_space(Coords(0, 2))) == type(Reserved()))
        self.assertTrue(type(p1.get_space(Coords(1, 0))) == type(None))
        self.assertTrue(type(p1.get_space(Coords(1, 1))) == type(Reserved()))
        self.assertTrue(type(p1.get_space(Coords(1, 2))) == type(None))
        self.assertTrue(type(p1.get_space(Coords(2, 0))) == type(Reserved()))
        self.assertTrue(type(p1.get_space(Coords(2, 1))) == type(TestCrop()))
        self.assertTrue(type(p1.get_space(Coords(2, 2))) == type(Reserved()))

        p1 = MediumPlot()
        p1.set_col(TestCrop(), 2)
        self.assertTrue(type(p1.get_space(Coords(0, 0))) == type(None))
        self.assertTrue(type(p1.get_space(Coords(0, 1))) == type(None))
        self.assertTrue(type(p1.get_space(Coords(0, 2))) == type(TestCrop()))
        self.assertTrue(type(p1.get_space(Coords(1, 0))) == type(None))
        self.assertTrue(type(p1.get_space(Coords(1, 1))) == type(Reserved()))
        self.assertTrue(type(p1.get_space(Coords(1, 2))) == type(TestCrop()))
        self.assertTrue(type(p1.get_space(Coords(2, 0))) == type(None))
        self.assertTrue(type(p1.get_space(Coords(2, 1))) == type(None))
        self.assertTrue(type(p1.get_space(Coords(2, 2))) == type(TestCrop()))

if __name__ == '__main__':
    unittest.main()