from constData import CONSTDATA
from coordinate import COORDINATE


class STORAGEAREA(object):
    def __init__(self, coordinate, index):
        self.coordinate = coordinate
        self.index = index


class STORAGEAREASET(object):
    def __init__(self):
        self.storage_areas = []
        self.short_side_index = []
        self.long_side_index = []
        self.set_storage_areas()

    def set_storage_areas(self):
        # short side
        for i in range(CONSTDATA.short_side_storage_area_num):
            x = CONSTDATA.storage_area_short_side_end_coordinate.x - i * CONSTDATA.short_side_width_between_storage_areas
            y = CONSTDATA.storage_area_short_side_end_coordinate.y
            index = i
            self.storage_areas.append(STORAGEAREA(COORDINATE(x, y), index))
            self.short_side_index.append(index)
        # long side
        for i in range(CONSTDATA.long_side_storage_area_num):
            x = CONSTDATA.storage_area_long_side_end_coordinate.x - i * CONSTDATA.long_side_width_between_storage_areas
            y = CONSTDATA.storage_area_long_side_end_coordinate.y
            index = i + CONSTDATA.short_side_storage_area_num
            self.storage_areas.append(STORAGEAREA(COORDINATE(x, y), index))
            self.long_side_index.append(index)
