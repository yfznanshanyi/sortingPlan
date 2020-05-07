from constData import CONSTDATA
from coordinate import COORDINATE


class SORTINGSATION(object):
    def __init__(self, coordinate, index):
        self.coordinate = coordinate
        self.index = index


class SORTINGSATIONSET(object):
    def __init__(self):
        self.sorting_sations = []
        self.short_side_index = []
        self.long_side_index = []
        self.set_sorting_sations()

    def set_sorting_sations(self):
        # short side
        for i in range(CONSTDATA.short_side_sorting_sation_num):
            x = CONSTDATA.sorting_sation_short_side_end_coordinate.x - i * CONSTDATA.short_side_width_between_sorting_sations
            y = CONSTDATA.sorting_sation_short_side_end_coordinate.y
            index = i
            self.sorting_sations.append(SORTINGSATION(COORDINATE(x, y), index))
            self.short_side_index.append(index)
        # long side
        for i in range(CONSTDATA.long_side_sorting_sation_num):
            x = CONSTDATA.sorting_sation_long_side_end_coordinate.x - i * CONSTDATA.long_side_width_between_sorting_sations
            y = CONSTDATA.sorting_sation_long_side_end_coordinate.y
            index = i + CONSTDATA.short_side_sorting_sation_num
            self.sorting_sations.append(SORTINGSATION(COORDINATE(x, y), index))
            self.long_side_index.append(index)
