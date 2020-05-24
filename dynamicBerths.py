import copy
from flow import FLOWINFO
from model import MODEL
from algs import ALGS
from model import MODEL
from constData import CONSTDATA
from calculateCost import CALCULATECOST

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class DYNAMICBERTHS(object):
    def __init__(self, data):
        self.data = copy.copy(data)
        self.date_list = copy.copy(self.data.date_list)
        self.record_date_list = []
        self.before_encoding_list = []
        self.after_encoding_list = []
        self.before_fit_list = []
        self.after_fit_list = []
        self.ori_fit_list = []
        self.mod_fit_list = []
        self.flow_info = FLOWINFO(self.data, False, False)
        self.model = MODEL(self.flow_info)
        self.encoding = {}
        self.fit = {}
        self.date_loads = {}
        self.loads_list = []
        self.date_before_ss_number = {}
        self.date_after_ss_number = {}
        self.date_origin_ss_number = {}
        self.date_modified_ss_number = {}
        # NC functions
        self.NC_date_list = copy.copy(self.data.date_list)
        self.NC_record_date_list = []
        self.NC_before_encoding_list = []
        self.NC_after_encoding_list = []
        self.NC_before_fit_list = []
        self.NC_after_fit_list = []
        self.NC_ori_fit_list = []
        self.NC_mod_fit_list = []
        self.NC_flow_info = FLOWINFO(self.data, True, False)
        self.NC_model = MODEL(self.NC_flow_info)
        self.NC_encoding = {}
        self.NC_fit = {}
        self.NC_date_loads = {}
        self.NC_loads_list = []
        self.NC_date_loads_no_NC = {}
        self.NC_loads_no_NC_list = []
        self.NC_date_NC_loads = {}
        self.NC_loads_NC_list = []
        self.NC_date_before_ss_number = {}
        self.NC_date_after_ss_number = {}
        self.NC_date_origin_ss_number = {}
        self.NC_date_modified_ss_number = {}

    def set_day_sort_plan(self, duration=0):
        self.record_date_list = []
        flow_info = FLOWINFO(self.data, False, False)
        model = MODEL(flow_info)
        algs = ALGS(model)
        self.encoding = algs.model.encoding
        self.fit = algs.model.fit
        calculateCost = CALCULATECOST(model)
        self.ori_fit = calculateCost.set_ori_cost()
        self.mod_fit = calculateCost.set_mod_cost()
        # algs.model.show_encoding()
        # algs.model.show_fit()
        encoding_record = algs.model.set_encoding_record()
        self.ori_fit_list = []
        for index, d in enumerate(self.date_list):
            ind = index + 1
            if duration != 0:
                if ind % duration == 0 and ind != 0 and ind != (len(self.date_list)):
                    date_list = self.date_list[ind - duration:ind]
                elif ind == (len(self.date_list)) and len(self.date_list) > duration:
                    date_list = self.date_list[ind - duration:ind]
                else:
                    continue
            else:
                date_list = [d]
            # print(date_list)
            self.record_date_list.append(date_list)
            temp_input_data = copy.copy(self.data)
            temp_input_data.set_date(date_list)
            flow_info = FLOWINFO(temp_input_data, False, False)
            model = MODEL(flow_info)
            algs = ALGS(model)
            self.before_encoding_list.append(algs.model.encoding)
            self.before_fit_list.append(algs.model.fit)
            # algs.model.show_fit()

            algs = ALGS(model, False, self.encoding, encoding_record)
            # algs.model.show_fit()
            self.after_encoding_list.append(algs.model.encoding)
            self.after_fit_list.append(algs.model.fit)
            calculateCost = CALCULATECOST(model)
            self.ori_fit_list.append(calculateCost.set_ori_cost())
            self.mod_fit_list.append(calculateCost.set_mod_cost())

    def set_compare_fit(self, label=True):
        self.comprea_info_fit = pd.DataFrame()
        temp_record_list = copy.copy(self.record_date_list)
        # temp_record_list.append('all')
        self.comprea_info_fit['date'] = temp_record_list
        before_main = []
        before_ss_2_sa = []
        before_sa_2_lb = []
        befor_NC_lb_2_sa = []
        befor_NC_sa_2_lb = []

        after_main = []
        after_ss_2_sa = []
        after_sa_2_lb = []
        after_NC_lb_2_sa = []
        after_NC_sa_2_lb = []

        origin_main = []
        origin_ss_2_sa = []
        origin_sa_2_lb = []

        modified_main = []
        modified_ss_2_sa = []
        modified_sa_2_lb = []

        for index, fit in enumerate(self.before_fit_list):
            before_main.append(fit['main_line'])
            before_ss_2_sa.append(fit['sorting_sation_2_storage_area'])
            before_sa_2_lb.append(fit['storage_area_2_loading_berth'])
            befor_NC_lb_2_sa.append(fit['NC_loading_berth_2_storage_area'])
            befor_NC_sa_2_lb.append(fit['NC_storage_area_2_loading_berth'])
            after_main.append(self.after_fit_list[index]['main_line'])
            after_ss_2_sa.append(self.after_fit_list[index]['sorting_sation_2_storage_area'])
            after_sa_2_lb.append(self.after_fit_list[index]['storage_area_2_loading_berth'])
            after_NC_lb_2_sa.append(self.after_fit_list[index]['NC_loading_berth_2_storage_area'])
            after_NC_sa_2_lb.append(self.after_fit_list[index]['NC_storage_area_2_loading_berth'])
            origin_main.append(self.ori_fit_list[index]['main_line_cost'])
            origin_ss_2_sa.append(self.ori_fit_list[index]['ss_2_sa_cost'])
            origin_sa_2_lb.append(self.ori_fit_list[index]['sa_2_lb_cost'])
            modified_main.append(self.mod_fit_list[index]['main_line_cost'])
            modified_ss_2_sa.append(self.mod_fit_list[index]['ss_2_sa_cost'])
            modified_sa_2_lb.append(self.mod_fit_list[index]['sa_2_lb_cost'])
        # before_main.append(self.fit['main_line'])
        # before_ss_2_sa.append(self.fit['sorting_sation_2_storage_area'])
        # before_sa_2_lb.append(self.fit['storage_area_2_loading_berth'])
        # befor_NC_lb_2_sa.append(self.fit['NC_loading_berth_2_storage_area'])
        # befor_NC_sa_2_lb.append(self.fit['NC_storage_area_2_loading_berth'])
        # after_main.append(self.fit['main_line'])
        # after_ss_2_sa.append(self.fit['sorting_sation_2_storage_area'])
        # after_sa_2_lb.append(self.fit['storage_area_2_loading_berth'])
        # after_NC_lb_2_sa.append(self.fit['NC_loading_berth_2_storage_area'])
        # after_NC_sa_2_lb.append(self.fit['NC_storage_area_2_loading_berth'])
        # origin_main.append(self.ori_fit['main_line_cost'])
        # origin_ss_2_sa.append(self.ori_fit['ss_2_sa_cost'])
        # origin_sa_2_lb.append(self.ori_fit['sa_2_lb_cost'])
        # modified_main.append(self.mod_fit['main_line_cost'])
        # modified_ss_2_sa.append(self.mod_fit['ss_2_sa_cost'])
        # modified_sa_2_lb.append(self.mod_fit['sa_2_lb_cost'])
        self.comprea_info_fit['before main_line'] = before_main
        self.comprea_info_fit['before sorting_sation_2_storage_area'] = before_ss_2_sa
        self.comprea_info_fit['before storage_area_2_loading_berth'] = before_sa_2_lb
        self.comprea_info_fit['before NC_loading_berth_2_storage_area'] = befor_NC_lb_2_sa
        self.comprea_info_fit['before NC_storage_area_2_loading_berth'] = befor_NC_sa_2_lb
        self.comprea_info_fit['after main_line'] = after_main
        self.comprea_info_fit['after sorting_sation_2_storage_area'] = after_ss_2_sa
        self.comprea_info_fit['after storage_area_2_loading_berth'] = after_sa_2_lb
        self.comprea_info_fit['after NC_loading_berth_2_storage_area'] = after_NC_lb_2_sa
        self.comprea_info_fit['after NC_storage_area_2_loading_berth'] = after_NC_sa_2_lb
        self.comprea_info_fit['origin main'] = origin_main
        self.comprea_info_fit['origin ss_2_sa'] = origin_ss_2_sa
        self.comprea_info_fit['origin sa_2_lb'] = origin_sa_2_lb
        self.comprea_info_fit['modified main'] = modified_main
        self.comprea_info_fit['modified ss_2_sa'] = modified_ss_2_sa
        self.comprea_info_fit['modified sa_2_lb'] = modified_sa_2_lb
        self.comprea_info_fit['loads'] = self.loads_list[:-1]
        if label == True:
            self.comprea_info_fit.to_csv(self.data.output_filefolder + 'comprea_info_fit.csv', index=False)
        return self.comprea_info_fit

    def set_date_loads(self):
        self.date_loads = {}
        temp_date_loads = pd.pivot_table(self.comprea_info_encoding, values='loads', index='date', fill_value=0,
                                         aggfunc='sum')
        temp_date_loads.reset_index(inplace=True)
        self.date_loads = {k: v for k, v in zip(temp_date_loads['date'], temp_date_loads['loads'])}
        temp_date_loads.sort_values(by='date', inplace=True)
        self.loads_list = list(copy.copy(temp_date_loads['loads']))
        return self.date_loads

    def set_compare_encoding(self, label=True):
        self.comprea_info_encoding = pd.DataFrame()
        date = []
        destination = []
        travel_level = []
        zone = []
        loads = []

        before_ss_index = []
        before_ss_coor = []
        before_main_line_dist = []
        before_lb_index = []
        before_lb_coor = []
        before_ss_2_sa_dist = []
        before_sa_2_lb_dist = []

        for index, d in enumerate(self.date_list):
            temp_before_encoding = self.before_encoding_list[index]
            for flowBand, sorting_sation_index in temp_before_encoding['encoding_flow_sorting_sation'].items():
                for flow in flowBand.flow_list:
                    date.append(d)
                    temp_destination = flow.destination
                    temp_travel_level = flow.travel_level
                    temp_zone = flow.zone
                    temp_loads = flow.loads
                    temp_before_ss_index = sorting_sation_index
                    temp_before_lb_index = temp_before_encoding['encoding_flow_loading_berth'][flowBand]
                    temp_before_ss_coor = self.model.sorting_sation_set.sorting_sations[temp_before_ss_index].coordinate
                    temp_before_lb_coor = self.model.loading_berth_set.loading_berths[temp_before_lb_index].coordinate

                    # distance
                    temp_before_main_line_dist = self.model.main_line_distance_list[temp_before_ss_index]
                    temp_before_ss_2_sa_dist = \
                        self.model.sorting_sation_2_storage_area_distance_matrix[temp_before_ss_index][
                            temp_before_lb_index]
                    temp_before_sa_2_lb_dist = \
                        self.model.storage_area_2_loading_berth_distance_matrix[temp_before_lb_index][
                            temp_before_lb_index]

                    destination.append(temp_destination)
                    travel_level.append(temp_travel_level)
                    zone.append(temp_zone)
                    loads.append(temp_loads)
                    before_ss_index.append(temp_before_ss_index)
                    before_ss_coor.append(temp_before_ss_coor.output())
                    before_lb_index.append(temp_before_lb_index)
                    before_lb_coor.append(temp_before_lb_coor.output())
                    # distance
                    before_main_line_dist.append(temp_before_main_line_dist)
                    before_ss_2_sa_dist.append(temp_before_ss_2_sa_dist)
                    before_sa_2_lb_dist.append(temp_before_sa_2_lb_dist)

        for index, d in enumerate(['all date']):
            temp_after_encoding = self.encoding
            for flowBand, sorting_sation_index in temp_after_encoding['encoding_flow_sorting_sation'].items():
                for flow in flowBand.flow_list:
                    date.append(d)
                    temp_destination = flow.destination
                    temp_travel_level = flow.travel_level
                    temp_zone = flow.zone
                    temp_loads = flow.loads
                    temp_after_ss_index = sorting_sation_index
                    temp_after_lb_index = temp_after_encoding['encoding_flow_loading_berth'][flowBand]
                    temp_after_ss_coor = self.model.sorting_sation_set.sorting_sations[temp_after_ss_index].coordinate
                    temp_after_lb_coor = self.model.loading_berth_set.loading_berths[temp_after_lb_index].coordinate

                    # distance
                    temp_after_main_line_dist = self.model.main_line_distance_list[temp_after_ss_index]
                    temp_after_ss_2_sa_dist = \
                        self.model.sorting_sation_2_storage_area_distance_matrix[temp_after_ss_index][
                            temp_after_lb_index]
                    temp_after_sa_2_lb_dist = \
                        self.model.storage_area_2_loading_berth_distance_matrix[temp_after_lb_index][
                            temp_after_lb_index]

                    destination.append(temp_destination)
                    travel_level.append(temp_travel_level)
                    zone.append(temp_zone)
                    loads.append(temp_loads)
                    before_ss_index.append(temp_after_ss_index)
                    before_ss_coor.append(temp_after_ss_coor.output())
                    before_lb_index.append(temp_after_lb_index)
                    before_lb_coor.append(temp_after_lb_coor.output())
                    # distance
                    before_main_line_dist.append(temp_after_main_line_dist)
                    before_ss_2_sa_dist.append(temp_after_ss_2_sa_dist)
                    before_sa_2_lb_dist.append(temp_after_sa_2_lb_dist)
        self.comprea_info_encoding['date'] = date
        self.comprea_info_encoding['destination'] = destination
        self.comprea_info_encoding['travel_level'] = travel_level
        self.comprea_info_encoding['zone'] = zone
        self.comprea_info_encoding['loads'] = loads

        self.comprea_info_encoding['ss_index'] = before_ss_index
        self.comprea_info_encoding['ss_coor'] = before_ss_coor
        self.comprea_info_encoding['main_line_dist'] = before_main_line_dist
        self.comprea_info_encoding['lb_index'] = before_lb_index
        self.comprea_info_encoding['lb_coor'] = before_lb_coor
        self.comprea_info_encoding['ss_2_sa_dist'] = before_ss_2_sa_dist
        self.comprea_info_encoding['sa_2_lb_dist'] = before_sa_2_lb_dist

        temp_comprea_info_encoding = copy.copy(self.comprea_info_encoding)
        temp_date = copy.copy(list(set(date)))
        all_date = 'all date'
        temp_date.remove(all_date)
        temp_date.sort()
        all_df = copy.copy(temp_comprea_info_encoding[temp_comprea_info_encoding['date'] == all_date])
        all_df.rename(columns={'loads': 'static_loads', 'date': 'static',
                               'ss_index': 'static_ss_index', 'ss_coor': 'static_ss_coor',
                               'main_line_dist': 'static_main_line_dist',
                               'lb_index': 'static_lb_index', 'lb_coor': 'static_lb_coor',
                               'ss_2_sa_dist': 'static_ss_2_sa_dist',
                               'sa_2_lb_dist': 'static_sa_2_lb_dist'
                               }, inplace=True)
        all_df.drop(columns='zone', inplace=True)
        comprea_info_encoding = pd.DataFrame()

        def get_list(s):
            return list(s)

        all_df = all_df.groupby(['static', 'travel_level', 'destination']). \
            agg({'static_loads': 'sum',
                 'static_ss_index': get_list, 'static_ss_coor': get_list,
                 'static_lb_index': get_list, 'static_lb_coor': get_list,
                 'static_main_line_dist': get_list,
                 'static_ss_2_sa_dist': get_list, 'static_sa_2_lb_dist': get_list}).reset_index()

        for d in temp_date:
            temp_df = copy.copy(temp_comprea_info_encoding[temp_comprea_info_encoding['date'] == d])
            temp_df = temp_df.groupby(['date', 'travel_level', 'zone', 'destination']). \
                agg({'loads': get_list,
                     'ss_index': get_list, 'ss_coor': get_list,
                     'lb_index': get_list, 'lb_coor': get_list,
                     'main_line_dist': get_list,
                     'ss_2_sa_dist': get_list, 'sa_2_lb_dist': get_list}).reset_index()
            temp_df = pd.merge(temp_df, all_df, how='left', on=['destination', 'travel_level'])
            comprea_info_encoding = comprea_info_encoding.append(temp_df)
        comprea_info_encoding.reset_index(drop=True, inplace=True)
        if label == True:
            comprea_info_encoding.to_csv(self.data.output_filefolder + 'comprea_info_encoding.csv', index=False,
                                         encoding='gbk')
        self.set_date_loads()
        return self.comprea_info_encoding

    def set_no_NC_figure(self, label=True):
        def set_date(s):
            if '-' in s:
                temps = s.split('-')
                res = str(temps[1] + temps[2])
                res = (res)[:-2]
                return res
            else:
                return s

        date = [set_date(str(d)) for d in self.comprea_info_fit["date"]]
        loads = copy.copy(self.loads_list[:-1])
        loads = [_ / CONSTDATA.kg_t for _ in loads]
        mean_loads = np.mean(loads[:-1])
        mean_loads_list = [mean_loads for _ in date]
        fixed = [_ * CONSTDATA.before_main_line_distance / CONSTDATA.km_m for _ in loads]
        before_main = self.comprea_info_fit["before main_line"] / CONSTDATA.km_m
        before_ss_2_sa = self.comprea_info_fit["before sorting_sation_2_storage_area"] / CONSTDATA.km_m
        before_sa_2_lb = self.comprea_info_fit["before storage_area_2_loading_berth"] / CONSTDATA.km_m
        after_main = self.comprea_info_fit["after main_line"] / CONSTDATA.km_m
        after_ss_2_sa = self.comprea_info_fit["after sorting_sation_2_storage_area"] / CONSTDATA.km_m
        after_sa_2_lb = self.comprea_info_fit["after storage_area_2_loading_berth"] / CONSTDATA.km_m

        ori_main = self.comprea_info_fit['origin main']
        ori_ss_2_sa = self.comprea_info_fit['origin ss_2_sa']
        ori_sa_2_lb = self.comprea_info_fit['origin sa_2_lb']

        mod_main = self.comprea_info_fit['modified main']
        mod_ss_2_sa = self.comprea_info_fit['modified ss_2_sa']
        mod_sa_2_lb = self.comprea_info_fit['modified sa_2_lb']

        fig = plt.figure()
        ax1 = fig.add_subplot(2, 2, 1)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        ax2 = fig.add_subplot(2, 2, 2)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        ax3 = fig.add_subplot(2, 2, 3)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        ax4 = fig.add_subplot(2, 2, 4)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

        ax1.plot(date, loads, 'ko--', label='loads', linewidth=2.0, ms=1)
        ax1.plot(date, mean_loads_list, 'g--', label='mean loads', linewidth=2.0, ms=1)
        ax1.legend(loc='lower left', fontsize=12)
        ax1.set_title('loads duing ' + date[0] + '-' + date[-2], fontsize=12)
        # ax1.set_xlabel('date',fontsize=12)
        ax1.set_ylabel('loads (t)', fontsize=12)

        ax2.plot(date, before_main, 'ro-', label='dynamic', linewidth=2.0, ms=1)
        ax2.plot(date, after_main, 'ko--', label='static', linewidth=2.0, ms=1)
        ax2.plot(date, ori_main, 'bo--', label='original', linewidth=2.0, ms=1)
        ax2.plot(date, mod_main, 'yo--', label='modified', linewidth=2.0, ms=1)
        ax2.plot(date, fixed, 'go--', label='fixed', linewidth=2.0, ms=1)
        ax2.legend(loc='lower left', fontsize=12)
        ax2.set_title('main line distance', fontsize=12)
        # ax2.set_xlabel('date',fontsize=12)
        ax2.set_ylabel('weight_distance (t·km)', fontsize=12)

        ax3.plot(date, before_ss_2_sa, 'ro-', label='dynamic', linewidth=2.0, ms=1)
        ax3.plot(date, after_ss_2_sa, 'ko--', label='static', linewidth=2.0, ms=1)
        ax3.plot(date, ori_ss_2_sa, 'bo--', label='original', linewidth=2.0, ms=1)
        ax3.plot(date, mod_ss_2_sa, 'yo--', label='modified', linewidth=2.0, ms=1)
        ax3.legend(loc='lower left', fontsize=12)
        ax3.set_title('sorting sation to storage area distance', fontsize=12)
        # ax3.set_xlabel('date',fontsize=12)
        ax3.set_ylabel('distance (km)', fontsize=12)

        # ax4.plot(date, before_sa_2_lb, 'ro-', label='dynamic', linewidth=2.0, ms=1)
        # ax4.plot(date, after_sa_2_lb, 'ko--', label='static', linewidth=2.0, ms=1)
        # ax4.plot(date, ori_sa_2_lb, 'bo--', label='original', linewidth=2.0, ms=1)
        # ax4.plot(date, mod_sa_2_lb, 'yo--', label='modified', linewidth=2.0, ms=1)
        # ax4.legend(loc='lower left', fontsize=12)
        # ax4.set_title('storage area to loading berth distance', fontsize=12)
        # # ax4.set_xlabel('date',fontsize=12)
        # ax4.set_ylabel('ditance (km)', fontsize=12)

        # cost

        before_cost = [
            i * CONSTDATA.main_line_cost_rate + j * CONSTDATA.ss_2_sa_cost_rate + k * CONSTDATA.sa_2_lb_cost_rate
            for i, j, k in zip(before_main, before_ss_2_sa, before_sa_2_lb)]
        after_cost = [
            i * CONSTDATA.main_line_cost_rate + j * CONSTDATA.ss_2_sa_cost_rate + k * CONSTDATA.sa_2_lb_cost_rate
            for i, j, k in zip(after_main, after_ss_2_sa, after_sa_2_lb)]
        ori_cost = [
            i * CONSTDATA.main_line_cost_rate + j * CONSTDATA.ss_2_sa_cost_rate + k * CONSTDATA.sa_2_lb_cost_rate
            for i, j, k in zip(ori_main, ori_ss_2_sa, ori_sa_2_lb)]
        mod_cost = [
            i * CONSTDATA.main_line_cost_rate + j * CONSTDATA.ss_2_sa_cost_rate + k * CONSTDATA.sa_2_lb_cost_rate
            for i, j, k in zip(mod_main, mod_ss_2_sa, mod_sa_2_lb)]
        ax4.plot(date, before_cost, 'ro-', label='dynamic', linewidth=2.0, ms=1)
        ax4.plot(date, after_cost, 'ko--', label='static', linewidth=2.0, ms=1)
        ax4.plot(date, ori_cost, 'bo--', label='original', linewidth=2.0, ms=1)
        ax4.plot(date, mod_cost, 'yo--', label='modified', linewidth=2.0, ms=1)
        ax4.legend(loc='lower left', fontsize=12)
        ax4.set_title('cost of all plans', fontsize=12)
        ax4.set_ylabel('cost (yuan)', fontsize=12)

        if label == True:
            plt.show()

    def plot_no_NC_zone_loads(self, label=True):
        temp_zone_loads = pd.pivot_table(self.comprea_info_encoding, values='loads',
                                         index=['date', 'travel_level', 'zone'],
                                         fill_value=0, aggfunc='sum')
        temp_zone_loads.reset_index(inplace=True)
        temp_zone_loads.sort_values(by=['loads'], ascending=False, inplace=True)
        temp_zone_loads.sort_values(by=['date'], ascending=True, inplace=True)
        # print(temp_zone_loads)
        # temp_zone_loads.to_csv('temp_zone_loads.csv', index=False, encoding='gbk')
        travel_level1_zone_loads = copy.copy(temp_zone_loads[temp_zone_loads['travel_level'] == '一级运输'])
        travel_level2_zone_loads = copy.copy(temp_zone_loads[temp_zone_loads['travel_level'] == '二级运输'])
        travel_level3_zone_loads = copy.copy(temp_zone_loads[temp_zone_loads['travel_level'] == '三级运输'])
        temp_travel_level3_zone_loads = pd.pivot_table(travel_level3_zone_loads, values='loads',
                                                       index=['date', 'travel_level'],
                                                       fill_value=0, aggfunc='sum')
        temp_travel_level3_zone_loads.reset_index(inplace=True)
        temp_travel_level3_zone_loads['zone'] = 'K775Y&755Y'
        travel_level3_zone_loads = temp_travel_level3_zone_loads[travel_level3_zone_loads.columns]
        travel_level23_zone_loads = travel_level2_zone_loads.append(travel_level3_zone_loads)

        def get_n_index(n, l):
            if n not in l:
                return 0
            else:
                return l.index(n) + 1

        def set_index(travel_level_zone_loads):
            result_travel_level_zone_loads = pd.DataFrame()
            date_list = list(travel_level_zone_loads['date'].unique())
            date_list.sort()
            for date in date_list:
                temp_travel_level_zone_loads = copy.copy(
                    travel_level_zone_loads[travel_level_zone_loads['date'] == date])
                loads_list = list(temp_travel_level_zone_loads['loads'])
                loads_list.sort(reverse=True)
                temp_travel_level_zone_loads['sequence'] = \
                    temp_travel_level_zone_loads['loads'].apply(lambda x: get_n_index(x, loads_list))
                result_travel_level_zone_loads = \
                    result_travel_level_zone_loads.append(copy.copy(temp_travel_level_zone_loads))
            return result_travel_level_zone_loads

        def get_list(s):
            return list(s)

        travel_level1_zone_loads = set_index(travel_level1_zone_loads)
        travel_level23_zone_loads = set_index(travel_level23_zone_loads)

        travel_level1_zone_loads_seq = pd.pivot_table(travel_level1_zone_loads, values=['sequence', 'loads'],
                                                      index=['travel_level', 'zone'], fill_value=0, aggfunc=get_list)
        travel_level23_zone_loads_seq = pd.pivot_table(travel_level23_zone_loads, values=['sequence', 'loads'],
                                                       index=['travel_level', 'zone'], fill_value=0, aggfunc=get_list)
        travel_level1_zone_loads_seq.sort_values(by='loads', inplace=True)
        travel_level23_zone_loads_seq.sort_values(by='loads', inplace=True)
        travel_level_zone_loads = travel_level1_zone_loads_seq.append(travel_level23_zone_loads_seq)
        travel_level_zone_loads.reset_index(inplace=True)
        travel_level_zone_loads['mean_loads'] = travel_level_zone_loads['loads']. \
            apply(lambda x: sum(list(x)) / len(list(x)))
        all_mean_loads = sum(travel_level_zone_loads['mean_loads'])
        travel_level_zone_loads['loads_rate'] = travel_level_zone_loads['mean_loads']. \
            apply(lambda x: x / all_mean_loads)
        travel_level_zone_loads['mean_seq'] = travel_level_zone_loads['sequence']. \
            apply(lambda x: sum(list(x)) / len(list(x)))

        def set_describe(r, tl, z, l):
            s = str(round(r * 100, 2)) + '%' + tl + ' ' + z + ' ' + str(round(l, 2))
            return s

        travel_level_zone_loads['describe'] = travel_level_zone_loads. \
            apply(lambda row: set_describe(row['loads_rate'], row['travel_level'], row['zone'], row['mean_loads']),
                  axis=1)

        # travel_level_zone_loads.to_csv(self.data.output_filefolder+'travel_level_zone_loads.csv', index=False, encoding='gbk')

        # figure
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

        recipe = list(travel_level_zone_loads['describe'])

        data = list(travel_level_zone_loads['mean_loads'])

        """
        参数wedgeprops以字典形式传递，设置饼图边界的相关属性，例如圆环宽度0.5
        饼状图默认从x轴正向沿逆时针绘图，参数startangle可指定新的角（例如负40度）度起画
        """
        wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-8)

        # 创建字典bbox_props，设置文本框的边框样式(boxstyle：方框，pad设置方框尺寸)、前景色(fc)为白色(w)、边框颜色(ec)为黑色(k)、线粗(lw)为0.72
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)

        """
        参数集kw以字典形式传递，包含一系列用于绘图标注的指定参数
        xycoords用于指定点xy的坐标环境，xycoords='data'表示沿用被注释的对象所采用的坐标系（默认设置）
        textcoords用于指定点xytext的坐标环境，textcoords='data'表示沿用被注释的对象所采用的坐标系（默认设置）
        参数arrowprops以字典形式传递，用于控制箭头的诸多属性，如箭头类型(arrowstyle)、箭头连接时的弯曲程度(connectionstyle)
        """
        kw = dict(xycoords='data', textcoords='data',
                  arrowprops=dict(arrowstyle="-"),  # connectionstyle="arc,angleA=-90,angleB=0,armA=30,armB=30,rad=5"),
                  bbox=bbox_props, zorder=0, va="center")

        for i, p in enumerate(wedges):  # 遍历每一个扇形

            ang = (p.theta2 - p.theta1) / 2. + p.theta1  # 锁定扇形夹角的中间位置，对应的度数为ang

            # np.deg2rad(x)将度数x转为弧度(x*pi)/180
            y = np.sin(np.deg2rad(ang))  # np.sin()求正弦
            x = np.cos(np.deg2rad(ang))  # np.cos()求余弦

            """
            np.sign()符号函数：大于0返回1.0，小于0返回-1.0，等于0返回0.0
            参数horizontalalignment用于设置垂直对齐方式，可选参数：left、right、center
            当余弦值x大于0（即标签在饼图右侧时，按框左侧对齐）时，horizontalalignment="left"
            当余弦值x小于0（即标签在饼图左侧时，按框右侧对齐）时，horizontalalignment="right"
            """
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]

            connectionstyle = "angle,angleA=0,angleB={}".format(ang)  # 参数connectionstyle用于控制箭头连接时的弯曲程度
            kw["arrowprops"].update({"connectionstyle": connectionstyle})  # 将connectionstyle更新至参数集kw的参数arrowprops中

            """
            用一个箭头/横线指向要注释的地方，再写上一段话的行为，叫做annotate
            ax.annotate()用于对已绘制的图形做标注
            recipe[i]是第i个注释文本
            size设置字体大小
            xy=(x1, y1)表示在给定的xycoords中，被注释对象的坐标点
            xytext=(x2, y2)表示在给定的textcoords中，注释文本的坐标点
            """
            ax.annotate(recipe[i], size=15, xy=(x, y), xytext=(1.2 * np.sign(x), 1.6 * y),
                        horizontalalignment=horizontalalignment, **kw)

        ax.set_title("travel level zone loads rate", fontsize=25)
        if label == True:
            plt.show()

    def analysis_no_NC_zone_loads(self, label=True):
        temp_zone_loads = pd.pivot_table(self.comprea_info_encoding, values='loads',
                                         index=['date', 'travel_level', 'zone'],
                                         fill_value=0, aggfunc='sum')
        temp_zone_loads.reset_index(inplace=True)
        temp_zone_loads.sort_values(by=['loads'], ascending=False, inplace=True)
        temp_zone_loads.sort_values(by=['date'], ascending=True, inplace=True)
        temp_travel_level1_zone_loads = copy.copy(temp_zone_loads[temp_zone_loads['travel_level'] == '一级运输'])
        temp_travel_level2_zone_loads = copy.copy(temp_zone_loads[temp_zone_loads['travel_level'] == '二级运输'])
        temp_travel_level3_zone_loads = copy.copy(temp_zone_loads[temp_zone_loads['travel_level'] == '三级运输'])
        temp_travel_level3_zone_loads['zone'] = ''  # 'K775Y&755Y')
        temp_zone_loads = \
            pd.concat([temp_travel_level1_zone_loads, temp_travel_level2_zone_loads, temp_travel_level3_zone_loads])
        temp_zone_loads['zone'] = temp_zone_loads['travel_level'] + temp_zone_loads['zone']

        date_list = list(temp_zone_loads['date'].unique())
        zone_list = list(temp_zone_loads['zone'].unique())

        temp_zone_loads = pd.pivot_table(temp_zone_loads, values='loads', index='date', columns='zone',
                                         fill_value=0, aggfunc='sum').reset_index()
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        for zone in zone_list:
            loads = copy.copy(list(temp_zone_loads[zone]))
            loads = [_ / CONSTDATA.kg_t for _ in loads]
            plt.plot(date_list[:-1], loads[:-1], 'o-', label=zone, linewidth=2.0, ms=1.0)
        plt.yticks(fontsize=15)
        plt.legend(loc='best', fontsize=15)
        plt.ylabel('loads (t)', fontsize=15)
        plt.title('travel level zone loads', fontsize=20)
        if label == True:
            plt.show()

    def no_NC_plots(self):
        self.set_day_sort_plan()
        self.set_compare_encoding()
        self.set_compare_fit()
        self.set_no_NC_figure()
        self.plot_no_NC_zone_loads()
        self.analysis_no_NC_zone_loads()

    # consider NC
    def NC_set_day_sort_plan(self, duration=0):
        self.NC_record_date_list = []
        flow_info = FLOWINFO(self.data, False, False)
        model = MODEL(flow_info)
        algs = ALGS(model, True)
        self.NC_encoding = algs.model.encoding
        self.NC_fit = algs.model.fit
        calculateCost = CALCULATECOST(model)
        self.NC_ori_fit = calculateCost.set_ori_cost()
        self.NC_mod_fit = calculateCost.set_mod_cost()
        NC_encoding_record = algs.model.set_encoding_record()
        for index, d in enumerate(self.NC_date_list):
            ind = index + 1
            if duration != 0:
                if ind % duration == 0 and ind != 0 and ind != (len(self.NC_date_list)):
                    date_list = self.NC_date_list[ind - duration:ind]
                elif ind == (len(self.NC_date_list)) and len(self.NC_date_list) > duration:
                    date_list = self.NC_date_list[ind - duration:ind]
                else:
                    continue
            else:
                date_list = [d]
            self.NC_record_date_list.append(date_list)
            temp_input_data = copy.copy(self.data)
            temp_input_data.set_date(date_list)
            flow_info = FLOWINFO(temp_input_data, False, False)
            model = MODEL(flow_info)
            algs = ALGS(model, True)
            self.NC_before_encoding_list.append(algs.model.encoding)
            self.NC_before_fit_list.append(algs.model.fit)
            algs = ALGS(model, True, self.NC_encoding, NC_encoding_record)
            self.NC_after_encoding_list.append(algs.model.encoding)
            self.NC_after_fit_list.append(algs.model.fit)
            calculateCost = CALCULATECOST(model)
            self.NC_ori_fit_list.append(calculateCost.set_ori_cost())
            self.NC_mod_fit_list.append(calculateCost.set_mod_cost())

    def NC_set_compare_fit(self, label=True):
        self.NC_comprea_info_fit = pd.DataFrame()
        temp_record_list = copy.copy(self.NC_record_date_list)
        # temp_record_list.append('all')
        self.NC_comprea_info_fit['date'] = temp_record_list
        before_main = []
        before_ss_2_sa = []
        before_sa_2_lb = []
        before_NC_lb_2_sa = []
        before_NC_sa_2_lb = []

        after_main = []
        after_ss_2_sa = []
        after_sa_2_lb = []
        after_NC_lb_2_sa = []
        after_NC_sa_2_lb = []

        origin_main = []
        origin_ss_2_sa = []
        origin_sa_2_lb = []
        origin_NC_lb_2_sa = []
        origin_NC_sa_2_lb = []

        modified_main = []
        modified_ss_2_sa = []
        modified_sa_2_lb = []
        modified_NC_lb_2_sa = []
        modified_NC_sa_2_lb = []

        for index, fit in enumerate(self.NC_before_fit_list):
            before_main.append(fit['main_line'])
            before_ss_2_sa.append(fit['sorting_sation_2_storage_area'])
            before_sa_2_lb.append(fit['storage_area_2_loading_berth'])
            before_NC_lb_2_sa.append(fit['NC_loading_berth_2_storage_area'])
            before_NC_sa_2_lb.append(fit['NC_storage_area_2_loading_berth'])
            after_main.append(self.NC_after_fit_list[index]['main_line'])
            after_ss_2_sa.append(self.NC_after_fit_list[index]['sorting_sation_2_storage_area'])
            after_sa_2_lb.append(self.NC_after_fit_list[index]['storage_area_2_loading_berth'])
            after_NC_lb_2_sa.append(self.NC_after_fit_list[index]['NC_loading_berth_2_storage_area'])
            after_NC_sa_2_lb.append(self.NC_after_fit_list[index]['NC_storage_area_2_loading_berth'])

            origin_main.append(self.NC_ori_fit_list[index]['main_line_cost'])
            origin_ss_2_sa.append(self.NC_ori_fit_list[index]['ss_2_sa_cost'])
            origin_sa_2_lb.append(self.NC_ori_fit_list[index]['sa_2_lb_cost'])
            origin_NC_lb_2_sa.append(self.NC_ori_fit_list[index]['NC_lb_2_sa_cost'])
            origin_NC_sa_2_lb.append(self.NC_ori_fit_list[index]['NC_sa_2_lb_cost'])

            modified_main.append(self.NC_mod_fit_list[index]['main_line_cost'])
            modified_ss_2_sa.append(self.NC_mod_fit_list[index]['ss_2_sa_cost'])
            modified_sa_2_lb.append(self.NC_mod_fit_list[index]['sa_2_lb_cost'])
            modified_NC_lb_2_sa.append(self.NC_mod_fit_list[index]['NC_lb_2_sa_cost'])
            modified_NC_sa_2_lb.append(self.NC_mod_fit_list[index]['NC_sa_2_lb_cost'])

        # before_main.append(self.NC_fit['main_line'])
        # before_ss_2_sa.append(self.NC_fit['sorting_sation_2_storage_area'])
        # before_sa_2_lb.append(self.NC_fit['storage_area_2_loading_berth'])
        # before_NC_lb_2_sa.append(self.NC_fit['NC_loading_berth_2_storage_area'])
        # before_NC_sa_2_lb.append(self.NC_fit['NC_storage_area_2_loading_berth'])
        # after_main.append(self.NC_fit['main_line'])
        # after_ss_2_sa.append(self.NC_fit['sorting_sation_2_storage_area'])
        # after_sa_2_lb.append(self.NC_fit['storage_area_2_loading_berth'])
        # after_NC_lb_2_sa.append(self.NC_fit['NC_loading_berth_2_storage_area'])
        # after_NC_sa_2_lb.append(self.NC_fit['NC_storage_area_2_loading_berth'])
        self.NC_comprea_info_fit['before main_line'] = before_main
        self.NC_comprea_info_fit['before sorting_sation_2_storage_area'] = before_ss_2_sa
        self.NC_comprea_info_fit['before storage_area_2_loading_berth'] = before_sa_2_lb
        self.NC_comprea_info_fit['before NC_loading_berth_2_storage_area'] = before_NC_lb_2_sa
        self.NC_comprea_info_fit['before NC_storage_area_2_loading_berth'] = before_NC_sa_2_lb
        self.NC_comprea_info_fit['after main_line'] = after_main
        self.NC_comprea_info_fit['after sorting_sation_2_storage_area'] = after_ss_2_sa
        self.NC_comprea_info_fit['after storage_area_2_loading_berth'] = after_sa_2_lb
        self.NC_comprea_info_fit['after NC_loading_berth_2_storage_area'] = after_NC_lb_2_sa
        self.NC_comprea_info_fit['after NC_storage_area_2_loading_berth'] = after_NC_sa_2_lb

        self.NC_comprea_info_fit['origin main_line'] = origin_main
        self.NC_comprea_info_fit['origin sorting_sation_2_storage_area'] = origin_ss_2_sa
        self.NC_comprea_info_fit['origin storage_area_2_loading_berth'] = origin_sa_2_lb
        self.NC_comprea_info_fit['origin NC_loading_berth_2_storage_area'] = origin_NC_lb_2_sa
        self.NC_comprea_info_fit['origin NC_storage_area_2_loading_berth'] = origin_NC_sa_2_lb

        self.NC_comprea_info_fit['modified main_line'] = modified_main
        self.NC_comprea_info_fit['modified sorting_sation_2_storage_area'] = modified_ss_2_sa
        self.NC_comprea_info_fit['modified storage_area_2_loading_berth'] = modified_sa_2_lb
        self.NC_comprea_info_fit['modified NC_loading_berth_2_storage_area'] = modified_NC_lb_2_sa
        self.NC_comprea_info_fit['modified NC_storage_area_2_loading_berth'] = modified_NC_sa_2_lb
        # print(len(self.NC_comprea_info_fit))
        # print(len(self.NC_loads_NC_list))
        # print(len(self.NC_loads_no_NC_list))
        self.NC_comprea_info_fit['NC loads'] = self.NC_loads_NC_list[:-1]
        self.NC_comprea_info_fit['no NC loads'] = self.NC_loads_no_NC_list[:-1]
        self.NC_comprea_info_fit['loads'] = self.NC_comprea_info_fit['NC loads'] + \
                                            self.NC_comprea_info_fit['no NC loads']
        if label == True:
            self.NC_comprea_info_fit.to_csv(self.data.output_filefolder + 'NC_comprea_info_fit.csv', index=False)
        return self.NC_comprea_info_fit

    def NC_set_date_loads(self):
        self.NC_date_loads = {}
        temp_date_loads = pd.pivot_table(self.NC_comprea_info_encoding,
                                         values='loads', index='date',
                                         fill_value=0, aggfunc='sum')
        temp_date_loads.reset_index(inplace=True)
        self.NC_date_loads = {k: v for k, v in zip(temp_date_loads['date'], temp_date_loads['loads'])}
        temp_date_loads.sort_values(by='date', inplace=True)
        self.NC_loads_list = list(copy.copy(temp_date_loads['loads']))
        return self.NC_date_loads

    def NC_set_date_loads_no_NC(self):
        self.NC_date_loads_no_NC = {}
        temp_date_loads_no_NC = pd.pivot_table(self.NC_comprea_info_encoding,
                                               values='loads_no_NC', index='date',
                                               fill_value=0, aggfunc='sum')
        temp_date_loads_no_NC.reset_index(inplace=True)
        self.NC_date_loads_no_NC = {k: v for k, v in
                                    zip(temp_date_loads_no_NC['date'], temp_date_loads_no_NC['loads_no_NC'])}
        temp_date_loads_no_NC.sort_values(by='date', inplace=True)
        self.NC_loads_no_NC_list = list(copy.copy(temp_date_loads_no_NC['loads_no_NC']))
        return self.NC_date_loads_no_NC

    def NC_set_date_loads_NC(self):
        self.NC_date_loads_NC = {}
        temp_date_loads_NC = pd.pivot_table(self.NC_comprea_info_encoding,
                                            values='loads_NC', index='date',
                                            fill_value=0, aggfunc='sum')
        temp_date_loads_NC.reset_index(inplace=True)
        self.NC_date_loads_NC = {k: v for k, v in zip(temp_date_loads_NC['date'], temp_date_loads_NC['loads_NC'])}
        temp_date_loads_NC.sort_values(by='date', inplace=True)
        self.NC_loads_NC_list = list(copy.copy(temp_date_loads_NC['loads_NC']))
        return self.NC_date_loads_NC

    def NC_set_compare_encoding(self, label=True):
        self.NC_comprea_info_encoding = pd.DataFrame()
        date = []
        destination = []
        travel_level = []
        zone = []
        loads = []
        loads_NC = []
        loads_no_NC = []

        before_ss_index = []
        before_ss_coor = []
        before_main_line_dist = []
        before_lb_index = []
        before_lb_coor = []
        before_ss_2_sa_dist = []
        before_sa_2_lb_dist = []

        for index, d in enumerate(self.NC_date_list):
            temp_before_encoding = self.NC_before_encoding_list[index]
            for flowBand, sorting_sation_index in temp_before_encoding['encoding_flow_sorting_sation'].items():
                for flow in flowBand.flow_list:
                    date.append(d)
                    temp_destination = flow.destination
                    temp_travel_level = flow.travel_level
                    temp_zone = flow.zone
                    temp_loads = flow.loads
                    temp_loads_NC = flow.loads_NC
                    temp_loads_no_NC = flow.loads_no_NC

                    temp_before_ss_index = sorting_sation_index
                    temp_before_lb_index = temp_before_encoding['encoding_flow_loading_berth'][flowBand]
                    temp_before_ss_coor = self.NC_model.sorting_sation_set.sorting_sations[
                        temp_before_ss_index].coordinate
                    temp_before_lb_coor = self.NC_model.loading_berth_set.loading_berths[
                        temp_before_lb_index].coordinate

                    # distance
                    temp_before_main_line_dist = self.NC_model.main_line_distance_list[temp_before_ss_index]
                    temp_before_ss_2_sa_dist = \
                        self.NC_model.sorting_sation_2_storage_area_distance_matrix[temp_before_ss_index][
                            temp_before_lb_index]
                    temp_before_sa_2_lb_dist = \
                        self.NC_model.storage_area_2_loading_berth_distance_matrix[temp_before_lb_index][
                            temp_before_lb_index]

                    destination.append(temp_destination)
                    travel_level.append(temp_travel_level)
                    zone.append(temp_zone)
                    loads.append(temp_loads)
                    loads_NC.append(temp_loads_NC)
                    loads_no_NC.append(temp_loads_no_NC)
                    before_ss_index.append(temp_before_ss_index)
                    before_ss_coor.append(temp_before_ss_coor.output())
                    before_lb_index.append(temp_before_lb_index)
                    before_lb_coor.append(temp_before_lb_coor.output())
                    # distance
                    before_main_line_dist.append(temp_before_main_line_dist)
                    before_ss_2_sa_dist.append(temp_before_ss_2_sa_dist)
                    before_sa_2_lb_dist.append(temp_before_sa_2_lb_dist)

        for index, d in enumerate(['all date']):
            temp_after_encoding = self.NC_encoding
            for flowBand, sorting_sation_index in temp_after_encoding['encoding_flow_sorting_sation'].items():
                for flow in flowBand.flow_list:
                    date.append(d)
                    temp_destination = flow.destination
                    temp_travel_level = flow.travel_level
                    temp_zone = flow.zone
                    temp_loads = flow.loads
                    temp_loads_NC = flow.loads_NC
                    temp_loads_no_NC = flow.loads_no_NC

                    temp_after_ss_index = sorting_sation_index
                    temp_after_lb_index = temp_after_encoding['encoding_flow_loading_berth'][flowBand]
                    temp_after_ss_coor = self.NC_model.sorting_sation_set.sorting_sations[
                        temp_after_ss_index].coordinate
                    temp_after_lb_coor = self.NC_model.loading_berth_set.loading_berths[temp_after_lb_index].coordinate

                    # distance
                    temp_after_main_line_dist = self.NC_model.main_line_distance_list[temp_after_ss_index]
                    temp_after_ss_2_sa_dist = \
                        self.NC_model.sorting_sation_2_storage_area_distance_matrix[temp_after_ss_index][
                            temp_after_lb_index]
                    temp_after_sa_2_lb_dist = \
                        self.NC_model.storage_area_2_loading_berth_distance_matrix[temp_after_lb_index][
                            temp_after_lb_index]

                    destination.append(temp_destination)
                    travel_level.append(temp_travel_level)
                    zone.append(temp_zone)
                    loads.append(temp_loads)
                    loads_NC.append(temp_loads_NC)
                    loads_no_NC.append(temp_loads_no_NC)
                    before_ss_index.append(temp_after_ss_index)
                    before_ss_coor.append(temp_after_ss_coor.output())
                    before_lb_index.append(temp_after_lb_index)
                    before_lb_coor.append(temp_after_lb_coor.output())
                    # distance
                    before_main_line_dist.append(temp_after_main_line_dist)
                    before_ss_2_sa_dist.append(temp_after_ss_2_sa_dist)
                    before_sa_2_lb_dist.append(temp_after_sa_2_lb_dist)
        self.NC_comprea_info_encoding['date'] = date
        self.NC_comprea_info_encoding['destination'] = destination
        self.NC_comprea_info_encoding['travel_level'] = travel_level
        self.NC_comprea_info_encoding['zone'] = zone
        self.NC_comprea_info_encoding['loads'] = loads
        self.NC_comprea_info_encoding['loads_NC'] = loads_NC
        self.NC_comprea_info_encoding['loads_no_NC'] = loads_no_NC

        self.NC_comprea_info_encoding['ss_index'] = before_ss_index
        self.NC_comprea_info_encoding['ss_coor'] = before_ss_coor
        self.NC_comprea_info_encoding['main_line_dist'] = before_main_line_dist
        self.NC_comprea_info_encoding['lb_index'] = before_lb_index
        self.NC_comprea_info_encoding['lb_coor'] = before_lb_coor
        self.NC_comprea_info_encoding['ss_2_sa_dist'] = before_ss_2_sa_dist
        self.NC_comprea_info_encoding['sa_2_lb_dist'] = before_sa_2_lb_dist

        temp_comprea_info_encoding = copy.copy(self.NC_comprea_info_encoding)
        # date = [str(d)for d in date]
        # temp_date = copy.copy(list(set(date)))
        temp_date = copy.copy(list(set(date)))
        all_date = 'all date'
        temp_date.remove(all_date)
        temp_date.sort()
        all_df = copy.copy(temp_comprea_info_encoding[temp_comprea_info_encoding['date'] == all_date])
        all_df.rename(columns={'loads': 'static_loads', 'date': 'static',
                               'loads_NC': 'static_loads_NC', 'loads_no_NC': 'static_loads_no_NC',
                               'ss_index': 'static_ss_index', 'ss_coor': 'static_ss_coor',
                               'main_line_dist': 'static_main_line_dist',
                               'lb_index': 'static_lb_index', 'lb_coor': 'static_lb_coor',
                               'ss_2_sa_dist': 'static_ss_2_sa_dist',
                               'sa_2_lb_dist': 'static_sa_2_lb_dist'
                               }, inplace=True)
        all_df.drop(columns='zone', inplace=True)
        comprea_info_encoding = pd.DataFrame()

        def get_list(s):
            return list(s)

        all_df = all_df.groupby(['static', 'travel_level', 'destination']). \
            agg({'static_loads': 'sum', 'static_loads_no_NC': 'sum', 'static_loads_NC': 'sum',
                 'static_ss_index': get_list, 'static_ss_coor': get_list,
                 'static_lb_index': get_list, 'static_lb_coor': get_list,
                 'static_main_line_dist': get_list,
                 'static_ss_2_sa_dist': get_list, 'static_sa_2_lb_dist': get_list}).reset_index()

        for d in temp_date:
            temp_df = copy.copy(temp_comprea_info_encoding[temp_comprea_info_encoding['date'] == d])
            temp_df = temp_df.groupby(['date', 'travel_level', 'zone', 'destination']). \
                agg({'loads': get_list,
                     'ss_index': get_list, 'ss_coor': get_list,
                     'lb_index': get_list, 'lb_coor': get_list,
                     'main_line_dist': get_list,
                     'ss_2_sa_dist': get_list, 'sa_2_lb_dist': get_list}).reset_index()
            temp_df = pd.merge(temp_df, all_df, how='left', on=['destination', 'travel_level'])
            comprea_info_encoding = comprea_info_encoding.append(temp_df)
        comprea_info_encoding.reset_index(drop=True, inplace=True)
        if label == True:
            comprea_info_encoding.to_csv(self.data.output_filefolder + 'NC_comprea_info_encoding.csv', index=False,
                                         encoding='gbk')
        self.NC_set_date_loads()
        self.NC_set_date_loads_no_NC()
        self.NC_set_date_loads_NC()
        return self.NC_comprea_info_encoding

    def NC_set_ss_num(self):
        self.NC_date_before_ss_number = {}
        self.NC_date_after_ss_number = {}
        self.NC_date_origin_ss_number = {}
        self.NC_date_modified_ss_number = {}
        for index, date in enumerate(self.NC_date_list):
            self.NC_date_origin_ss_number[date] = self.NC_ori_fit_list[index]['ss_num']+3
            self.NC_date_modified_ss_number[date] = self.NC_mod_fit_list[index]['ss_num']
            self.NC_date_before_ss_number[date] = \
                len(set(self.NC_before_encoding_list[index]['encoding_flow_sorting_sation'].values()))
            temp_ss_number = []
            for i,j in self.NC_after_encoding_list[index]['encoding_flow_sorting_sation'].items():
                if i.loads> 0:
                    temp_ss_number.append(j)
            self.NC_date_after_ss_number[date] = len(set(temp_ss_number))
        # print()

    def set_NC_figure(self):
        def set_date(s):
            if '-' in s:
                temps = s.split('-')
                res = str(temps[1] + temps[2])
                res = (res)[:-2]
                return res
            else:
                return s

        date = [set_date(str(d)) for d in self.NC_comprea_info_fit["date"]]
        loads = copy.copy(self.NC_loads_list[:-1])
        loads = [_ / CONSTDATA.kg_t for _ in loads]
        loads_no_NC = copy.copy(self.NC_loads_no_NC_list[:-1])
        loads_no_NC = [_ / CONSTDATA.kg_t for _ in loads_no_NC]
        loads_NC = copy.copy(self.NC_loads_NC_list[:-1])
        loads_NC = [_ / CONSTDATA.kg_t for _ in loads_NC]

        mean_loads = np.mean(loads)
        mean_loads_list = [mean_loads for _ in date]
        mean_loads_no_NC = np.mean(loads_no_NC)
        mean_loads_no_NC_list = [mean_loads_no_NC for _ in date]
        mean_loads_NC = np.mean(loads_NC)
        mean_loads_NC_list = [mean_loads_NC for _ in date]

        fixed = [_ * CONSTDATA.before_main_line_distance / CONSTDATA.km_m for _ in loads_no_NC]
        before_main = self.NC_comprea_info_fit["before main_line"] / CONSTDATA.km_m
        before_ss_2_sa = self.NC_comprea_info_fit["before sorting_sation_2_storage_area"] / CONSTDATA.km_m
        before_sa_2_lb = self.NC_comprea_info_fit["before storage_area_2_loading_berth"] / CONSTDATA.km_m
        before_NC_lb_2_sa = self.NC_comprea_info_fit['before NC_loading_berth_2_storage_area'] / CONSTDATA.km_m
        before_NC_sa_2_lb = self.NC_comprea_info_fit['before NC_storage_area_2_loading_berth'] / CONSTDATA.km_m

        after_main = self.NC_comprea_info_fit["after main_line"] / CONSTDATA.km_m
        after_ss_2_sa = self.NC_comprea_info_fit["after sorting_sation_2_storage_area"] / CONSTDATA.km_m
        after_sa_2_lb = self.NC_comprea_info_fit["after storage_area_2_loading_berth"] / CONSTDATA.km_m
        after_NC_lb_2_sa = self.NC_comprea_info_fit['after NC_loading_berth_2_storage_area'] / CONSTDATA.km_m
        after_NC_sa_2_lb = self.NC_comprea_info_fit['after NC_storage_area_2_loading_berth'] / CONSTDATA.km_m

        ori_main = self.NC_comprea_info_fit['origin main_line']
        ori_ss_2_sa = self.NC_comprea_info_fit['origin sorting_sation_2_storage_area']
        ori_sa_2_lb = self.NC_comprea_info_fit['origin storage_area_2_loading_berth']
        ori_NC_lb_2_sa = self.NC_comprea_info_fit['origin NC_loading_berth_2_storage_area']
        ori_NC_sa_2_lb = self.NC_comprea_info_fit['origin NC_storage_area_2_loading_berth']

        mod_main = self.NC_comprea_info_fit['modified main_line']
        mod_ss_2_sa = self.NC_comprea_info_fit['modified sorting_sation_2_storage_area']
        mod_sa_2_lb = self.NC_comprea_info_fit['modified storage_area_2_loading_berth']
        mod_NC_lb_2_sa = self.NC_comprea_info_fit['modified NC_loading_berth_2_storage_area']
        mod_NC_sa_2_lb = self.NC_comprea_info_fit['modified NC_storage_area_2_loading_berth']

        before_main_cost = \
            [ml * CONSTDATA.main_line_per_power_per_dist_per_weight * CONSTDATA.electricity_price for ml in before_main]
        before_sa_2_lb_man_cost = \
            [CONSTDATA.driver_per_cost * sl / CONSTDATA.driver_per_speed / CONSTDATA.driver_per_period for sl in
             before_ss_2_sa]
        before_sa_2_lb_power_cost = \
            [CONSTDATA.electricity_price * CONSTDATA.forklift_power * sl / CONSTDATA.driver_per_speed for sl in
             before_ss_2_sa]
        before_NC_lb_2_sa_man_cost = \
            [CONSTDATA.driver_per_cost * sl / CONSTDATA.driver_per_speed / CONSTDATA.driver_per_period for sl in
             before_NC_lb_2_sa]
        before_NC_lb_2_sa_power_cost = \
            [CONSTDATA.electricity_price * CONSTDATA.forklift_power * sl / CONSTDATA.driver_per_speed for sl in
             before_NC_lb_2_sa]
        before_forklift_man_cost = [i + j for i, j in zip(before_sa_2_lb_man_cost, before_NC_lb_2_sa_man_cost)]
        before_forklift_poewr_cost = [i + j for i, j in zip(before_sa_2_lb_power_cost, before_NC_lb_2_sa_power_cost)]
        before_forklift_cost = [i + j for i, j in zip(before_forklift_man_cost, before_forklift_poewr_cost)]
        before_forklift_all_cost = [i + j for i, j in zip(before_main_cost, before_forklift_cost)]

        after_main_cost = \
            [ml * CONSTDATA.main_line_per_power_per_dist_per_weight * CONSTDATA.electricity_price for ml in after_main]
        after_sa_2_lb_man_cost = \
            [CONSTDATA.driver_per_cost * sl / CONSTDATA.driver_per_speed / CONSTDATA.driver_per_period for sl in
             after_ss_2_sa]
        after_sa_2_lb_power_cost = \
            [CONSTDATA.electricity_price * CONSTDATA.forklift_power * sl / CONSTDATA.driver_per_speed for sl in
             after_ss_2_sa]
        after_NC_lb_2_sa_man_cost = \
            [CONSTDATA.driver_per_cost * sl / CONSTDATA.driver_per_speed / CONSTDATA.driver_per_period for sl in
             after_NC_lb_2_sa]
        after_NC_lb_2_sa_power_cost = \
            [CONSTDATA.electricity_price * CONSTDATA.forklift_power * sl / CONSTDATA.driver_per_speed for sl in
             after_NC_lb_2_sa]
        after_forklift_man_cost = [i + j for i, j in zip(after_sa_2_lb_man_cost, after_NC_lb_2_sa_man_cost)]
        after_forklift_poewr_cost = [i + j for i, j in zip(after_sa_2_lb_power_cost, after_NC_lb_2_sa_power_cost)]
        after_forklift_cost = [i + j for i, j in zip(after_forklift_man_cost, after_forklift_poewr_cost)]
        after_forklift_all_cost = [i + j for i, j in zip(after_main_cost, after_forklift_cost)]

        ori_main_cost = \
            [ml * CONSTDATA.main_line_per_power_per_dist_per_weight * CONSTDATA.electricity_price for ml in ori_main]
        ori_sa_2_lb_man_cost = \
            [CONSTDATA.driver_per_cost * sl / CONSTDATA.driver_per_speed / CONSTDATA.driver_per_period for sl in
             ori_ss_2_sa]
        ori_sa_2_lb_power_cost = \
            [CONSTDATA.electricity_price * CONSTDATA.forklift_power * sl / CONSTDATA.driver_per_speed for sl in
             ori_ss_2_sa]
        ori_NC_lb_2_sa_man_cost = \
            [CONSTDATA.driver_per_cost * sl / CONSTDATA.driver_per_speed / CONSTDATA.driver_per_period for sl in
             ori_NC_lb_2_sa]
        ori_NC_lb_2_sa_power_cost = \
            [CONSTDATA.electricity_price * CONSTDATA.forklift_power * sl / CONSTDATA.driver_per_speed for sl in
             ori_NC_lb_2_sa]
        ori_forklift_man_cost = [i + j for i, j in zip(ori_sa_2_lb_man_cost, ori_NC_lb_2_sa_man_cost)]
        ori_forklift_poewr_cost = [i + j for i, j in zip(ori_sa_2_lb_power_cost, ori_NC_lb_2_sa_power_cost)]
        ori_forklift_cost = [i + j for i, j in zip(ori_forklift_man_cost, ori_forklift_poewr_cost)]
        ori_forklift_all_cost = [i + j for i, j in zip(ori_main_cost, ori_forklift_cost)]

        mod_main_cost = \
            [ml * CONSTDATA.main_line_per_power_per_dist_per_weight * CONSTDATA.electricity_price for ml in mod_main]
        mod_sa_2_lb_man_cost = \
            [CONSTDATA.driver_per_cost * sl / CONSTDATA.driver_per_speed / CONSTDATA.driver_per_period for sl in
             mod_ss_2_sa]
        mod_sa_2_lb_power_cost = \
            [CONSTDATA.electricity_price * CONSTDATA.forklift_power * sl / CONSTDATA.driver_per_speed for sl in
             mod_ss_2_sa]
        mod_NC_lb_2_sa_man_cost = \
            [CONSTDATA.driver_per_cost * sl / CONSTDATA.driver_per_speed / CONSTDATA.driver_per_period for sl in
             mod_NC_lb_2_sa]
        mod_NC_lb_2_sa_power_cost = \
            [CONSTDATA.electricity_price * CONSTDATA.forklift_power * sl / CONSTDATA.driver_per_speed for sl in
             mod_NC_lb_2_sa]
        mod_forklift_man_cost = [i + j for i, j in zip(mod_sa_2_lb_man_cost, mod_NC_lb_2_sa_man_cost)]
        mod_forklift_poewr_cost = [i + j for i, j in zip(mod_sa_2_lb_power_cost, mod_NC_lb_2_sa_power_cost)]
        mod_forklift_cost = [i + j for i, j in zip(mod_forklift_man_cost, mod_forklift_poewr_cost)]
        mod_forklift_all_cost = [i + j for i, j in zip(mod_main_cost, mod_forklift_cost)]

        fig = plt.figure()
        ax1 = fig.add_subplot(2, 3, 1)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        ax2 = fig.add_subplot(2, 3, 2)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        ax3 = fig.add_subplot(2, 3, 3)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        ax4 = fig.add_subplot(2, 3, 4)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        ax5 = fig.add_subplot(2, 3, 5)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        ax6 = fig.add_subplot(2, 3, 6)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

        ax1.plot(date, loads, 'ko--', label='loads', linewidth=2.0, ms=1)
        ax1.plot(date, mean_loads_list, 'g--', label='mean loads', linewidth=2.0, ms=1)
        ax1.plot(date, loads_no_NC, 'ro--', label='no NC loads', linewidth=2.0, ms=1)
        ax1.plot(date, mean_loads_no_NC_list, 'b--', label='mean no loads', linewidth=2.0, ms=1)
        ax1.plot(date, loads_NC, 'mo--', label='NC loads', linewidth=2.0, ms=1)
        ax1.plot(date, mean_loads_NC_list, 'c--', label='mean NC loads', linewidth=2.0, ms=1)

        ax1.legend(loc='lower left', fontsize=12)
        ax1.set_title('loads duing ' + date[0] + '-' + date[-1], fontsize=12)
        # ax1.set_xlabel('date',fontsize=12)
        ax1.set_ylabel('loads (t)', fontsize=12)

        ax2.plot(date, before_main, 'ro-', label='dynamic', linewidth=2.0, ms=1)
        ax2.plot(date, after_main, 'ko--', label='static', linewidth=2.0, ms=1)
        ax2.plot(date, ori_main, 'bo--', label='original', linewidth=2.0, ms=1)
        ax2.plot(date, mod_main, 'yo--', label='modified', linewidth=2.0, ms=1)
        ax2.plot(date, fixed, 'go--', label='fixed', linewidth=2.0, ms=1)
        ax2.legend(loc='lower left', fontsize=12)
        ax2.set_title('main line distance', fontsize=12)
        # ax2.set_xlabel('date',fontsize=12)
        ax2.set_ylabel('weight_distance (t·km)', fontsize=12)

        ax3.plot(date, before_ss_2_sa, 'ro-', label='dynamic', linewidth=2.0, ms=1)
        ax3.plot(date, after_ss_2_sa, 'ko--', label='static', linewidth=2.0, ms=1)
        ax3.plot(date, ori_ss_2_sa, 'bo--', label='original', linewidth=2.0, ms=1)
        ax3.plot(date, mod_ss_2_sa, 'yo--', label='modified', linewidth=2.0, ms=1)
        ax3.legend(loc='lower left', fontsize=12)
        ax3.set_title('sorting sation to storage area distance', fontsize=12)
        # ax3.set_xlabel('date',fontsize=12)
        ax3.set_ylabel('distance (km)', fontsize=12)

        ax4.plot(date, before_sa_2_lb, 'ro-', label='dynamic', linewidth=2.0, ms=1)
        ax4.plot(date, after_sa_2_lb, 'ko--', label='static', linewidth=2.0, ms=1)
        ax4.plot(date, ori_sa_2_lb, 'bo--', label='original', linewidth=2.0, ms=1)
        ax4.plot(date, mod_sa_2_lb, 'yo--', label='modified', linewidth=2.0, ms=1)
        ax4.legend(loc='lower left', fontsize=12)
        ax4.set_title('storage area to loading berth distance', fontsize=12)
        # ax4.set_xlabel('date',fontsize=12)
        ax4.set_ylabel('ditance (km)', fontsize=12)

        ax5.plot(date, before_NC_lb_2_sa, 'ro-', label='dynamic', linewidth=2.0, ms=1)
        ax5.plot(date, after_NC_lb_2_sa, 'ko--', label='static', linewidth=2.0, ms=1)
        ax5.plot(date, ori_NC_lb_2_sa, 'bo--', label='original', linewidth=2.0, ms=1)
        ax5.plot(date, mod_NC_lb_2_sa, 'yo--', label='modified', linewidth=2.0, ms=1)
        ax5.legend(loc='lower left', fontsize=12)
        ax5.set_title('NC unloading berth to storage area distance', fontsize=12)
        # ax4.set_xlabel('date',fontsize=12)
        ax5.set_ylabel('ditance (km)', fontsize=12)

        ax6.plot(date, before_NC_sa_2_lb, 'ro-', label='dynamic', linewidth=2.0, ms=1)
        ax6.plot(date, after_NC_sa_2_lb, 'ko--', label='static', linewidth=2.0, ms=1)
        ax6.plot(date, ori_NC_sa_2_lb, 'bo--', label='original', linewidth=2.0, ms=1)
        ax6.plot(date, mod_NC_sa_2_lb, 'yo--', label='modified', linewidth=2.0, ms=1)
        ax6.legend(loc='lower left', fontsize=12)
        ax6.set_title('NC storage area to loading berth distance', fontsize=12)
        # ax4.set_xlabel('date',fontsize=12)
        ax6.set_ylabel('ditance (km)', fontsize=12)

        plt.show()

    def set_NC_figure1(self):
        def set_date(s):
            if '-' in s:
                temps = s.split('-')
                res = str(temps[1] + temps[2])
                res = (res)[:-2]
                return res
            else:
                return s

        date = [set_date(str(d)) for d in self.NC_comprea_info_fit["date"]]
        used_date = [i for i, _ in enumerate(date)]
        # print(used_date)
        loads = copy.copy(self.NC_loads_list[:-1])
        loads = [_ / CONSTDATA.kg_t for _ in loads]
        loads_no_NC = copy.copy(self.NC_loads_no_NC_list[:-1])
        loads_no_NC = [_ / CONSTDATA.kg_t for _ in loads_no_NC]
        loads_NC = copy.copy(self.NC_loads_NC_list[:-1])
        loads_NC = [_ / CONSTDATA.kg_t for _ in loads_NC]

        mean_loads = np.mean(loads)
        mean_loads_list = [mean_loads for _ in date]
        mean_loads_no_NC = np.mean(loads_no_NC)
        mean_loads_no_NC_list = [mean_loads_no_NC for _ in date]
        mean_loads_NC = np.mean(loads_NC)
        mean_loads_NC_list = [mean_loads_NC for _ in date]

        fixed = [_ * CONSTDATA.before_main_line_distance / CONSTDATA.km_m for _ in loads_no_NC]
        before_main = self.NC_comprea_info_fit["before main_line"] / CONSTDATA.km_m
        before_ss_2_sa = self.NC_comprea_info_fit["before sorting_sation_2_storage_area"] / CONSTDATA.km_m
        before_sa_2_lb = self.NC_comprea_info_fit["before storage_area_2_loading_berth"] / CONSTDATA.km_m
        before_NC_lb_2_sa = self.NC_comprea_info_fit['before NC_loading_berth_2_storage_area'] / CONSTDATA.km_m
        before_NC_sa_2_lb = self.NC_comprea_info_fit['before NC_storage_area_2_loading_berth'] / CONSTDATA.km_m

        after_main = self.NC_comprea_info_fit["after main_line"] / CONSTDATA.km_m
        after_ss_2_sa = self.NC_comprea_info_fit["after sorting_sation_2_storage_area"] / CONSTDATA.km_m
        after_sa_2_lb = self.NC_comprea_info_fit["after storage_area_2_loading_berth"] / CONSTDATA.km_m
        after_NC_lb_2_sa = self.NC_comprea_info_fit['after NC_loading_berth_2_storage_area'] / CONSTDATA.km_m
        after_NC_sa_2_lb = self.NC_comprea_info_fit['after NC_storage_area_2_loading_berth'] / CONSTDATA.km_m

        ori_main = self.NC_comprea_info_fit['origin main_line']
        ori_ss_2_sa = self.NC_comprea_info_fit['origin sorting_sation_2_storage_area']
        ori_sa_2_lb = self.NC_comprea_info_fit['origin storage_area_2_loading_berth']
        ori_NC_lb_2_sa = self.NC_comprea_info_fit['origin NC_loading_berth_2_storage_area']
        ori_NC_sa_2_lb = self.NC_comprea_info_fit['origin NC_storage_area_2_loading_berth']

        mod_main = self.NC_comprea_info_fit['modified main_line']
        mod_ss_2_sa = self.NC_comprea_info_fit['modified sorting_sation_2_storage_area']
        mod_sa_2_lb = self.NC_comprea_info_fit['modified storage_area_2_loading_berth']
        mod_NC_lb_2_sa = self.NC_comprea_info_fit['modified NC_loading_berth_2_storage_area']
        mod_NC_sa_2_lb = self.NC_comprea_info_fit['modified NC_storage_area_2_loading_berth']

        before_main_cost = \
            [ml * CONSTDATA.main_line_per_power_per_dist_per_weight * CONSTDATA.electricity_price for ml in before_main]
        before_sa_2_lb_man_cost = \
            [CONSTDATA.driver_per_cost * sl / CONSTDATA.driver_per_speed / CONSTDATA.driver_per_period for sl in
             before_ss_2_sa]
        before_sa_2_lb_power_cost = \
            [CONSTDATA.electricity_price * CONSTDATA.forklift_power * sl / CONSTDATA.driver_per_speed for sl in
             before_ss_2_sa]
        before_NC_lb_2_sa_man_cost = \
            [CONSTDATA.driver_per_cost * sl / CONSTDATA.driver_per_speed / CONSTDATA.driver_per_period for sl in
             before_NC_lb_2_sa]
        before_NC_lb_2_sa_power_cost = \
            [CONSTDATA.electricity_price * CONSTDATA.forklift_power * sl / CONSTDATA.driver_per_speed for sl in
             before_NC_lb_2_sa]
        before_forklift_man_cost = [i + j for i, j in zip(before_sa_2_lb_man_cost, before_NC_lb_2_sa_man_cost)]
        before_forklift_poewr_cost = [i + j for i, j in zip(before_sa_2_lb_power_cost, before_NC_lb_2_sa_power_cost)]
        before_forklift_cost = [i + j for i, j in zip(before_forklift_man_cost, before_forklift_poewr_cost)]
        before_sorting_cost = [_* CONSTDATA.sorting_per_cost for _ in self.NC_date_before_ss_number.values()]
        before_all_cost = [i + j + k for i, j, k in zip(before_main_cost, before_forklift_cost, before_sorting_cost)]

        after_main_cost = \
            [ml * CONSTDATA.main_line_per_power_per_dist_per_weight * CONSTDATA.electricity_price for ml in after_main]
        after_sa_2_lb_man_cost = \
            [CONSTDATA.driver_per_cost * sl / CONSTDATA.driver_per_speed / CONSTDATA.driver_per_period for sl in
             after_ss_2_sa]
        after_sa_2_lb_power_cost = \
            [CONSTDATA.electricity_price * CONSTDATA.forklift_power * sl / CONSTDATA.driver_per_speed for sl in
             after_ss_2_sa]
        after_NC_lb_2_sa_man_cost = \
            [CONSTDATA.driver_per_cost * sl / CONSTDATA.driver_per_speed / CONSTDATA.driver_per_period for sl in
             after_NC_lb_2_sa]
        after_NC_lb_2_sa_power_cost = \
            [CONSTDATA.electricity_price * CONSTDATA.forklift_power * sl / CONSTDATA.driver_per_speed for sl in
             after_NC_lb_2_sa]
        after_forklift_man_cost = [i + j for i, j in zip(after_sa_2_lb_man_cost, after_NC_lb_2_sa_man_cost)]
        after_forklift_poewr_cost = [i + j for i, j in zip(after_sa_2_lb_power_cost, after_NC_lb_2_sa_power_cost)]
        after_forklift_cost = [i + j for i, j in zip(after_forklift_man_cost, after_forklift_poewr_cost)]
        after_sorting_cost = [_ * CONSTDATA.sorting_per_cost for _ in self.NC_date_after_ss_number.values()]
        after_all_cost = [i + j+k for i, j,k in zip(after_main_cost, after_forklift_cost,after_sorting_cost)]

        ori_main_cost = \
            [ml * CONSTDATA.main_line_per_power_per_dist_per_weight * CONSTDATA.electricity_price for ml in ori_main]
        ori_sa_2_lb_man_cost = \
            [CONSTDATA.driver_per_cost * sl / CONSTDATA.driver_per_speed / CONSTDATA.driver_per_period for sl in
             ori_ss_2_sa]
        ori_sa_2_lb_power_cost = \
            [CONSTDATA.electricity_price * CONSTDATA.forklift_power * sl / CONSTDATA.driver_per_speed for sl in
             ori_ss_2_sa]
        ori_NC_lb_2_sa_man_cost = \
            [CONSTDATA.driver_per_cost * sl / CONSTDATA.driver_per_speed / CONSTDATA.driver_per_period for sl in
             ori_NC_lb_2_sa]
        ori_NC_lb_2_sa_power_cost = \
            [CONSTDATA.electricity_price * CONSTDATA.forklift_power * sl / CONSTDATA.driver_per_speed for sl in
             ori_NC_lb_2_sa]
        ori_forklift_man_cost = [i + j for i, j in zip(ori_sa_2_lb_man_cost, ori_NC_lb_2_sa_man_cost)]
        ori_forklift_poewr_cost = [i + j for i, j in zip(ori_sa_2_lb_power_cost, ori_NC_lb_2_sa_power_cost)]
        ori_forklift_cost = [i + j for i, j in zip(ori_forklift_man_cost, ori_forklift_poewr_cost)]
        ori_sorting_cost = [_ * CONSTDATA.sorting_per_cost for _ in self.NC_date_origin_ss_number.values()]
        ori_all_cost = [i + j+k for i, j,k in zip(ori_main_cost, ori_forklift_cost,ori_sorting_cost)]

        mod_main_cost = \
            [ml * CONSTDATA.main_line_per_power_per_dist_per_weight * CONSTDATA.electricity_price for ml in mod_main]
        mod_sa_2_lb_man_cost = \
            [CONSTDATA.driver_per_cost * sl / CONSTDATA.driver_per_speed / CONSTDATA.driver_per_period for sl in
             mod_ss_2_sa]
        mod_sa_2_lb_power_cost = \
            [CONSTDATA.electricity_price * CONSTDATA.forklift_power * sl / CONSTDATA.driver_per_speed for sl in
             mod_ss_2_sa]
        mod_NC_lb_2_sa_man_cost = \
            [CONSTDATA.driver_per_cost * sl / CONSTDATA.driver_per_speed / CONSTDATA.driver_per_period for sl in
             mod_NC_lb_2_sa]
        mod_NC_lb_2_sa_power_cost = \
            [CONSTDATA.electricity_price * CONSTDATA.forklift_power * sl / CONSTDATA.driver_per_speed for sl in
             mod_NC_lb_2_sa]
        mod_forklift_man_cost = [i + j for i, j in zip(mod_sa_2_lb_man_cost, mod_NC_lb_2_sa_man_cost)]
        mod_forklift_poewr_cost = [i + j for i, j in zip(mod_sa_2_lb_power_cost, mod_NC_lb_2_sa_power_cost)]
        mod_forklift_cost = [i + j for i, j in zip(mod_forklift_man_cost, mod_forklift_poewr_cost)]
        mod_sorting_cost = [_ * CONSTDATA.sorting_per_cost for _ in self.NC_date_modified_ss_number.values()]
        mod_all_cost = [i + j+k for i, j,k in zip(mod_main_cost, mod_forklift_cost,mod_sorting_cost)]

        fixed_main_cost = [CONSTDATA.main_line_per_power_per_dist_per_weight * CONSTDATA.electricity_price*_ for _ in
                           fixed]

        fig = plt.figure()
        ax1 = fig.add_subplot(2, 2, 1)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        ax2 = fig.add_subplot(2, 2, 2)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        ax3 = fig.add_subplot(2, 2, 3)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        ax4 = fig.add_subplot(2, 2, 4)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

        plt.rcParams['font.sans-serif'] = ['SimHei']

        ax1.plot(used_date, loads, 'ko-', label='总货量', linewidth=2.0, ms=1)
        ax1.plot(used_date, mean_loads_list, 'g--', label='货量均值', linewidth=2.0, ms=1)
        # ax1.plot(date, loads_no_NC, 'ro--', label='no NC loads', linewidth=2.0, ms=1)
        # ax1.plot(date, mean_loads_no_NC_list, 'b--', label='mean no loads', linewidth=2.0, ms=1)
        ax1.plot(used_date, loads_NC, 'mo-', label='NC货量', linewidth=2.0, ms=1)
        ax1.plot(used_date, mean_loads_NC_list, 'c--', label='NC货量均值', linewidth=2.0, ms=1)

        ax1.legend(loc='lower left', fontsize=12)
        ax1.set_title(date[0] + '-' + date[-1] + ' 的货量情况', fontsize=12)
        # ax1.set_xlabel('date',fontsize=12)
        ax1.set_ylabel('loads (t)', fontsize=12)

        ax2.plot(used_date, before_main_cost, 'ro-', label='动态', linewidth=2.0, ms=1)
        ax2.plot(used_date, after_main_cost, 'ko--', label='静态', linewidth=2.0, ms=1)
        ax2.plot(used_date, ori_main_cost, 'bo--', label='原卡位', linewidth=2.0, ms=1)
        ax2.plot(used_date, mod_main_cost, 'yo--', label='修正卡位', linewidth=2.0, ms=1)
        ax2.plot(used_date, fixed_main_cost, 'go--', label='固定成本', linewidth=2.0, ms=1)
        ax2.legend(loc='lower left', fontsize=12)
        ax2.set_title('主线运行成本', fontsize=12)
        ax2.set_ylabel('cost (yuan)', fontsize=12)

        ax3.plot(used_date, before_forklift_man_cost, 'ro-', label='动态叉车', linewidth=2.0, ms=1)
        ax3.plot(used_date, after_forklift_man_cost, 'ko--', label='静态叉车', linewidth=2.0, ms=1)
        ax3.plot(used_date, ori_forklift_man_cost, 'bo--', label='原卡位叉车', linewidth=2.0, ms=1)
        ax3.plot(used_date, mod_forklift_man_cost, 'yo--', label='修正卡位叉车', linewidth=2.0, ms=1)

        ax3.plot(used_date, before_sorting_cost, 'ro--', label='动态分拣', linewidth=2.0, ms=1)
        ax3.plot(used_date, after_sorting_cost, 'ko--', label='静态分拣', linewidth=2.0, ms=1)
        ax3.plot(used_date, ori_sorting_cost, 'bo--', label='原卡位分拣', linewidth=2.0, ms=1)
        ax3.plot(used_date, mod_sorting_cost, 'yo--', label='修正卡位分拣', linewidth=2.0, ms=1)

        ax3.plot(used_date, ori_forklift_poewr_cost, 'go--', label='叉车电费', linewidth=2.0, ms=1)
        ax3.legend(loc='lower left', fontsize=12)
        ax3.set_title('叉车成本', fontsize=12)
        # ax3.set_xlabel('date',fontsize=12)
        ax3.set_ylabel('cost(yuan)', fontsize=12)

        ax4.plot(used_date, before_all_cost, 'ro-', label='动态', linewidth=2.0, ms=1)
        ax4.plot(used_date, after_all_cost, 'ko--', label='静态', linewidth=2.0, ms=1)
        ax4.plot(used_date, ori_all_cost, 'bo--', label='原卡位', linewidth=2.0, ms=1)
        ax4.plot(used_date, mod_all_cost, 'yo--', label='修正卡位', linewidth=2.0, ms=1)
        ax4.legend(loc='lower left', fontsize=12)
        ax4.set_title('总成本', fontsize=12)
        # ax4.set_xlabel('date',fontsize=12)
        ax4.set_ylabel('cost(yuan)', fontsize=12)

        # ax5.plot(date, before_NC_lb_2_sa, 'ro-', label='dynamic', linewidth=2.0, ms=1)
        # ax5.plot(date, after_NC_lb_2_sa, 'ko--', label='static', linewidth=2.0, ms=1)
        # ax5.plot(date, ori_NC_lb_2_sa, 'bo--', label='original', linewidth=2.0, ms=1)
        # ax5.plot(date, mod_NC_lb_2_sa, 'yo--', label='modified', linewidth=2.0, ms=1)
        # ax5.legend(loc='lower left', fontsize=12)
        # ax5.set_title('NC unloading berth to storage area distance', fontsize=12)
        # # ax4.set_xlabel('date',fontsize=12)
        # ax5.set_ylabel('ditance (km)', fontsize=12)
        #
        # ax6.plot(date, before_NC_sa_2_lb, 'ro-', label='dynamic', linewidth=2.0, ms=1)
        # ax6.plot(date, after_NC_sa_2_lb, 'ko--', label='static', linewidth=2.0, ms=1)
        # ax6.plot(date, ori_NC_sa_2_lb, 'bo--', label='original', linewidth=2.0, ms=1)
        # ax6.plot(date, mod_NC_sa_2_lb, 'yo--', label='modified', linewidth=2.0, ms=1)
        # ax6.legend(loc='lower left', fontsize=12)
        # ax6.set_title('NC storage area to loading berth distance', fontsize=12)
        # # ax4.set_xlabel('date',fontsize=12)
        # ax6.set_ylabel('ditance (km)', fontsize=12)

        print('before all sorting mean : ', np.mean(before_sorting_cost)/CONSTDATA.sorting_per_cost)
        print('after all sorting mean : ', np.mean(after_sorting_cost)/CONSTDATA.sorting_per_cost)
        print('ori all sorting mean : ', np.mean(ori_sorting_cost)/CONSTDATA.sorting_per_cost)
        print('mod all sorting mean : ', np.mean(mod_sorting_cost)/CONSTDATA.sorting_per_cost)

        print('before all cost mean : ',np.mean(before_all_cost))
        print('after all cost mean : ',np.mean(after_all_cost))
        print('ori all cost mean : ',np.mean(ori_all_cost))
        print('mod all cost mean : ',np.mean(mod_all_cost))
        plt.show()

    def NC_plots(self):
        self.NC_set_day_sort_plan()
        self.NC_set_compare_encoding()
        self.NC_set_compare_fit()
        self.NC_set_ss_num()
        self.set_NC_figure1()
