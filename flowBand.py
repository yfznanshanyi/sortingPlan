import copy
import math
from flow import FLOW
from constData import CONSTDATA


class FLOWBAND(object):
    def __init__(self, flow_list):
        self.flow_list = copy.copy(flow_list)
        self.flow_dict = {}
        self.loads = 0
        self.mean_loads = 0
        self.set_basic_data()

    def set_loads(self):
        self.loads = sum([flow.loads for flow in self.flow_list])
        self.mean_loads = self.loads / len(self.flow_list)
        return self.loads

    def set_flow_dict(self):
        self.flow_dict = {flow.destination: flow for flow in self.flow_list}
        return self.flow_dict

    def set_basic_data(self):
        self.set_loads()
        self.set_flow_dict()

    # 单个大流向分解
    def split_big_flow(self, sorting_sation_weight, sorting_sation_num_ub):
        if len(self.flow_list) == 1:
            split_num = self.loads / sorting_sation_weight
            # print('loads: ',self.loads,' split_num: ',split_num)
            if split_num < CONSTDATA.sorting_sation_travel_level1_split_rate_lb:
                return [FLOWBAND(self.flow_list)]
            elif split_num > sorting_sation_num_ub:
                split_num = sorting_sation_num_ub
            else:
                split_num = math.ceil(split_num)
            mean_loads = self.loads / split_num
            temp_flowBands_list = []
            for i in range(split_num):
                flow = copy.copy(self.flow_list[0])
                flow.loads = mean_loads
                temp_flowBands_list.append(FLOWBAND([flow]))
            # print(self.flow_list[0].destination,len(temp_flowBands_list))
            return temp_flowBands_list
        else:
            return -1

    # 用于小流向合并，并输出flowBand列表
    def set_combined_flowBands(self, sorting_sation_weight, sorting_sation_travel_level1_combine_rate_ub):
        # flow
        temp_flow_list = copy.copy(self.flow_list)
        temp_flow_list.sort()
        combined_flowBands = []
        temp_flowBand = []
        for flow in temp_flow_list:
            if len(temp_flowBand) == 0:
                temp_flowBand.append(copy.copy(flow))
            elif sum([flow.loads for flow in temp_flowBand]) < sorting_sation_weight:
                weight_ub = sorting_sation_travel_level1_combine_rate_ub * sorting_sation_weight
                if sum([flow.loads for flow in temp_flowBand]) + flow.loads < weight_ub:
                    temp_flowBand.append(copy.copy(flow))
                else:
                    combined_flowBands.append(FLOWBAND(temp_flowBand))
                    temp_flowBand = []
                    temp_flowBand.append(copy.copy(flow))
            else:
                combined_flowBands.append(FLOWBAND(temp_flowBand))
                temp_flowBand = []
                temp_flowBand.append(copy.copy(flow))
        if len(temp_flowBand) != 0:
            combined_flowBands.append(FLOWBAND(temp_flowBand))
            temp_flowBand = []
        return combined_flowBands

    def same(self, other):
        if self.flow_dict == other.flow_dict:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.loads < other.loads:
            return True
        else:
            return False

    def __le__(self, other):
        if self.loads <= other.loads:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.loads > other.loads:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.loads >= other.loads:
            return True
        else:
            return False
