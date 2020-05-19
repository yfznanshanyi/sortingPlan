from inputData import INPUTDATA
from model import MODEL
from flow import FLOWINFO
from flow import FLOW

import copy
import pandas as pd
import math


class COSTGFLOW(object):
    def __init__(self, flow,ss,lb):
        self.flow = copy.copy(flow)
        self.ss_index = copy.copy(ss)
        self.lb_index = copy.copy(lb)
        self.main_line_cost = 0.0
        self.ss_2_sa_cost = 0.0
        self.sa_2_lb_cost = 0.0


class CALCULATECOST(object):
    def __init__(self, model, shift='755VF2200'):
        self.shift = shift
        self.model = copy.copy(model)
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
        temp_info = pd.merge(temp_ss,temp_lb)
        # print(temp_info.columns)
        for r,c in temp_info.iterrows():
            destination = c[0]
            travel_level = c[1]
            zone = c[2]
            _ss = c[3]
            _lb = c[4]
            loads = self.flow_used[destination]
            flow = FLOW(destination,travel_level,loads,zone)
            temp_costFlow = COSTGFLOW(flow,_ss,_lb)
            costFlow[destination] = temp_costFlow
        return costFlow

    def set_costFlows(self):
        self.ori_costFlows = {}
        self.algs_costFlows = {}
        self.mod_costFlows = {}
        self.ori_costFlows = self.set_costFlow(self.ori_costFlows, self.original_ss, self.original_lb)
        self.algs_costFlows = self.set_costFlow(self.algs_costFlows, self.algs_ss, self.algs_lb)
        self.mod_costFlows = self.set_costFlow(self.mod_costFlows, self.mod_ss, self.mod_lb)

    def set_single_flow_cost(self,costFlows):
        for d,cf in costFlows.items():
            ss_coor = [ ]
            lb_coor = [for ]

            # main line

            # ss 2 sa

            # sa 2 lb

    # def set_flows_cost(self):



if __name__ == '__main__':
    input_file = './input/'
    data_list = ['20200301-20200325', '20200402-20200408',
                 '20200401-20200416', '20200301-20200429', '20200301-20200415']
    input_data = INPUTDATA(input_file + data_list[4] + '/')

    flow_info = FLOWINFO(input_data, False, False)
    model = MODEL(flow_info)

    calculateCost = CALCULATECOST(model)
