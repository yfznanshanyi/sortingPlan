import pandas as pd
import copy
import numpy as np


# static methods
def get_list(s):
    s = list(s)
    return s


class INPUTDATA(object):
    def __init__(self, input_filefolder='./input/', output_filefolder='./output/'):
        self.input_filefolder = input_filefolder
        self.output_filefolder = output_filefolder
        self.loading_file_in = '快运干支线装载率日报表755VF进.csv'
        self.loading_file_out = '快运干支线装载率日报表755VF出.csv'
        self.split_rate_file = 'select_plan_input.csv'
        self.NC_rate_file = 'df_NC_rate.csv'
        self.all_plans_file = '各分拣计划汇总.xlsx'
        self.set_input_data()

    def set_input_data(self):
        self.loading_table_in = pd.read_csv(self.input_filefolder + self.loading_file_in)
        self.loading_table_out = pd.read_csv(self.input_filefolder + self.loading_file_out)
        self.split_rate = pd.read_csv(self.input_filefolder + self.split_rate_file)
        # self.loading_table_in = self.loading_table_in[self.loading_table_in==self.loading_table_in]
        # self.loading_table_out = self.loading_table_out[self.loading_table_out==self.loading_table_out]
        self.loading_table_in['任务状态'].replace(np.nan, '', inplace=True)
        self.loading_table_out['任务状态'].replace(np.nan, '', inplace=True)
        self.loading_table_in = self.loading_table_in[self.loading_table_in['任务状态'].str.contains('已完成')]
        self.loading_table_out = self.loading_table_out[self.loading_table_out['任务状态'].str.contains('已完成')]
        # try:
        self.NC_rate = pd.read_csv(self.input_filefolder + self.NC_rate_file)
        # finally:
        #     print('Error: no NC rate data!')
        self.date_list = list(self.loading_table_in['运行日期'].unique())
        self.date_list.sort()

    def set_date(self, date_list):
        self.loading_table_out = self.loading_table_out[self.loading_table_out['运行日期'].isin(date_list)]
        self.loading_table_in = self.loading_table_in[self.loading_table_in['运行日期'].isin(date_list)]
        self.date_list = list(self.loading_table_in['运行日期'].unique())
        self.date_list.sort()
