import copy
import itertools

from constData import CONSTDATA
from flowBand import FLOWBAND


class ALGS(object):
    def __init__(self, model, NC_label=False, encoding='', encoding_record=''):
        self.model = copy.copy(model)
        self.model.initliza_encoding()
        if len(encoding_record) == 0:
            if NC_label == False:
                self.set_big_shift_travel_level1()
                encoding = self.set_big_shift_travel_level23()
            else:
                self.NC_set_big_shift_travel_level1()
                encoding = self.set_big_shift_travel_level23()
        else:
            self.model.set_other_encoding(encoding, encoding_record)
            encoding = self.model.encoding
        self.model.fit = self.model.decoding(encoding)
    # no NC sorted
    def sort_flowBand_list(self, flowBand_list, order=0):
        temp_flowBand_list = copy.copy(flowBand_list)
        temp_flowBand_list.sort()
        front_index = 0
        back_index = len(temp_flowBand_list) - 1
        sorted_flowBand_list = []
        label = 0
        if order != 0:
            label = 1
        while len(sorted_flowBand_list) < len(flowBand_list):
            if label % 2 == 0:
                sorted_flowBand_list.append(copy.copy(temp_flowBand_list[front_index]))
                front_index = front_index + 1
            else:
                sorted_flowBand_list.append(copy.copy(temp_flowBand_list[back_index]))
                back_index = back_index - 1
            label = label + 1
        # print(len(flowBand_list),len(sorted_flowBand_list))
        return sorted_flowBand_list

    # 设置大班次一级干线流向
    def set_big_shift_travel_level1(self):
        shift = self.model.flow_info.big_shift
        shift_mean_loads = self.model.shift_flowBands_mean_loads[shift]
        travel_level = '一级运输'
        # if travel_level not in self.model.shift_flowBands_mean_loads.keys():
        #     return copy.copy(self.model.initliza_encoding())
        shift_travel_level_mean_loads = self.model.shift_travel_level_flowBands_mean_loads[shift][travel_level]
        rate = self.model.shift_travel_level_flowBands_all_loads[shift][travel_level] / \
               self.model.shift_flowBands_all_loads[shift]
        max_sorting_sation_num = CONSTDATA.short_side_sorting_sation_num
        theory_soring_sation_num = round(CONSTDATA.sorting_sation_num * rate, 0)
        max_loading_berth_num = CONSTDATA.short_side_loading_berth_num
        theory_loading_berth_num = round(CONSTDATA.loading_berth_num * rate, 0)

        temp_flows_list = copy.copy(self.model.shift_travel_level_flowBands[shift][travel_level])
        temp_zone_flowBands = []
        for zone, flow_list in self.model.shift_travel_level_zone_flowBands[shift][travel_level].items():
            if len(flow_list) == 0:
                continue
            temp_zone_flowBands.append(FLOWBAND(copy.copy(flow_list)))
        temp_zone_flowBands.sort(key=lambda x: x.mean_loads, reverse=True)
        sorting_sation_flowBands = []
        loading_berth_flowBands = []
        label = 1
        for flowBand in temp_zone_flowBands:
            # temp = flowBand.set_combined_flowBands(shift_travel_level_mean_loads,
            #                                        CONSTDATA.sorting_sation_travel_level1_combine_rate_ub)
            temp = flowBand.set_combined_flowBands(CONSTDATA.sorting_sation_loads_ub,
                                                   CONSTDATA.sorting_sation_travel_level1_combine_rate_ub)
            temp.sort(reverse=True)
            label = label + len(temp)
            temp = self.sort_flowBand_list(temp, label % 2)
            for flowBand in temp:
                # ttemp = flowBand.split_big_flow(shift_travel_level_mean_loads,
                #                                 CONSTDATA.sorting_sation_travel_level1_num_ub)
                ttemp = flowBand.split_big_flow(CONSTDATA.sorting_sation_loads_ub,
                                                CONSTDATA.sorting_sation_travel_level1_num_ub)
                if ttemp == -1:
                    sorting_sation_flowBands.append(flowBand)
                    loading_berth_flowBands.append(flowBand)
                else:
                    sorting_sation_flowBands.extend(ttemp)
                    loading_berth_flowBands.append(ttemp)
        # set algorithm encoding
        encoding = copy.copy(self.model.initliza_encoding())
        for flowBand, sorting_sation_index in zip(sorting_sation_flowBands,
                                                  self.model.sorting_sation_set.short_side_index):
            encoding['encoding_flow_sorting_sation'][flowBand] = sorting_sation_index
        for flowBand, loading_berth_index in zip(loading_berth_flowBands,
                                                 self.model.loading_berth_set.short_side_index):
            if type(flowBand) == list:
                for subflowBand in flowBand:
                    encoding['encoding_flow_loading_berth'][subflowBand] = loading_berth_index
            else:
                encoding['encoding_flow_loading_berth'][flowBand] = loading_berth_index
        return encoding

    # 设置大班次二三级干线流向
    def set_big_shift_travel_level23(self):
        shift = self.model.flow_info.big_shift
        shift_mean_loads = self.model.shift_flowBands_mean_loads[shift]
        travel_level1 = '一级运输'
        travel_level2 = '二级运输'
        travel_level3 = '三级运输'
        # shift_travel_level1_mean_loads = self.model.shift_travel_level_flowBands_mean_loads[shift][travel_level1]
        shift_travel_level2_mean_loads = self.model.shift_travel_level_flowBands_mean_loads[shift][travel_level2]
        shift_travel_level3_mean_loads = self.model.shift_travel_level_flowBands_mean_loads[shift][travel_level3]
        rate2 = self.model.shift_travel_level_flowBands_all_loads[shift][travel_level2] / \
                self.model.shift_flowBands_all_loads[shift]
        rate3 = self.model.shift_travel_level_flowBands_all_loads[shift][travel_level3] / \
                self.model.shift_flowBands_all_loads[shift]
        max_sorting_sation_num = CONSTDATA.long_side_sorting_sation_num
        theory_soring_sation_num = round(CONSTDATA.sorting_sation_num * (rate2 + rate3), 0)
        theory_soring_sation_travel_levele2_num = round(CONSTDATA.sorting_sation_num * rate2, 0)
        theory_soring_sation_travel_levele3_num = round(CONSTDATA.sorting_sation_num * rate3, 0)
        max_loading_berth_num = CONSTDATA.long_side_loading_berth_num
        theory_loading_berth_num = round(CONSTDATA.loading_berth_num * (rate2 + rate3), 0)
        theory_loading_berth_travel_level2_num = round(CONSTDATA.loading_berth_num * rate2, 0)
        theory_loading_berth_travel_level3_num = round(CONSTDATA.loading_berth_num * rate3, 0)
        temp_travel_level2_flows_list = copy.copy(self.model.shift_travel_level_flowBands[shift][travel_level2])
        temp_travel_level3_flows_list = copy.copy(self.model.shift_travel_level_flowBands[shift][travel_level3])
        temp_travel_level2_zone_flowBands = []
        temp_travel_level3_zone_flowBands = []
        for zone, flow_list in self.model.shift_travel_level_zone_flowBands[shift][travel_level2].items():
            temp_travel_level2_zone_flowBands.append(FLOWBAND(copy.copy(flow_list)))
        temp_travel_level2_zone_flowBands.sort(key=lambda x: x.mean_loads, reverse=True)
        temp_travel_level3_zone_flowBands.append(FLOWBAND(temp_travel_level3_flows_list))
        temp_travel_level23_zone_flowBands = copy.copy(temp_travel_level2_zone_flowBands)
        temp_travel_level23_zone_flowBands.insert(1, temp_travel_level3_zone_flowBands[0])
        sorting_sation_flowBands = []
        loading_berth_flowBands = []

        temp_travel_level23_flowsBands = []
        label = 1
        for flowBand in temp_travel_level23_zone_flowBands:
            travel_level = flowBand.flow_list[0].travel_level
            if travel_level == travel_level2:
                # temp = flowBand.set_combined_flowBands(shift_travel_level1_mean_loads,
                #                                        CONSTDATA.sorting_sation_travel_level2_combine_rate_ub)
                temp = flowBand.set_combined_flowBands(CONSTDATA.sorting_sation_loads_ub,
                                                       CONSTDATA.sorting_sation_travel_level2_combine_rate_ub)
            else:
                # temp = flowBand.set_combined_flowBands(shift_travel_level1_mean_loads,
                #                                        CONSTDATA.sorting_sation_travel_level3_combine_rate_ub)
                temp = flowBand.set_combined_flowBands(CONSTDATA.sorting_sation_loads_ub,
                                                       CONSTDATA.sorting_sation_travel_level3_combine_rate_ub)
            temp.sort(reverse=True)
            label = label + len(temp)
            temp = self.sort_flowBand_list(temp, label % 2)
            for flowBand in temp:
                travel_level = flowBand.flow_list[0].travel_level
                if travel_level == travel_level2:
                    # ttemp = flowBand.split_big_flow(shift_travel_level1_mean_loads,
                    #                                 CONSTDATA.sorting_sation_travel_level2_num_ub)
                    ttemp = flowBand.split_big_flow(CONSTDATA.sorting_sation_loads_ub,
                                                    CONSTDATA.sorting_sation_travel_level2_num_ub)
                else:
                    # ttemp = flowBand.split_big_flow(shift_travel_level1_mean_loads,
                    #                                 CONSTDATA.sorting_sation_travel_level3_num_ub)
                    ttemp = flowBand.split_big_flow(CONSTDATA.sorting_sation_loads_ub,
                                                    CONSTDATA.sorting_sation_travel_level3_num_ub)
                if ttemp == -1:
                    sorting_sation_flowBands.append(flowBand)
                    loading_berth_flowBands.append(flowBand)
                else:
                    sorting_sation_flowBands.extend(ttemp)
                    loading_berth_flowBands.append(ttemp)

        # set algorithm encoding
        encoding = copy.copy(self.model.encoding)
        for flowBand, sorting_sation_index in zip(sorting_sation_flowBands,
                                                  self.model.sorting_sation_set.long_side_index):
            encoding['encoding_flow_sorting_sation'][flowBand] = sorting_sation_index
        for flowBand, loading_berth_index in zip(loading_berth_flowBands,
                                                 self.model.loading_berth_set.long_side_index):
            if type(flowBand) == list:
                for subflowBand in flowBand:
                    encoding['encoding_flow_loading_berth'][subflowBand] = loading_berth_index
            else:
                encoding['encoding_flow_loading_berth'][flowBand] = loading_berth_index
        # self.model.set_encoding(encoding)
        # self.model.show_encoding()
        return encoding

    # 考虑NC件，对一级干线各区域进行排序
    def set_zone_fit(self, ss_zone_flowBand, lb_zone_flowBand, ss_begin_index, lb_begin_index):
        encoding = copy.copy(self.model.initliza_encoding())
        temp_ss_index = [ss_begin_index + _ for _ in range(len(ss_zone_flowBand))]
        # print(temp_ss_index)
        temp_lb_index = [lb_begin_index + _ for _ in range(len(lb_zone_flowBand))]

        for flowBand, sorting_sation_index in zip(ss_zone_flowBand, temp_ss_index):
            encoding['encoding_flow_sorting_sation'][flowBand] = sorting_sation_index
        for flowBand, loading_berth_index in zip(lb_zone_flowBand, temp_lb_index):
            if type(flowBand) == list:
                for subflowBand in flowBand:
                    encoding['encoding_flow_loading_berth'][subflowBand] = loading_berth_index
            else:
                encoding['encoding_flow_loading_berth'][flowBand] = loading_berth_index
        fit = copy.copy(self.model.decoding(encoding))
        for f in fit.keys():
            fit[f] = fit[f] / len(ss_zone_flowBand)
        return fit

    def NC_sort_flowBand_list(self, NC_ss_zone_flowBands, NC_lb_zone_flowBands):
        temp_NC_ss_zone_flowBands = copy.copy(NC_ss_zone_flowBands)
        temp_NC_lb_zone_flowBands = copy.copy(NC_lb_zone_flowBands)
        cur_ss_index = 0
        cur_lb_index = 0
        sorted_ss_zone_flowBand_list = []
        sorted_lb_zone_flowBand_list = []
        zone_index_list = [_ for _ in range(len(temp_NC_ss_zone_flowBands))]
        for i in range(len(NC_ss_zone_flowBands)):
            temp_fit_list = [self.set_zone_fit(temp_NC_ss_zone_flowBands[_], temp_NC_lb_zone_flowBands[_],
                                               cur_ss_index, cur_lb_index) for _ in range(len(temp_NC_ss_zone_flowBands))]
            temp_compare_fit_list = [fit['sorting_sation_2_storage_area'] + fit['NC_loading_berth_2_storage_area']
                             for fit in temp_fit_list]
            zone_index = temp_compare_fit_list.index(max(temp_compare_fit_list))
            zone_index_list.remove(zone_index_list[zone_index])
            sorted_ss_zone_flowBand_list.append(copy.copy(temp_NC_ss_zone_flowBands[zone_index]))
            sorted_lb_zone_flowBand_list.append(copy.copy(temp_NC_lb_zone_flowBands[zone_index]))
            temp_NC_ss_zone_flowBands.remove(temp_NC_ss_zone_flowBands[zone_index])
            temp_NC_lb_zone_flowBands.remove(temp_NC_lb_zone_flowBands[zone_index])
            cur_ss_index = cur_ss_index + len(sorted_ss_zone_flowBand_list[-1])
            cur_lb_index = cur_lb_index + len(sorted_lb_zone_flowBand_list[-1])
        return sorted_ss_zone_flowBand_list, sorted_lb_zone_flowBand_list

    def NC_set_big_shift_travel_level1(self):
        shift = self.model.flow_info.big_shift
        shift_mean_loads = self.model.shift_flowBands_mean_loads[shift]
        travel_level = '一级运输'
        shift_travel_level_mean_loads = self.model.shift_travel_level_flowBands_mean_loads[shift][travel_level]
        rate = self.model.shift_travel_level_flowBands_all_loads[shift][travel_level] / \
               self.model.shift_flowBands_all_loads[shift]
        max_sorting_sation_num = CONSTDATA.short_side_sorting_sation_num
        theory_soring_sation_num = round(CONSTDATA.sorting_sation_num * rate, 0)
        max_loading_berth_num = CONSTDATA.short_side_loading_berth_num
        theory_loading_berth_num = round(CONSTDATA.loading_berth_num * rate, 0)

        temp_flows_list = copy.copy(self.model.shift_travel_level_flowBands[shift][travel_level])
        temp_zone_flowBands = []
        for zone, flow_list in self.model.shift_travel_level_zone_flowBands[shift][travel_level].items():
            if len(flow_list) == 0:
                continue
            temp_zone_flowBands.append(FLOWBAND(copy.copy(flow_list)))
        temp_zone_flowBands.sort(key=lambda x: x.mean_loads_no_NC, reverse=True)
        label = 1
        temp_NC_ss_zone_flowBands = []
        temp_NC_lb_zone_flowBands = []
        for flowBand in temp_zone_flowBands:
            temp_NC_ss_zone_flowBands.append([])
            temp_NC_lb_zone_flowBands.append([])
            temp = flowBand.NC_set_combined_flowBands(CONSTDATA.sorting_sation_loads_ub,
                                                      CONSTDATA.sorting_sation_travel_level1_combine_rate_ub)
            temp.sort(reverse=True)
            label = label + len(temp)
            temp = self.sort_flowBand_list(temp, label % 2)
            for flowBand in temp:
                ttemp = flowBand.NC_split_big_flow(CONSTDATA.sorting_sation_loads_ub,
                                                   CONSTDATA.sorting_sation_travel_level1_num_ub)
                if ttemp == -1:
                    temp_NC_ss_zone_flowBands[-1].append(flowBand)
                    temp_NC_lb_zone_flowBands[-1].append(flowBand)
                else:
                    temp_NC_ss_zone_flowBands[-1].extend(ttemp)
                    temp_NC_lb_zone_flowBands[-1].append(ttemp)
        temp_sorting_sation_flowBands,temp_loading_berth_flowBands = self.NC_sort_flowBand_list(temp_NC_ss_zone_flowBands, temp_NC_lb_zone_flowBands)
        sorting_sation_flowBands = []
        loading_berth_flowBands = []
        for ss_flowBand in temp_sorting_sation_flowBands:
            sorting_sation_flowBands.extend(ss_flowBand)
        for ss_flowBand in temp_loading_berth_flowBands:
            loading_berth_flowBands.extend(ss_flowBand)
        # set algorithm encoding
        encoding = copy.copy(self.model.initliza_encoding())
        for flowBand, sorting_sation_index in zip(sorting_sation_flowBands,
                                                  self.model.sorting_sation_set.short_side_index):
            encoding['encoding_flow_sorting_sation'][flowBand] = sorting_sation_index
        for flowBand, loading_berth_index in zip(loading_berth_flowBands,
                                                 self.model.loading_berth_set.short_side_index):
            if type(flowBand) == list:
                for subflowBand in flowBand:
                    encoding['encoding_flow_loading_berth'][subflowBand] = loading_berth_index
            else:
                encoding['encoding_flow_loading_berth'][flowBand] = loading_berth_index
        return encoding
