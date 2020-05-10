import copy
from flow import FLOWINFO
from model import MODEL
from algs import ALGS
from model import MODEL
from constData import CONSTDATA

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
        self.flow_info = FLOWINFO(self.data, 1)
        self.model = MODEL(self.flow_info)
        self.encoding = {}
        self.fit = {}
        self.date_loads = {}
        self.loads_list = []

    def set_day_sort_plan(self, duration=0):
        self.record_date_list = []
        flow_info = FLOWINFO(self.data, 1)
        model = MODEL(flow_info)
        algs = ALGS(model)
        self.encoding = algs.model.encoding
        self.fit = algs.model.fit
        # algs.model.show_encoding()
        # algs.model.show_fit()
        encoding_record = algs.model.set_encoding_record()
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
            flow_info = FLOWINFO(temp_input_data, 1)
            model = MODEL(flow_info)
            algs = ALGS(model)
            self.before_encoding_list.append(algs.model.encoding)
            self.before_fit_list.append(algs.model.fit)
            # algs.model.show_fit()

            algs = ALGS(model, True, self.encoding, encoding_record)
            # algs.model.show_fit()
            self.after_encoding_list.append(algs.model.encoding)
            self.after_fit_list.append(algs.model.fit)

    def set_compare_fit(self, label=False):
        self.comprea_info_fit = pd.DataFrame()
        temp_record_list = copy.copy(self.record_date_list)
        temp_record_list.append('all')
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
        before_main.append(self.fit['main_line'])
        before_ss_2_sa.append(self.fit['sorting_sation_2_storage_area'])
        before_sa_2_lb.append(self.fit['storage_area_2_loading_berth'])
        befor_NC_lb_2_sa.append(self.fit['NC_loading_berth_2_storage_area'])
        befor_NC_sa_2_lb.append(self.fit['NC_storage_area_2_loading_berth'])
        after_main.append(self.fit['main_line'])
        after_ss_2_sa.append(self.fit['sorting_sation_2_storage_area'])
        after_sa_2_lb.append(self.fit['storage_area_2_loading_berth'])
        after_NC_lb_2_sa.append(self.fit['NC_loading_berth_2_storage_area'])
        after_NC_sa_2_lb.append(self.fit['NC_storage_area_2_loading_berth'])
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

    def set_compare_encoding(self, label=False):
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

    def set_no_NC_figure(self):
        def set_date(s):
            if '-' in s:
                temps = s.split('-')
                res = str(temps[1] + temps[2])
                res = (res)[:-2]
                return res
            else:
                return s

        date = [set_date(str(d)) for d in self.comprea_info_fit["date"]]
        loads = copy.copy(self.loads_list)
        loads = [_ / CONSTDATA.kg_t for _ in loads]
        mean_loads = np.mean(loads[:-1])
        mean_loads_list = [mean_loads for _ in date]
        fixed = [_ * CONSTDATA.before_main_line_distance/CONSTDATA.km_m for _ in loads]
        before_main = self.comprea_info_fit["before main_line"]/CONSTDATA.km_m
        before_ss_2_sa = self.comprea_info_fit["before sorting_sation_2_storage_area"]/CONSTDATA.km_m
        before_sa_2_lb = self.comprea_info_fit["before storage_area_2_loading_berth"]/CONSTDATA.km_m
        after_main = self.comprea_info_fit["after main_line"]/CONSTDATA.km_m
        after_ss_2_sa = self.comprea_info_fit["after sorting_sation_2_storage_area"]/CONSTDATA.km_m
        after_sa_2_lb = self.comprea_info_fit["after storage_area_2_loading_berth"]/CONSTDATA.km_m

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
        ax1.legend(loc='best', fontsize=12)
        ax1.set_title('loads duing ' + date[0] + '-' + date[-2], fontsize=12)
        # ax1.set_xlabel('date',fontsize=12)
        ax1.set_ylabel('loads (t)', fontsize=12)

        ax2.plot(date, before_main, 'ro-', label='dynamic', linewidth=2.0, ms=1)
        ax2.plot(date, after_main, 'ko--', label='static', linewidth=2.0, ms=1)
        ax2.plot(date, fixed, 'go--', label='fixed', linewidth=2.0, ms=1)
        ax2.legend(loc='best', fontsize=12)
        ax2.set_title('main line distance', fontsize=12)
        # ax2.set_xlabel('date',fontsize=12)
        ax2.set_ylabel('weight_distance (t*km)', fontsize=12)

        ax3.plot(date, before_ss_2_sa, 'ro-', label='dynamic', linewidth=2.0, ms=1)
        ax3.plot(date, after_ss_2_sa, 'ko--', label='static', linewidth=2.0, ms=1)
        ax3.legend(loc='best', fontsize=12)
        ax3.set_title('sorting sation to storage area distance', fontsize=12)
        # ax3.set_xlabel('date',fontsize=12)
        ax3.set_ylabel('distance (km)', fontsize=12)

        ax4.plot(date, before_sa_2_lb, 'ro-', label='dynamic', linewidth=2.0, ms=1)
        ax4.plot(date, after_sa_2_lb, 'ko--', label='static', linewidth=2.0, ms=1)
        ax4.legend(loc='best', fontsize=12)
        ax4.set_title('storage area to loading berth distance', fontsize=12)
        # ax4.set_xlabel('date',fontsize=12)
        ax4.set_ylabel('ditance (km)', fontsize=12)

        plt.show()

    def plot_no_NC_zone_loads(self):
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

        plt.show()

    def analysis_no_NC_zone_loads(self):
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
            plt.plot(date_list[:-1], loads[:-1],'o-', label=zone, linewidth=2.0, ms=1.0)
        plt.yticks(fontsize=15)
        plt.legend(loc='best', fontsize=15)
        plt.ylabel('loads (t)', fontsize=15)
        plt.title('travel level zone loads', fontsize=20)
        plt.show()

    # consider NC
    def set_day_sort_plan(self, duration=0):
        self.record_date_list = []
        flow_info = FLOWINFO(self.data, 1)
        model = MODEL(flow_info)
        algs = ALGS(model)
        self.encoding = algs.model.encoding
        self.fit = algs.model.fit
        # algs.model.show_encoding()
        # algs.model.show_fit()
        encoding_record = algs.model.set_encoding_record()
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
            flow_info = FLOWINFO(temp_input_data, 1)
            model = MODEL(flow_info)
            algs = ALGS(model)
            self.before_encoding_list.append(algs.model.encoding)
            self.before_fit_list.append(algs.model.fit)
            # algs.model.show_fit()

            algs = ALGS(model, True, self.encoding, encoding_record)
            # algs.model.show_fit()
            self.after_encoding_list.append(algs.model.encoding)
            self.after_fit_list.append(algs.model.fit)

    def set_compare_fit(self, label=False):
        self.comprea_info_fit = pd.DataFrame()
        temp_record_list = copy.copy(self.record_date_list)
        temp_record_list.append('all')
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
        before_main.append(self.fit['main_line'])
        before_ss_2_sa.append(self.fit['sorting_sation_2_storage_area'])
        before_sa_2_lb.append(self.fit['storage_area_2_loading_berth'])
        befor_NC_lb_2_sa.append(self.fit['NC_loading_berth_2_storage_area'])
        befor_NC_sa_2_lb.append(self.fit['NC_storage_area_2_loading_berth'])
        after_main.append(self.fit['main_line'])
        after_ss_2_sa.append(self.fit['sorting_sation_2_storage_area'])
        after_sa_2_lb.append(self.fit['storage_area_2_loading_berth'])
        after_NC_lb_2_sa.append(self.fit['NC_loading_berth_2_storage_area'])
        after_NC_sa_2_lb.append(self.fit['NC_storage_area_2_loading_berth'])
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

    def set_compare_encoding(self, label=False):
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

    def set_no_NC_figure(self):
        def set_date(s):
            if '-' in s:
                temps = s.split('-')
                res = str(temps[1] + temps[2])
                res = (res)[:-2]
                return res
            else:
                return s

        date = [set_date(str(d)) for d in self.comprea_info_fit["date"]]
        loads = copy.copy(self.loads_list)
        loads = [_ / CONSTDATA.kg_t for _ in loads]
        mean_loads = np.mean(loads[:-1])
        mean_loads_list = [mean_loads for _ in date]
        fixed = [_ * CONSTDATA.before_main_line_distance/CONSTDATA.km_m for _ in loads]
        before_main = self.comprea_info_fit["before main_line"]/CONSTDATA.km_m
        before_ss_2_sa = self.comprea_info_fit["before sorting_sation_2_storage_area"]/CONSTDATA.km_m
        before_sa_2_lb = self.comprea_info_fit["before storage_area_2_loading_berth"]/CONSTDATA.km_m
        after_main = self.comprea_info_fit["after main_line"]/CONSTDATA.km_m
        after_ss_2_sa = self.comprea_info_fit["after sorting_sation_2_storage_area"]/CONSTDATA.km_m
        after_sa_2_lb = self.comprea_info_fit["after storage_area_2_loading_berth"]/CONSTDATA.km_m

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
        ax1.legend(loc='best', fontsize=12)
        ax1.set_title('loads duing ' + date[0] + '-' + date[-2], fontsize=12)
        # ax1.set_xlabel('date',fontsize=12)
        ax1.set_ylabel('loads (t)', fontsize=12)

        ax2.plot(date, before_main, 'ro-', label='dynamic', linewidth=2.0, ms=1)
        ax2.plot(date, after_main, 'ko--', label='static', linewidth=2.0, ms=1)
        ax2.plot(date, fixed, 'go--', label='fixed', linewidth=2.0, ms=1)
        ax2.legend(loc='best', fontsize=12)
        ax2.set_title('main line distance', fontsize=12)
        # ax2.set_xlabel('date',fontsize=12)
        ax2.set_ylabel('weight_distance (t*km)', fontsize=12)

        ax3.plot(date, before_ss_2_sa, 'ro-', label='dynamic', linewidth=2.0, ms=1)
        ax3.plot(date, after_ss_2_sa, 'ko--', label='static', linewidth=2.0, ms=1)
        ax3.legend(loc='best', fontsize=12)
        ax3.set_title('sorting sation to storage area distance', fontsize=12)
        # ax3.set_xlabel('date',fontsize=12)
        ax3.set_ylabel('distance (km)', fontsize=12)

        ax4.plot(date, before_sa_2_lb, 'ro-', label='dynamic', linewidth=2.0, ms=1)
        ax4.plot(date, after_sa_2_lb, 'ko--', label='static', linewidth=2.0, ms=1)
        ax4.legend(loc='best', fontsize=12)
        ax4.set_title('storage area to loading berth distance', fontsize=12)
        # ax4.set_xlabel('date',fontsize=12)
        ax4.set_ylabel('ditance (km)', fontsize=12)

        plt.show()

    def plot_no_NC_zone_loads(self):
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

        plt.show()

    def analysis_no_NC_zone_loads(self):
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
            plt.plot(date_list[:-1], loads[:-1], label=zone, linewidth=2.0, ms=1.0)
        plt.yticks(fontsize=15)
        plt.legend(loc='best', fontsize=15)
        plt.ylabel('loads (t)', fontsize=15)
        plt.title('travel level zone loads', fontsize=20)
        plt.show()

