from constData import CONSTDATA
from coordinate import COORDINATE


class LOADINGBERTH(object):
    def __init__(self, coordinate, index):
        self.coordinate = coordinate
        self.index = index


class LOADINGBERTHSET(object):
    def __init__(self):
        self.loading_berths = []
        self.short_side_index = []
        self.long_side_index = []
        self.NC_loading_berths = []
        self.NC_short_side_index = []
        self.NC_long_side_index = []
        self.set_loading_berths()
        self.set_NC_loading_berths()

    def set_loading_berths(self):
        # short side
        for i in range(CONSTDATA.short_side_loading_berth_num):
            x = CONSTDATA.loading_berth_short_side_end_coordinate.x - \
                (i + CONSTDATA.short_side_unloading_berth_num+CONSTDATA.short_side_NC_loading_berth_num) * \
                CONSTDATA.short_side_width_between_loading_berths
            y = CONSTDATA.loading_berth_short_side_end_coordinate.y
            index = i
            self.loading_berths.append(LOADINGBERTH(COORDINATE(x, y), index))
            self.short_side_index.append(index)
        # long side
        for i in range(CONSTDATA.long_side_loading_berth_num):
            x = CONSTDATA.loading_berth_long_side_end_coordinate.x - \
                (i + CONSTDATA.long_side_unloading_berth_num+CONSTDATA.long_side_NC_loading_berth_num) *\
                CONSTDATA.long_side_width_between_loading_berths
            y = CONSTDATA.loading_berth_long_side_end_coordinate.y
            index = i + CONSTDATA.short_side_loading_berth_num
            self.loading_berths.append(LOADINGBERTH(COORDINATE(x, y), index))
            self.long_side_index.append(index)

    def set_NC_loading_berths(self):
        for i in range(CONSTDATA.short_side_NC_loading_berth_num):
            x = CONSTDATA.loading_berth_short_side_end_coordinate.x - \
                (i + CONSTDATA.short_side_unloading_berth_num) \
                * CONSTDATA.short_side_width_between_loading_berths
            y = CONSTDATA.loading_berth_short_side_end_coordinate.y
            index = i
            self.NC_loading_berths.append(LOADINGBERTH(COORDINATE(x, y), index))
            self.NC_short_side_index.append(index)
        for i in range(CONSTDATA.long_side_NC_loading_berth_num):
            x = CONSTDATA.loading_berth_long_side_end_coordinate.x - \
                (i + CONSTDATA.long_side_unloading_berth_num) \
                * CONSTDATA.long_side_width_between_loading_berths
            y = CONSTDATA.loading_berth_long_side_end_coordinate.y
            index = i + CONSTDATA.short_side_NC_loading_berth_num
            self.NC_loading_berths.append(LOADINGBERTH(COORDINATE(x, y), index))
            self.NC_long_side_index.append(index)