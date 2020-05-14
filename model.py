import copy
import numpy as np

from sortingSation import SORTINGSATIONSET
from storageArea import STORAGEAREASET
from loadingBerth import LOADINGBERTHSET
from flow import FLOW
from flowBand import FLOWBAND
from constData import CONSTDATA


class MODEL(object):
    def __init__(self, flow_info):
        self.flow_info = copy.copy(flow_info)
        self.sorting_sation_set = SORTINGSATIONSET()
        self.loading_berth_set = LOADINGBERTHSET()
        self.storage_area_set = STORAGEAREASET()

        # data for calculate
        self.main_line_distance_list = []
        self.sorting_sation_2_storage_area_distance_matrix = []
        self.storage_area_2_loading_berth_distance_matrix = []
        self.sorting_sation_2_NC_loading_berth_distance_list = []
        self.NC_loading_berth_2_storage_area_distance_list = []
        self.set_calculate_data()

        # encoding and decoding
        self.shift_flowBands = {}
        self.shift_flowBands_all_loads = {}
        self.shift_flowBands_mean_loads = {}
        self.set_shift_flowBands()
        self.shift_travel_level_flowBands = {}
        self.shift_travel_level_flowBands_all_loads = {}
        self.shift_travel_level_flowBands_mean_loads = {}
        self.set_shift_travel_level_flowBands()
        self.shift_travel_level_zone_flowBands = {}
        self.shift_travel_level_zone_flowBands_all_loads = {}
        self.shift_travel_level_zone_flowBands_mean_loads = {}
        self.set_shift_travel_level_zone_flowBands()

        self.encoding = []
        self.fit = {}
        self.encoding_record = {}

    def set_shift_flowBands(self):
        self.shift_flowBands = {}
        for shift in self.flow_info.shift_travel_level_zone.keys():
            self.shift_flowBands[shift] = []
        for shift in self.flow_info.shift_travel_level_zone.keys():
            for travel_level in self.flow_info.shift_travel_level_zone[shift].keys():
                for destination in self.flow_info.flows_used_dict[shift][travel_level]:
                    loads = self.flow_info.flows_used_dict[shift][travel_level][destination]
                    zone = self.flow_info.travel_level_destination_zone_dict[travel_level][destination]
                    NC_rate = self.flow_info.flows_used_NC_rate_dict[shift][destination]
                    self.shift_flowBands[shift].append(FLOW(destination, travel_level, loads, zone, NC_rate))
        self.shift_flowBands_mean_loads = {}
        self.shift_flowBands_all_loads = {}
        for shift in self.flow_info.shift_travel_level_zone.keys():
            self.shift_flowBands_mean_loads[shift] = copy.copy(
                np.mean([flow.loads for flow in self.shift_flowBands[shift]]))
            self.shift_flowBands_all_loads[shift] = copy.copy(
                np.sum([flow.loads for flow in self.shift_flowBands[shift]]))
        return self.shift_flowBands

    def set_shift_travel_level_flowBands(self):
        self.shift_travel_level_flowBands = {}
        for shift in self.flow_info.shift_travel_level_zone.keys():
            self.shift_travel_level_flowBands[shift] = {}
            for travel_level in self.flow_info.shift_travel_level_zone[shift].keys():
                self.shift_travel_level_flowBands[shift][travel_level] = []
        for shift in self.flow_info.shift_travel_level_zone.keys():
            for travel_level in self.flow_info.shift_travel_level_zone[shift].keys():
                for destination in self.flow_info.flows_used_dict[shift][travel_level]:
                    loads = self.flow_info.flows_used_dict[shift][travel_level][destination]
                    zone = self.flow_info.travel_level_destination_zone_dict[travel_level][destination]
                    NC_rate = self.flow_info.flows_used_NC_rate_dict[shift][destination]
                    self.shift_travel_level_flowBands[shift][travel_level].append(
                        FLOW(destination, travel_level, loads, zone, NC_rate))
        self.shift_travel_level_flowBands_mean_loads = {}
        self.shift_travel_level_flowBands_all_loads = {}
        for shift in self.flow_info.shift_travel_level_zone.keys():
            self.shift_travel_level_flowBands_mean_loads[shift] = {}
            self.shift_travel_level_flowBands_all_loads[shift] = {}
            for travel_level in self.flow_info.shift_travel_level_zone[shift].keys():
                self.shift_travel_level_flowBands_mean_loads[shift][travel_level] = \
                    copy.copy(np.mean([flow.loads for flow in self.shift_travel_level_flowBands[shift][travel_level]]))
                self.shift_travel_level_flowBands_all_loads[shift][travel_level] = \
                    copy.copy(np.sum([flow.loads for flow in self.shift_travel_level_flowBands[shift][travel_level]]))
        return self.shift_travel_level_flowBands

    def set_shift_travel_level_zone_flowBands(self):
        self.shift_travel_level_zone_flowBands = {}
        for shift in self.flow_info.shift_travel_level_zone.keys():
            self.shift_travel_level_zone_flowBands[shift] = {}
            for travel_level in self.flow_info.shift_travel_level_zone[shift].keys():
                self.shift_travel_level_zone_flowBands[shift][travel_level] = {}
                for zone in self.flow_info.shift_travel_level_zone[shift][travel_level]:
                    self.shift_travel_level_zone_flowBands[shift][travel_level][zone] = []
        for shift in self.flow_info.shift_travel_level_zone.keys():
            for travel_level in self.flow_info.shift_travel_level_zone[shift].keys():
                for destination in self.flow_info.flows_used_dict[shift][travel_level]:
                    loads = self.flow_info.flows_used_dict[shift][travel_level][destination]
                    zone = self.flow_info.travel_level_destination_zone_dict[travel_level][destination]
                    NC_rate = self.flow_info.flows_used_NC_rate_dict[shift][destination]
                    self.shift_travel_level_zone_flowBands[shift][travel_level][zone]. \
                        append(FLOW(destination, travel_level, loads, zone, NC_rate))
        self.shift_travel_level_zone_flowBands_mean_loads = {}
        self.shift_travel_level_zone_flowBands_all_loads = {}
        for shift in self.flow_info.shift_travel_level_zone.keys():
            self.shift_travel_level_zone_flowBands_mean_loads[shift] = {}
            self.shift_travel_level_zone_flowBands_all_loads[shift] = {}
            for travel_level in self.flow_info.shift_travel_level_zone[shift].keys():
                self.shift_travel_level_zone_flowBands_mean_loads[shift][travel_level] = {}
                self.shift_travel_level_zone_flowBands_all_loads[shift][travel_level] = {}
                for zone in self.flow_info.shift_travel_level_zone[shift][travel_level]:
                    self.shift_travel_level_zone_flowBands_mean_loads[shift][travel_level][zone] = \
                        copy.copy(np.mean(
                            [flow.loads for flow in self.shift_travel_level_zone_flowBands[shift][travel_level][zone]]))
                    self.shift_travel_level_zone_flowBands_all_loads[shift][travel_level][zone] = \
                        copy.copy(np.sum(
                            [flow.loads for flow in self.shift_travel_level_zone_flowBands[shift][travel_level][zone]]))
        return self.shift_travel_level_zone_flowBands

    def set_main_line_list(self):
        self.main_line_distance_list = []
        for index in self.sorting_sation_set.short_side_index:
            coordinate1 = CONSTDATA.sorting_sation_short_side_end_coordinate
            coordinate2 = self.sorting_sation_set.sorting_sations[index].coordinate
            distance = coordinate1.get_dist(coordinate2) + CONSTDATA.sorting_sation_width / 2
            self.main_line_distance_list.append(distance)
        for index in self.sorting_sation_set.long_side_index:
            coordinate1 = CONSTDATA.sorting_sation_long_side_end_coordinate
            coordinate2 = self.sorting_sation_set.sorting_sations[index].coordinate
            distance = coordinate1.get_dist(coordinate2) + CONSTDATA.sorting_sation_width / 2
            self.main_line_distance_list.append(distance)
        return self.main_line_distance_list

    def set_sorting_sation_2_storage_area_distance_matrix(self):
        self.sorting_sation_2_storage_area_distance_matrix = []
        for sorting_sation in self.sorting_sation_set.sorting_sations:
            distance_list = []
            for storage_area in self.storage_area_set.storage_areas:
                coordinate1 = sorting_sation.coordinate
                coordinate2 = storage_area.coordinate
                distance = coordinate1.get_dist(coordinate2)
                distance_list.append(distance)
            self.sorting_sation_2_storage_area_distance_matrix.append(copy.copy(distance_list))
        return self.sorting_sation_2_storage_area_distance_matrix

    def set_storage_area_2_loading_berth_distance_matrix(self):
        self.storage_area_2_loading_berth_distance_matrix = []
        for storage_area in self.storage_area_set.storage_areas:
            distance_list = []
            for loading_berth in self.loading_berth_set.loading_berths:
                coordinate1 = storage_area.coordinate
                coordinate2 = loading_berth.coordinate
                distance = coordinate1.get_dist(coordinate2)
                distance_list.append(distance)
            self.storage_area_2_loading_berth_distance_matrix.append(copy.copy(distance_list))
        return self.storage_area_2_loading_berth_distance_matrix

    def set_sorting_sation_2_NC_loading_berth_distance_list(self):
        self.sorting_sation_2_NC_loading_berth_distance_list = []
        for index, sorting_sation in enumerate(self.sorting_sation_set.sorting_sations):
            coordinate1 = sorting_sation.coordinate
            if index in self.sorting_sation_set.short_side_index:
                NC_index = self.loading_berth_set.NC_short_side_index[0]
                coordinate2 = self.loading_berth_set.NC_loading_berths[NC_index].coordinate
            else:
                NC_index = self.loading_berth_set.NC_long_side_index[0]
                coordinate2 = self.loading_berth_set.NC_loading_berths[NC_index].coordinate
            distance = coordinate1.get_dist(coordinate2)
            self.sorting_sation_2_NC_loading_berth_distance_list.append(distance)
        return self.sorting_sation_2_NC_loading_berth_distance_list

    def set_NC_loading_berth_2_loading_berth_distance_list(self):
        self.NC_loading_berth_2_storage_area_distance_list = []
        for index, loading_berth in enumerate(self.loading_berth_set.loading_berths):
            coordinate1 = loading_berth.coordinate
            if index in self.loading_berth_set.short_side_index:
                NC_index = self.loading_berth_set.NC_short_side_index[0]
                coordinate2 = self.loading_berth_set.NC_loading_berths[NC_index].coordinate
            else:
                NC_index = self.loading_berth_set.NC_long_side_index[0]
                coordinate2 = self.loading_berth_set.NC_loading_berths[NC_index].coordinate
            distance = coordinate1.get_dist(coordinate2)
            self.NC_loading_berth_2_storage_area_distance_list.append(distance)
        return self.NC_loading_berth_2_storage_area_distance_list

    def set_calculate_data(self):
        self.set_main_line_list()
        self.set_sorting_sation_2_storage_area_distance_matrix()
        self.set_storage_area_2_loading_berth_distance_matrix()
        self.set_sorting_sation_2_NC_loading_berth_distance_list()
        self.set_NC_loading_berth_2_loading_berth_distance_list()

    def initliza_encoding(self):
        encoding = {'encoding_flow_sorting_sation': {}, 'encoding_flow_loading_berth': {}}
        self.encoding = copy.copy(encoding)
        return encoding

    def cost_main_line(self, encoding):
        weight_distance = 0.0
        for flowBand, index in encoding['encoding_flow_sorting_sation'].items():
            weight = flowBand.get_no_NC_loads()  / CONSTDATA.kg_t
            distance = self.main_line_distance_list[index] + CONSTDATA.before_main_line_distance
            weight_distance = weight_distance + weight * distance
        return weight_distance

    def cost_sorting_sation_2_storage_area(self, encoding):
        weight_distance = 0.0
        for flowBand, sorting_sation_index in encoding['encoding_flow_sorting_sation'].items():
            weight = flowBand.get_no_NC_loads()
            pallet = weight / CONSTDATA.pallets_weight
            # print(flowBand.flow_list[0].destination)
            storage_area_index = encoding['encoding_flow_loading_berth'][flowBand]
            distance = self.sorting_sation_2_storage_area_distance_matrix[sorting_sation_index][storage_area_index]
            weight_distance = weight_distance + pallet * distance
        weight_distance = weight_distance * 2
        return weight_distance

    def cost_storage_area_2_loading_berth(self, encoding):
        weight_distance = 0.0
        for flowBand, index in encoding['encoding_flow_loading_berth'].items():
            weight = flowBand.get_no_NC_loads()
            pallet = weight / CONSTDATA.pallets_weight
            distance = self.storage_area_2_loading_berth_distance_matrix[index][index]
            weight_distance = weight_distance + pallet * distance
        weight_distance = weight_distance * 2
        return weight_distance

    def cost_NC_loading_berth_2_storage_area(self, encoding):
        weight_distance = 0.0
        for flowBand, index in encoding['encoding_flow_loading_berth'].items():
            weight = flowBand.get_NC_loads()
            pallet = weight / CONSTDATA.pallets_weight
            distance = self.NC_loading_berth_2_storage_area_distance_list[index]
            weight_distance = weight_distance + pallet * distance
        weight_distance = weight_distance * 2
        return weight_distance

    def cost_NC_storage_area_2_loading_berth(self, encoding):
        weight_distance = 0.0
        for flowBand, index in encoding['encoding_flow_loading_berth'].items():
            weight = flowBand.get_NC_loads()
            pallet = weight / CONSTDATA.pallets_weight
            distance = self.storage_area_2_loading_berth_distance_matrix[index][index]
            weight_distance = weight_distance + pallet * distance
        weight_distance = weight_distance * 2
        return weight_distance

    def decoding(self, encoding):
        fit = {}
        fit['main_line'] = self.cost_main_line(encoding)
        fit['sorting_sation_2_storage_area'] = self.cost_sorting_sation_2_storage_area(encoding)
        fit['storage_area_2_loading_berth'] = self.cost_storage_area_2_loading_berth(encoding)
        fit['NC_loading_berth_2_storage_area'] = self.cost_NC_loading_berth_2_storage_area(encoding)
        fit['NC_storage_area_2_loading_berth'] = self.cost_NC_storage_area_2_loading_berth(encoding)
        return fit

    def set_encoding(self, encoding):
        self.encoding = copy.copy(encoding)
        return self.encoding

    def set_fit(self, fit):
        self.fit = copy.copy(fit)
        return self.fit

    def show_encoding(self):
        print('encoding_flow_sorting_sation: ')
        for flowBand, sorting_sation_index in self.encoding['encoding_flow_sorting_sation'].items():
            for flow in flowBand.flow_list:
                print(sorting_sation_index + 1, flow.travel_level, flow.destination, flow.zone, flow.loads)
        print('encoding_flow_loading_berth: ')
        for flowBand, loading_berth_index in self.encoding['encoding_flow_loading_berth'].items():
            for flow in flowBand.flow_list:
                print(loading_berth_index + 1, flow.travel_level, flow.destination, flow.zone, flow.loads)
        return self.encoding

    def set_encoding_record(self):
        self.encoding_record = {}
        self.encoding_record['record_flow_sorting_sation'] = {}
        self.encoding_record['record_flow_loading_berth'] = {}
        # print('encoding_flow_sorting_sation: ')
        for flowBand, sorting_sation_index in self.encoding['encoding_flow_sorting_sation'].items():
            for flow in flowBand.flow_list:
                # print(sorting_sation_index + 1, flow.travel_level, flow.destination, flow.zone, flow.loads)
                if flow.destination not in self.encoding_record['record_flow_sorting_sation'].keys():
                    self.encoding_record['record_flow_sorting_sation'][flow.destination] = [sorting_sation_index]
                else:
                    self.encoding_record['record_flow_sorting_sation'][flow.destination].append(sorting_sation_index)
        # print('encoding_flow_loading_berth: ')
        for flowBand, loading_berth_index in self.encoding['encoding_flow_loading_berth'].items():
            for flow in flowBand.flow_list:
                # print(loading_berth_index + 1, flow.travel_level, flow.destination, flow.zone, flow.loads)
                if flow.destination not in self.encoding_record['record_flow_loading_berth'].keys():
                    self.encoding_record['record_flow_loading_berth'][flow.destination] = [loading_berth_index]
                else:
                    self.encoding_record['record_flow_loading_berth'][flow.destination].append(loading_berth_index)
        return self.encoding_record

    def show_fit(self):
        print('fit: ')
        for label, value in self.fit.items():
            print(label, ' : ', value)
        return self.fit

    def set_other_encoding(self, encoding, encoding_record):
        # shift = '755VF1401'
        shift = '755VF2200'
        self.flow_Bands = []
        for flowBand, sorting_sation_index in encoding['encoding_flow_sorting_sation'].items():
            temp_flow_list = []
            for flow in flowBand.flow_list:
                destination = flow.destination
                travel_level = flow.travel_level
                zone = flow.zone
                if destination not in self.flow_info.flows_used_dict[shift][travel_level].keys():
                    loads = 0
                    NC_rate = 0.0
                else:
                    loads = self.flow_info.flows_used_dict[shift][travel_level][destination]
                    NC_rate = self.flow_info.flows_used_NC_rate_dict[shift][destination]
                num = len(set(encoding_record['record_flow_sorting_sation'][destination]))
                loads = loads / num
                new_flow = FLOW(destination, travel_level, loads, zone, NC_rate)
                temp_flow_list.append(new_flow)
            temp_flowBand = FLOWBAND(temp_flow_list)
            self.flow_Bands.append(temp_flowBand)
            loading_berth_index = encoding['encoding_flow_loading_berth'][flowBand]
            self.encoding['encoding_flow_sorting_sation'][self.flow_Bands[-1]] = sorting_sation_index
            self.encoding['encoding_flow_loading_berth'][self.flow_Bands[-1]] = loading_berth_index
        return self.encoding
