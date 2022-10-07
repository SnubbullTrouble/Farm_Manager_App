from dataclasses import field
import unittest

from pkg_resources import get_platform

from field import Field
from plot import *
from testing_resources import TestCrop, TestField

class Test_Field(unittest.TestCase):

    def test_compare(self):
        field1, field2 = (Field(type(SmallPlot()), 3, 3), 
            Field(type(SmallPlot()), 3, 3))
        self.assertTrue(field1._compare(field2) == 0)

        field1, field2 = (Field(type(SmallPlot()), 3, 3), 
            Field(type(MediumPlot()), 3, 3))
        self.assertTrue(field1._compare(field2) == -2)

        field1, field2 = (Field(type(LargePlot()), 3, 3), 
            Field(type(LargePlot()), 3, 3))
        self.assertTrue(field1._compare(field2) == 0)

        field1, field2 = (Field(type(LargePlot()), 3, 3), 
            Field(type(MediumPlot()), 3, 3))
        self.assertTrue(field1._compare(field2) == -2)

        field1, field2 = (Field(type(MediumPlot()), 5, 5), 
            Field(type(MediumPlot()), 3, 3))
        self.assertTrue(field1._compare(field2) == -1)

        field1, field2 = (Field(type(MediumPlot()), 5, 2), 
            Field(type(MediumPlot()), 2, 5))
        self.assertTrue(field1._compare(field2) == -1)

    def test_instantiation(self):
        field1, field2 = Field(type(SmallPlot()), 3, 3), TestField()
        field2._plots = {0: {0: SmallPlot(), 1: SmallPlot(), 2: SmallPlot()},
                1: {0: SmallPlot(), 1: SmallPlot(), 2: SmallPlot()},
                2: {0: SmallPlot(), 1: SmallPlot(), 2: SmallPlot()}}
        self.assertTrue(field1._compare(field2) == 0)

        field1, field2 = Field(type(MediumPlot()), 3, 3), TestField()
        field2._plots = {0: {0: MediumPlot(), 1: MediumPlot(), 2: MediumPlot()},
                1: {0: MediumPlot(), 1: MediumPlot(), 2: MediumPlot()},
                2: {0: MediumPlot(), 1: MediumPlot(), 2: MediumPlot()}}
        self.assertTrue(field1._compare(field2) == 0)

        field1, field2 = Field(type(MediumPlot()), 1, 1), TestField()
        field2._plots = {0: {0: MediumPlot()}}
        self.assertTrue(field1._compare(field2) == 0)
        
        field1, field2 = Field(type(LargePlot()), 1, 3), TestField()
        field2._plots = {0: {0: LargePlot(), 1: LargePlot(), 2: LargePlot()}}
        self.assertTrue(field1._compare(field2) == 0)

        field1, field2 = Field(type(MediumPlot()), 2, 1), TestField()
        field2._plots = {0: {0: MediumPlot()},
                1: {0: MediumPlot()}}
        self.assertTrue(field1._compare(field2) == 0)

    def test_get_plot(self):
        field1 = Field(type(SmallPlot()), 1, 2)
        self.assertTrue(field1.get_plot(Coords(0,1)).compare(field1._plots[0][1]) == 0)
        self.assertTrue(field1.get_plot(Coords(0, 1)) == field1.get_plot(Coords(0, 1)))
        self.assertFalse(field1.get_plot(Coords(0, 1)) == field1.get_plot(Coords(0, 0)))

    def test_add_row(self):
        field1, field2 = Field(type(SmallPlot()), 2, 2), TestField()
        field2._plots = {0: {0: SmallPlot(), 1: SmallPlot()},
                1: {0: SmallPlot(), 1: SmallPlot()},
                2: {0: SmallPlot(), 1: SmallPlot()}}
        field1.add_row()
        self.assertTrue(field1._num_rows == 3)
        self.assertTrue(field1._compare(field2) == 0)

        field1, field2 = Field(type(MediumPlot()), 2, 3), TestField()
        field2._plots = {0: {0: MediumPlot(), 1: MediumPlot(), 2: MediumPlot()},
                1: {0: MediumPlot(), 1: MediumPlot(), 2: MediumPlot()},
                2: {0: MediumPlot(), 1: MediumPlot(), 2: MediumPlot()}}
        field1.add_row()
        self.assertTrue(field1._num_rows == 3)
        self.assertTrue(field1._compare(field2) == 0)

        field1, field2 = Field(type(LargePlot()), 1, 1), TestField()
        field2._plots = {0: {0: LargePlot()},
                1: {0: LargePlot()}}
        field1.add_row()
        self.assertTrue(field1._num_rows == 2)
        self.assertTrue(field1._compare(field2) == 0)

    def test_add_column(self):
        field1, field2 = Field(type(SmallPlot()), 2, 2), TestField()
        field2._plots = {0: {0: SmallPlot(), 1: SmallPlot(), 2: SmallPlot()},
                1: {0: SmallPlot(), 1: SmallPlot(), 2: SmallPlot()}}
        field1.add_column()
        self.assertTrue(field1._num_cols == 3)
        self.assertTrue(field1._compare(field2) == 0)

        field1, field2 = Field(type(MediumPlot()), 2, 3), TestField()
        field2._plots = {0: {0: MediumPlot(), 1: MediumPlot(), 2: MediumPlot(), 3: MediumPlot()},
                1: {0: MediumPlot(), 1: MediumPlot(), 2: MediumPlot(), 3: MediumPlot()}}
        field1.add_column()
        self.assertTrue(field1._num_cols == 4)
        self.assertTrue(field1._compare(field2) == 0)

        field1, field2 = Field(type(LargePlot()), 1, 1), TestField()
        field2._plots = {0: {0: LargePlot(), 1: LargePlot()}}
        field1.add_column()
        self.assertTrue(field1._num_cols == 2)
        self.assertTrue(field1._compare(field2) == 0)

    def test_next_empty(self):
        field1 = Field(type(SmallPlot()), 1, 3)
        nonempty_plot = field1.get_plot(Coords(0, 0))
        self.assertTrue(nonempty_plot.is_empty() == True)
        nonempty_plot.set_row(TestCrop(), 1)
        self.assertFalse(nonempty_plot.is_empty() == True)
        empty_plot_coords = field1.get_next_empty_plot()
        self.assertTrue(empty_plot_coords.compare(Coords(0, 1)) == True)

        field1 = Field(type(MediumPlot()), 2, 3)
        for plot in field1._plots[0].values():
            plot.set_row(TestCrop(), 2)
        empty_plot_coords = field1.get_next_empty_plot()
        self.assertTrue(empty_plot_coords.compare(Coords(1, 0)) == True)

    def test_get_row(self):
        field1 = Field(type(LargePlot()), 1, 1)
        row = field1.get_row(0)
        self.assertTrue(row[0] == field1.get_plot(Coords(0, 0)))

        field1 = Field(type(MediumPlot()), 3, 3)
        p1, p2, p3 = field1.get_plot(Coords(1, 0)), field1.get_plot(Coords(1, 1)), field1.get_plot(Coords(1, 2))
        p1.set_row(TestCrop(), 0)
        p2.set_row(TestCrop(), 1)
        p3.set_row(TestCrop(), 2)
        row = field1.get_row(1)
        self.assertTrue(type(row[0].get_space(Coords(0, 0)) == type(TestCrop())))
        self.assertTrue(type(row[1].get_space(Coords(1, 1)) == type(TestCrop())))
        self.assertTrue(type(row[2].get_space(Coords(2, 2)) == type(TestCrop())))

    def test_set_plot(self):
        #TODO test param None vs Coords
        pass

    def test_get_size(self):
        #TODO implement
        pass

if __name__ == '__main__':
    unittest.main()