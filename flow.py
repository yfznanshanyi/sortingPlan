import copy
import pandas as pd
import numpy as np

from constData import CONSTDATA


class FLOW(object):
    def __init__(self, destination, travele_level, loads, zone, NC_rate=CONSTDATA.default_NC_rate):  # , trunk_num):
        self.destination = destination
        self.travel_level = travele_level
        self.loads = loads
        self.zone = zone
        self.NC_rate = NC_rate
        self.loads_no_NC = 0.0
        self.loads_NC = 0.0
        self.set_loads_NC()
        self.set_loads_no_NC()
        # self.trunk_num = trunk_num

    def set_loads_no_NC(self):
        self.loads_no_NC = self.loads * (1.0 - self.NC_rate)
        return self.loads_no_NC

    def set_loads_NC(self):
        self.loads_NC = self.loads * self.NC_rate
        return self.loads_NC

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


class FLOWINFO(object):
    def __init__(self, input_date, split_label,NC_label):
        self.input_data = copy.copy(input_date)
        self.date_list = []
        self.shift_list = []
        self.destination_list = []
        self.travel_level_list = []
        self.zone_list = []
        self.travel_level_zone_dict = {}
        self.travel_level_destination_zone_dict = {}
        self.travel_level_zone_destination_dict = {}
        # self.shift_travel_level_flow_dict = {}
        self.flows_used_dict = {}
        self.flows_used_NC_rate_dict = {}
        self.shift_travel_level_zone = {}
        self.date_shift_destination_NC_rate = {}
        self.set_basic_data(NC_label)

        # set split rate
        self.big_shift = '755VF2200'
        self.big_shift_split_rate = {}
        if split_label == True:
            self.set_big_shift_split_rate()

        # set flows used
        self.set_flows()
        self.set_flows_used_dict()

    def set_date_list(self):
        self.date_list = list(self.input_data.loading_table_out['运行日期'].unique())
        self.date_list.sort()
        # print('date list: ', self.date_list)
        return self.date_list

    def set_shift_list(self):
        self.shift_list = list(self.input_data.loading_table_out['计划发出班次'].unique())
        self.shift_list.sort()
        # print('shift list: ', self.shift_list)
        return self.shift_list

    def set_zone_list(self):
        self.zone_list = list(self.input_data.loading_table_out['到达地区'].unique())
        self.zone_list.sort()
        # print('zone list: ', self.zone_list)
        return self.shift_list

    def set_destination_list(self):
        self.destination_list = list(self.input_data.loading_table_out['到达网点'].unique())
        return self.destination_list

    def set_travel_level_list(self):
        self.travel_level_list = list(self.input_data.loading_table_out['运输等级'].unique())
        self.travel_level_list = ['一级运输', '二级运输', '三级运输']
        # print('travel level list: ', self.travel_level_list)
        return self.travel_level_list

    def set_travel_level_zone_dict(self):
        self.travel_level_zone_dict = {}
        temp_loading_table_out = copy.copy(self.input_data.loading_table_out[['运输等级', '到达地区']].drop_duplicates())
        for item in zip(temp_loading_table_out['运输等级'], temp_loading_table_out['到达地区']):
            if item[0] not in self.travel_level_zone_dict.keys():
                self.travel_level_zone_dict[item[0]] = [item[1]]
            else:
                self.travel_level_zone_dict[item[0]].append(item[1])
        # print('travel_level_zone_dict: ', self.travel_level_zone_dict)
        return self.travel_level_zone_dict

    def set_travel_level_zone_destination_dict(self):
        self.travel_level_zone_destination_dict = {}
        temp_loading_table_out = copy.copy(
            self.input_data.loading_table_out[['运输等级', '到达地区', '到达网点']].drop_duplicates())
        for travel_level in self.travel_level_list:
            self.travel_level_zone_destination_dict[travel_level] = {}
            for zone in self.travel_level_zone_dict[travel_level]:
                self.travel_level_zone_destination_dict[travel_level][zone] = []
        for r, c in temp_loading_table_out.iterrows():
            self.travel_level_zone_destination_dict[c[0]][c[1]].append(c[2])
        # print('travel_level_zone_destination_dict: ', self.travel_level_zone_destination_dict)
        return self.travel_level_zone_destination_dict

    def set_travel_level_destination_zone_dict(self):
        self.travel_level_destination_zone_dict = {}
        temp_loading_table_out = copy.copy(
            self.input_data.loading_table_out[['运输等级', '到达地区', '到达网点']].drop_duplicates())
        for r, c, in temp_loading_table_out.iterrows():
            if c[0] not in self.travel_level_destination_zone_dict.keys():
                self.travel_level_destination_zone_dict[c[0]] = {}
                self.travel_level_destination_zone_dict[c[0]][c[2]] = c[1]
            else:
                self.travel_level_destination_zone_dict[c[0]][c[2]] = c[1]
        return self.travel_level_destination_zone_dict

    def set_shift_travel_level_zone(self):
        self.shift_travel_level_zone = {}
        temp_loading_table_out = copy.copy(
            self.input_data.loading_table_out[['计划发出班次', '运输等级', '到达地区']].drop_duplicates())
        for item in zip(temp_loading_table_out['计划发出班次']):
            self.shift_travel_level_zone[item[0]] = {}
        for item in zip(temp_loading_table_out['计划发出班次'], temp_loading_table_out['运输等级']):
            self.shift_travel_level_zone[item[0]][item[1]] = []
        for item in zip(temp_loading_table_out['计划发出班次'],
                        temp_loading_table_out['运输等级'], temp_loading_table_out['到达地区']):
            self.shift_travel_level_zone[item[0]][item[1]].append(item[2])
        return self.shift_travel_level_zone

    def generate_date_shift_destination_NC_rate(self):
        df_NC_rate = pd.DataFrame()
        temp_date = []
        temp_shift = []
        temp_destination = []
        temp_NC_rate = []
        for date in self.date_list:
            for shift in self.shift_list:
                for destination in self.destination_list:
                    temp_date.append(date)
                    temp_shift.append(shift)
                    temp_destination.append(destination)
                    temp_NC_rate.append(copy.copy(np.random.uniform(0.0, CONSTDATA.NC_rate_up_bound)))
        df_NC_rate['date'] = temp_date
        df_NC_rate['shift'] = temp_shift
        df_NC_rate['destination'] = temp_destination
        df_NC_rate['NC_rate'] = temp_NC_rate
        df_NC_rate.to_csv('df_NC_rate.csv',index=False)
        return df_NC_rate

    def set_default_NC_rate(self):
        self.date_shift_destination_NC_rate = {}
        for date in self.date_list:
            self.date_shift_destination_NC_rate[date] = {}
            for shift in self.shift_list:
                self.date_shift_destination_NC_rate[date][shift] = {}
                for destination in self.destination_list:
                    self.date_shift_destination_NC_rate[date][shift][destination] = CONSTDATA.default_NC_rate
        return self.date_shift_destination_NC_rate

    def set_date_shift_destination_NC_rate(self):
        NC_rate_df = copy.copy(self.input_data.NC_rate[self.input_data.NC_rate['date'].isin(self.date_list)])
        for r,c in NC_rate_df.iterrows():
            date = c['date']
            shift = c['shift']
            destination = c['destination']
            NC_rate = c['NC_rate']
            if date not in self.date_shift_destination_NC_rate.keys():
                continue
            self.date_shift_destination_NC_rate[date][shift][destination] = NC_rate
        return self.date_shift_destination_NC_rate

    def set_basic_data(self,NC_label):
        self.set_date_list()
        self.set_shift_list()
        self.set_zone_list()
        self.set_destination_list()
        self.set_travel_level_list()
        self.set_travel_level_zone_dict()
        self.set_travel_level_zone_destination_dict()
        self.set_travel_level_destination_zone_dict()
        self.set_shift_travel_level_zone()
        # self.generate_date_shift_destination_NC_rate()
        self.set_default_NC_rate()
        if NC_label==True:
            self.set_date_shift_destination_NC_rate()

    def set_big_shift_split_rate(self):
        # default shift
        self.big_shift_split_rate = {}
        temp_split_rate = copy.copy(self.input_data.split_rate[['下一站网点', '1号库货量占比']])
        for item in zip(temp_split_rate['下一站网点'], temp_split_rate['1号库货量占比']):
            self.big_shift_split_rate[item[0]] = item[1]
        return self.big_shift_split_rate

    def set_flows(self):
        self.date_shift_flow_travel_level_dict = {}
        temp_loading_table_out = pd.pivot_table(self.input_data.loading_table_out, values={'装载重量'},
                                                index={'运行日期', '计划发出班次', '运输等级', '到达网点'},
                                                fill_value=0, aggfunc='sum')
        temp_loading_table_out.reset_index(inplace=True)
        for date in self.date_list:
            self.date_shift_flow_travel_level_dict[date] = {}
            for shift in self.shift_list:
                self.date_shift_flow_travel_level_dict[date][shift] = {}
                for travel_level in self.travel_level_list:
                    self.date_shift_flow_travel_level_dict[date][shift][travel_level] = {}
        for r, c in temp_loading_table_out.iterrows():
            rate = 1.0
            if c['计划发出班次'] == self.big_shift:
                if c['到达网点'] in self.big_shift_split_rate.keys():
                    rate = self.big_shift_split_rate[c['到达网点']]
            self.date_shift_flow_travel_level_dict[c['运行日期']][c['计划发出班次']][c['运输等级']][c['到达网点']] = \
                c['装载重量'] * rate
        return self.date_shift_flow_travel_level_dict

    def set_flows_used_dict(self):
        self.flows_used_dict = {}
        self.flows_used_NC_rate_dict = {}
        for shift in self.shift_list:
            self.flows_used_dict[shift] = {}
            self.flows_used_NC_rate_dict[shift] = {}
            for travel_level in self.travel_level_list:
                self.flows_used_dict[shift][travel_level] = {}
                self.flows_used_NC_rate_dict[shift][travel_level] = {}
        # max loads
        # for date in self.date_list:
        #     for shift in self.shift_list:
        #         for travel_level in self.travel_level_list:
        #             for destination in self.date_shift_flow_travel_level_dict[date][shift][travel_level].keys():
        #                 if destination not in self.flows_used_dict[shift][travel_level].keys():
        #                     self.flows_used_dict[shift][travel_level][destination] = \
        #                         self.date_shift_flow_travel_level_dict[date][shift][travel_level][destination]
        #                     self.flows_used_NC_rate_dict[shift][destination] = \
        #                         self.date_shift_destination_NC_rate[date][shift][destination]
        #                 else:
        #                     orirgin_loads = self.flows_used_dict[shift][travel_level][destination]
        #                     self.flows_used_dict[shift][travel_level][destination] = \
        #                         max(self.flows_used_dict[shift][travel_level][destination],
        #                             self.date_shift_flow_travel_level_dict[date][shift][travel_level][destination])
        #                     if self.flows_used_dict[shift][travel_level][destination] != orirgin_loads:
        #                         self.flows_used_NC_rate_dict[shift][destination] = \
        #                             self.date_shift_destination_NC_rate[date][shift][destination]
        # mean loads
        for date in self.date_list:
            for shift in self.shift_list:
                for travel_level in self.travel_level_list:
                    for destination in self.date_shift_flow_travel_level_dict[date][shift][travel_level].keys():
                        if destination not in self.flows_used_dict[shift][travel_level].keys():
                            self.flows_used_dict[shift][travel_level][destination] = \
                                self.date_shift_flow_travel_level_dict[date][shift][travel_level][destination]
                            self.flows_used_NC_rate_dict[shift][destination] = \
                                self.date_shift_destination_NC_rate[date][shift][destination]
                        else:
                            orirgin_loads = self.flows_used_dict[shift][travel_level][destination]
                            self.flows_used_dict[shift][travel_level][destination] = \
                                max(self.flows_used_dict[shift][travel_level][destination],
                                    self.date_shift_flow_travel_level_dict[date][shift][travel_level][destination])
                            if self.flows_used_dict[shift][travel_level][destination] != orirgin_loads:
                                self.flows_used_NC_rate_dict[shift][destination] = \
                                    self.date_shift_destination_NC_rate[date][shift][destination]
        return self.flows_used_dict

    # def set_flows_used_dict(self):
    #     self.flows_used_dict = {}
    #     self.flows_used_NC_rate_dict = {}
    #     for shift in self.shift_list:
    #         self.flows_used_dict[shift] = {}
    #         self.flows_used_NC_rate_dict[shift] = {}
    #         for travel_level in self.travel_level_list:
    #             self.flows_used_dict[shift][travel_level] = {}
    #             self.flows_used_NC_rate_dict[shift][travel_level] = {}
    #     for date in self.date_list:
    #         for shift in self.shift_list:
    #             for travel_level in self.travel_level_list:
    #                 for destination in self.date_shift_flow_travel_level_dict[date][shift][travel_level].keys():
    #                     if destination not in self.flows_used_dict[shift][travel_level].keys():
    #                         self.flows_used_dict[shift][travel_level][destination] = \
    #                             [self.date_shift_flow_travel_level_dict[date][shift][travel_level][destination]]
    #                         self.flows_used_NC_rate_dict[shift][destination] = \
    #                             [self.date_shift_destination_NC_rate[date][shift][destination]]
    #                     else:
    #                         orirgin_loads = self.flows_used_dict[shift][travel_level][destination]
    #                         self.flows_used_dict[shift][travel_level][destination].append(
    #                             self.date_shift_flow_travel_level_dict[date][shift][travel_level][destination])
    #                         if self.flows_used_dict[shift][travel_level][destination] != orirgin_loads:
    #                             self.flows_used_NC_rate_dict[shift][destination].append(
    #                                 self.date_shift_destination_NC_rate[date][shift][destination])
    #     for shift in self.shift_list:
    #         for travel_level in self.travel_level_list:
    #             for destination in self.flows_used_dict[shift][travel_level].keys():
    #                 loads = copy.copy(self.flows_used_dict[shift][travel_level][destination])
    #                 mean_loads = sum(loads)/len(loads)
    #                 self.flows_used_dict[shift][travel_level][destination] = mean_loads
    #                 loads_no_NC = copy.copy(self.flows_used_NC_rate_dict[shift][destination])
    #                 mean_loads_no_NC = sum(loads_no_NC)/len(loads_no_NC)
    #                 self.flows_used_NC_rate_dict[shift][destination] = mean_loads_no_NC
    #     return self.flows_used_dict
