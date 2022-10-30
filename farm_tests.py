from crop import Reserved
from farm import *
import unittest
from testing_resources import TestCrop
from plot import LargePlot, MediumPlot, Plot, SmallPlot

class Test_Farm(unittest.TestCase):

    def test_intialization(self):
        farm = Farm()
        farm.create_field(type(SmallPlot()), 3, 2)
        self.assertTrue(farm._fields[0].get_field_size()[0] == 3)
        self.assertTrue(farm._fields[0].get_field_size()[1] == 2)

        farm = Farm()
        farm.create_field(type(MediumPlot()), 3, 3)
        self.assertIn(0, farm._fields.keys())
        self.assertNotIn(1, farm._fields.keys())
        farm.create_field(type(LargePlot()), 2, 1)
        self.assertIn(0, farm._fields.keys())
        self.assertIn(1, farm._fields.keys())
        self.assertTrue(farm._fields[1].get_field_size()[0] == 2)
        self.assertTrue(farm._fields[1].get_field_size()[1] == 1)

    def test_get_space(self):
        farm = Farm()
        farm.create_field(type(SmallPlot()), 3, 3)
        farm._fields[0]._plots[0][2]._spaces[0][1] = TestCrop()
        space = farm.get_space(0, Coords(0, 2), Coords(0, 1))
        self.assertTrue(type(space) == type(TestCrop()))
        space = farm.get_space(0, Coords(0, 2), Coords(0, 2))
        self.assertTrue(type(space) == type(Reserved())) 

        farm = Farm()
        farm.create_field(type(SmallPlot()), 2, 3)
        farm._fields[0]._plots[1][2].set_row(TestCrop(), 2)
        space = farm.get_space(0, Coords(1, 2), Coords(2, 1))
        self.assertTrue(type(space) == type(TestCrop()))
        space = farm.get_space(0, Coords(1, 2), Coords(2, 0))
        self.assertTrue(type(space) == type(Reserved())) 

        farm = Farm()
        farm.create_field(type(MediumPlot()), 3, 1)
        farm._fields[0]._plots[1][0].set_row(TestCrop(), 1)
        space = farm.get_space(0, Coords(1, 0), Coords(1, 0))
        self.assertTrue(type(space) == type(TestCrop()))
        space = farm.get_space(0, Coords(1, 0), Coords(1, 1))
        self.assertTrue(type(space) == type(Reserved()))
        space = farm.get_space(0, Coords(1, 0), Coords(1, 2))
        self.assertTrue(type(space) == type(TestCrop()))

        farm = Farm()
        farm.create_field(type(LargePlot()), 1, 1)
        space1 = farm.get_space(0, Coords(0, 0), Coords(2, 1))
        space2 = farm.get_space(0, Coords(0, 0), Coords(2, 2))
        self.assertTrue(space1 != space2)

    def test_get_space_location_from_field_row(self):
        farm = Farm()
        farm.create_field(type(SmallPlot()), 3, 3)
        farm._fields[0]._plots[0][0].set_row(TestCrop(), 0)
        farm._fields[0]._plots[0][2].set_row(Reserved(), 0)
        space_loc = farm.get_space_location_from_field_row(0, 0)
        plot_row_num, space_row_num = space_loc[0], space_loc[1]
        space = farm.get_space(0, Coords(plot_row_num, 0), Coords(space_row_num, 1))
        self.assertTrue(type(space) == type(TestCrop()))
        space = farm.get_space(0, Coords(plot_row_num, 1), Coords(space_row_num, 1))
        self.assertTrue(type(space) == type(None))
        space = farm.get_space(0, Coords(plot_row_num, 2), Coords(space_row_num, 1))
        self.assertTrue(type(space) == type(Reserved()))

        farm = Farm()
        farm.create_field(type(MediumPlot()), 3, 1)
        farm._fields[0]._plots[1][0].set_row(TestCrop(), 0)
        farm._fields[0]._plots[2][0].set_row(Reserved(), 2)
        space_loc = farm.get_space_location_from_field_row(0, 3)
        plot_row_num, space_row_num = space_loc[0], space_loc[1]
        space = farm.get_space(0, Coords(plot_row_num, 0), Coords(space_row_num, 0))
        self.assertTrue(type(space) == type(TestCrop()))
        space_loc = farm.get_space_location_from_field_row(0, 8)
        plot_row_num, space_row_num = space_loc[0], space_loc[1]
        space = farm.get_space(0, Coords(plot_row_num, 0), Coords(space_row_num, 0))
        self.assertTrue(type(space) == type(Reserved()))

    def test_set_space(self):
        farm = Farm()
        farm.create_field(type(MediumPlot()), 3, 3)
        plot_cords, space_coords = Coords(2, 2), Coords(2, 2)
        farm.set_space(TestCrop(), 0, plot_cords, space_coords)
        self.assertTrue(type(farm.get_space( 0, plot_cords, space_coords)) == type(TestCrop()))

        farm = Farm()
        farm.create_field(type(LargePlot()), 1, 3)
        plot_cords, space_coords = Coords(0, 2), Coords(2, 1)
        farm.set_space(TestCrop(), 0, plot_cords, space_coords)
        self.assertTrue(type(farm.get_space(0, plot_cords, space_coords)) == type(TestCrop()))

    def test_set_crop_row(self):
        return
        farm = Farm()
        farm.create_field(type(SmallPlot()), 3, 3)
        farm.set_crop_row(TestCrop(), 0, )


    def test_singleton(self):
        farm1 = Farm()
        farm2 = Farm()
        self.assertTrue(farm1 == farm2)

if __name__ == '__main__':
    unittest.main()