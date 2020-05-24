from inputData import INPUTDATA
from model import MODEL
from flow import FLOWINFO
from flow import FLOW
from algs import ALGS
from constData import CONSTDATA

import copy
import pandas as pd
import math


class COSTGFLOW(object):
    def __init__(self, flow, ss, lb):
        self.flow = copy.copy(flow)
        self.ss_index = copy.copy(ss)
        self.lb_index = copy.copy(lb)
        # self.main_line_cost = 0.0
        # self.ss_2_sa_cost = 0.0
        # self.sa_2_lb_cost = 0.0
        self.cost = {}


class CALCULATECOST(object):
    def __init__(self, model, shift='755VF2200'):
        self.shift = shift
        self.model = copy.copy(model)
        self.cost = {}
        self.set_data()
        self.set_flow_used()


    def set_flow_used(self):
        self.flow_used = {}
        for tl in self.model.flow_info.flows_used_dict[self.shift].values():
            self.flow_used.update(tl)
        return self.flow_used

    def set_data(self):
        file = './input/' + self.model.flow_info.input_data.all_plans_file
        self.original_ss = pd.read_excel(file, encoding='gbk', sheet_name='原分拣口')
        self.original_lb = pd.read_excel(file, encoding='gbk', sheet_name='原卡位')
        self.algs_ss = pd.read_excel(file, encoding='gbk', sheet_name='算法输出分拣口')
        self.algs_lb = pd.read_excel(file, encoding='gbk', sheet_name='算法输出卡位')
        self.mod_ss = pd.read_excel(file, encoding='gbk', sheet_name='调整后分拣口')
        self.mod_lb = pd.read_excel(file, encoding='gbk', sheet_name='调整后卡位')

    def set_costFlow(self, costFlow, ss, lb):
        def set_list(l):
            l = list(l)
            l.sort()
            return l

        temp_ss = pd.pivot_table(ss, values='分拣口', index=['到达网点', '运输等级', '区域'], aggfunc=set_list)
        temp_ss.reset_index(inplace=True)
        temp_lb = pd.pivot_table(lb, values='卡位', index=['到达网点', '运输等级', '区域'], aggfunc=set_list)
        temp_lb.reset_index(inplace=True)
        temp_info = pd.merge(temp_ss, temp_lb)
        # print(temp_info.columns)
        for r, c in temp_info.iterrows():
            destination = c[0]
            travel_level = c[1]
            zone = c[2]
            _ss = c[3]
            _lb = c[4]
            if destination not in self.flow_used.keys():
                continue
            loads = self.flow_used[destination]
            flow = FLOW(destination, travel_level, loads, zone)
            temp_costFlow = COSTGFLOW(flow, _ss, _lb)
            costFlow[destination] = temp_costFlow
        return costFlow

    def set_costFlows(self):
        self.ori_costFlows = {}
        self.algs_costFlows = {}
        self.mod_costFlows = {}
        self.ori_costFlows = self.set_costFlow(self.ori_costFlows, self.original_ss, self.original_lb)
        self.algs_costFlows = self.set_costFlow(self.algs_costFlows, self.algs_ss, self.algs_lb)
        self.mod_costFlows = self.set_costFlow(self.mod_costFlows, self.mod_ss, self.mod_lb)

    def set_single_flowsCost(self, costFlows):
        for d, cf in costFlows.items():
            destination = d
            ori_loads_no_NC = copy.copy(cf.flow.loads_no_NC)
            loads_no_NC = [ori_loads_no_NC]
            loads_NC = [cf.flow.loads_NC]
            ss_index = cf.ss_index
            lb_index = cf.lb_index
            if len(ss_index) > 1:
                loads_no_NC = [ori_loads_no_NC / len(ss_index) for _ in range(len(ss_index))]
            pallets_no_NC = [_ / CONSTDATA.pallets_weight for _ in loads_no_NC]
            pallets_NC = [_ / CONSTDATA.pallets_weight for _ in loads_NC]
            cf.cost = {}
            # main line
            main_dist = [self.model.main_line_distance_list[i - 1] + CONSTDATA.before_main_line_distance
                         for i in ss_index]
            # print('main line:', main_dist, loads)
            cf.cost['main_line_dist'] = main_dist
            cf.cost['main_line_cost'] = [d * l / CONSTDATA.km_m / CONSTDATA.kg_t for d, l in zip(main_dist, loads_no_NC)]
            # ss 2 sa
            ss_2_sa_dist = [self.model.sorting_sation_2_storage_area_distance_matrix[i - 1][lb_index[0] - 1]
                            for i in ss_index]
            cf.cost['ss_2_sa_dist'] = ss_2_sa_dist
            cf.cost['ss_2_sa_cost'] = [d * p * 2 / CONSTDATA.km_m for d, p in zip(ss_2_sa_dist, pallets_no_NC)]
            # sa 2 lb
            sa_lb_dist = [self.model.storage_area_2_loading_berth_distance_matrix[lb_index[0] - 1][lb_index[0] - 1]]
            cf.cost['sa_2_lb_dist'] = sa_lb_dist
            cf.cost['sa_2_lb_cost'] = [sa_lb_dist[0] * p * 2 / CONSTDATA.km_m for p in pallets_no_NC]
            # NC lb 2 sa
            NC_lb_2_sa_dist = [self.model.NC_loading_berth_2_storage_area_distance_list[lb_index[0]-1]]
            cf.cost['NC_lb_2_sa_dist'] = NC_lb_2_sa_dist
            cf.cost['NC_lb_2_sa_cost'] = [NC_lb_2_sa_dist[0] * p * 2 / CONSTDATA.km_m for p in pallets_NC]
            # NC sa 2 lb
            NC_sa_2_lb_dist = [self.model.storage_area_2_loading_berth_distance_matrix[lb_index[0] - 1][lb_index[0] - 1]]
            cf.cost['NC_sa_2_lb_dist'] = NC_sa_2_lb_dist
            cf.cost['NC_sa_2_lb_cost'] = [NC_sa_2_lb_dist[0] * p * 2 / CONSTDATA.km_m for p in pallets_NC]
        return costFlows

    def set_single_flowsCost_all(self, costFlows, costFlows_str):
        self.cost[costFlows_str] = {}
        self.cost[costFlows_str]['loads'] = sum([flow.flow.loads for flow in costFlows.values()])
        self.cost[costFlows_str]['main_line_cost'] = sum(
            [sum(flow.cost['main_line_cost']) for flow in costFlows.values()])
        self.cost[costFlows_str]['ss_2_sa_cost'] = sum([sum(flow.cost['ss_2_sa_cost']) for flow in costFlows.values()])
        self.cost[costFlows_str]['NC_lb_2_sa_cost'] = sum([sum(flow.cost['NC_lb_2_sa_cost']) for flow in costFlows.values()])
        self.cost[costFlows_str]['sa_2_lb_cost'] = sum([sum(flow.cost['sa_2_lb_cost']) for flow in costFlows.values()])
        self.cost[costFlows_str]['NC_sa_2_lb_cost'] = sum([sum(flow.cost['NC_sa_2_lb_cost']) for flow in costFlows.values()])
        temp_ss_index = []
        for i in costFlows.values():
            temp_ss_index.extend(i.ss_index)
        self.cost[costFlows_str]['ss_num'] = len(set(temp_ss_index))
        return self.cost

    def set_flows_cost(self):
        self.ori_costFlows = self.set_single_flowsCost(self.ori_costFlows)
        self.algs_costFlows = self.set_single_flowsCost(self.algs_costFlows)
        self.mod_costFlows = self.set_single_flowsCost(self.mod_costFlows)
        self.set_single_flowsCost_all(self.ori_costFlows, 'original')
        self.set_single_flowsCost_all(self.algs_costFlows, 'algs')
        self.set_single_flowsCost_all(self.mod_costFlows, 'modified')
        return self.cost

    def show_single_flowsCost_detail(self, costFlows, costFlows_str, writer):
        destination = []
        travel_level = []
        zone = []
        loads = []
        ss_index = []
        lb_index = []
        main_dist = []
        ss_2_sa_dist = []
        sa_2_lb_dist = []
        main_line_cost = []
        ss_2_sa_cost = []
        sa_2_lb_cost = []
        for d, cf in costFlows.items():
            destination.append(d)
            travel_level.append(cf.flow.travel_level)
            zone.append(cf.flow.zone)
            loads.append(cf.flow.loads)
            ss_index.append(cf.ss_index)
            lb_index.append(cf.lb_index)
            main_dist.append(cf.cost['main_line_dist'])
            ss_2_sa_dist.append(cf.cost['ss_2_sa_dist'])
            sa_2_lb_dist.append(cf.cost['sa_2_lb_dist'])
            main_line_cost.append(sum(cf.cost['main_line_cost']))
            ss_2_sa_cost.append(sum(cf.cost['ss_2_sa_cost']))
            sa_2_lb_cost.append(sum(cf.cost['sa_2_lb_cost']))
        result = pd.DataFrame()
        result['destination'] = destination
        result['travel_level'] = travel_level
        result['zone'] = zone
        result['loads'] = loads
        result[costFlows_str + 'ss_index'] = ss_index
        result[costFlows_str + 'lb_index'] = lb_index
        result[costFlows_str + 'main_dist'] = main_dist
        result[costFlows_str + 'ss_2_sa__dist'] = ss_2_sa_dist
        result[costFlows_str + 'sa_2_lb__dist'] = sa_2_lb_dist
        result[costFlows_str + 'main_line_cost'] = main_line_cost
        result[costFlows_str + 'ss_2_sa_cost'] = ss_2_sa_cost
        result[costFlows_str + 'sa_2_lb_cost'] = sa_2_lb_cost
        result.to_excel(excel_writer=writer, sheet_name=costFlows_str, index=False)
        return result

    def show_single_flowCost(self,writer):
        type = ['type']
        loads = ['loads']
        main_line_cost = ['main_line_cost']
        ss_2_sa_cost = ['ss_2_sa_cost']
        sa_2_lb_cost = ['sa_2_lb_cost']
        for k,v in self.cost.items():
            type.append(k)
        for i in range(len(self.cost.items())):
            loads.append(self.cost[type[i+1]][loads[0]])
            main_line_cost.append(self.cost[type[i+1]][main_line_cost[0]])
            ss_2_sa_cost.append(self.cost[type[i+1]][ss_2_sa_cost[0]])
            sa_2_lb_cost.append(self.cost[type[i+1]][sa_2_lb_cost[0]])
        self.cost_df = pd.DataFrame()
        self.cost_df[type[0]] =type[1:]
        self.cost_df[loads[0]] =loads[1:]
        self.cost_df[main_line_cost[0]] =main_line_cost[1:]
        self.cost_df[ss_2_sa_cost[0]] =ss_2_sa_cost[1:]
        self.cost_df[sa_2_lb_cost[0]] =sa_2_lb_cost[1:]
        # self.cost_df.to_excel(excel_writer=writer, sheet_name='costFlows', index=False)
        return self.cost_df

    def show_all_single_flowCost(self, writer):
        self.ori_cost_detail = self.show_single_flowsCost_detail(self.ori_costFlows, 'original', writer)
        self.algs_cost_detail = self.show_single_flowsCost_detail(self.algs_costFlows, 'algs', writer)
        self.mod_cost_detail = self.show_single_flowsCost_detail(self.mod_costFlows, 'modified', writer)
        self.cost_detail = pd.merge(self.ori_cost_detail,self.algs_cost_detail,how='outer')
        self.cost_detail = pd.merge(self.cost_detail,self.mod_cost_detail,how='outer')
        # self.cost_detail.to_excel(excel_writer=writer, sheet_name='cost_detail', index=False)
        self.show_single_flowCost(writer)


    def set_all_flowsCost(self):
        self.set_costFlows()
        self.set_flows_cost()

    def set_ori_cost(self):
        self.ori_costFlows = {}
        self.ori_costFlows = self.set_costFlow(self.ori_costFlows, self.original_ss, self.original_lb)
        self.ori_costFlows = self.set_single_flowsCost(self.ori_costFlows)
        self.set_single_flowsCost_all(self.ori_costFlows, 'original')
        self.ori_cost = self.cost['original']
        return self.ori_cost

    def set_algs_cost(self):
        self.algs_costFlows = {}
        self.algs_costFlows = self.set_costFlow(self.algs_costFlows, self.algs_ss, self.algs_lb)
        self.algs_costFlows = self.set_single_flowsCost(self.algs_costFlows)
        self.set_single_flowsCost_all(self.algs_costFlows, 'algs')
        self.algs_cost = self.cost['algs']
        return self.algs_cost

    def set_mod_cost(self):
        self.mod_costFlows = {}
        self.mod_costFlows = self.set_costFlow(self.mod_costFlows, self.mod_ss, self.mod_lb)
        self.mod_costFlows = self.set_single_flowsCost(self.mod_costFlows)
        self.set_single_flowsCost_all(self.mod_costFlows, 'modified')
        self.mod_cost = self.cost['modified']
        return self.mod_cost

if __name__ == '__main__':
    input_file = './input/'
    data_list = ['20200301-20200325', '20200402-20200408',
                 '20200401-20200416', '20200301-20200429', '20200301-20200415']
    input_data = INPUTDATA(input_file + data_list[4] + '/')

    flow_info = FLOWINFO(input_data, False, True)
    model = MODEL(flow_info)
    # algs = ALGS(model)
    # algs.model.show_fit()

    calculateCost = CALCULATECOST(model)
    # calculateCost.set_all_flowsCost()
    calculateCost.set_ori_cost()
    calculateCost.set_algs_cost()
    calculateCost.set_mod_cost()


    writer = pd.ExcelWriter(input_data.output_filefolder + 'output.xlsx')
    calculateCost.show_all_single_flowCost(writer)
    writer.save()
    writer.close()
