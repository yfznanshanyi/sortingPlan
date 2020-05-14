from coordinate import COORDINATE


class CONSTDATA(object):
    # second_level = ['769WK', '020WH', '757WH', '762VA', '752WH', '663WH', '760WH', '759VA', '668VA']
    # changeDic = {
    #     '519WH': '519W', '551WH': '551WL', '592WH': '592WD',
    #     '757WL': '757WH', '752W': '752WH'
    # }

    main_line_capacity = 5000
    average_weight_per_package = 25
    average_piece_per_person = 6.87
    # pallets data
    pallets_weight = 200
    pallets_length = 1.2
    pallets_width = 1.0
    # kilogram
    kg_t = 1000.0
    # kilometer
    km_m = 1000.0
    # man efficiency
    x_max = 75
    x_min = 0
    y_max = 136
    y_min = 0

    # sorting sation
    sorting_sation_width = 1.2
    short_side_sorting_sation_num = 31
    sorting_sation_short_side_begin_coordinate = COORDINATE(18.0, 12.5)
    sorting_sation_short_side_end_coordinate = COORDINATE(96.0, 12.5)
    short_side_width_between_sorting_sations = 2.6

    long_side_sorting_sation_num = 31
    sorting_sation_long_side_begin_coordinate = COORDINATE(18.0, -12.5)
    sorting_sation_long_side_end_coordinate = COORDINATE(96.0, -12.5)
    long_side_width_between_sorting_sations = 2.6

    sorting_sation_num = short_side_sorting_sation_num + long_side_sorting_sation_num

    # storage area
    short_side_storage_area_num = 22
    storage_area_short_side_begin_coordinate = COORDINATE(20.0, 26.75)
    storage_area_short_side_end_coordinate = COORDINATE(104.0, 26.75)
    short_side_width_between_storage_areas = 4.0

    long_side_storage_area_num = 27
    storage_area_long_side_begin_coordinate = COORDINATE(0.0, -26.75)
    storage_area_long_side_end_coordinate = COORDINATE(104.0, -26.75)
    long_side_width_between_storage_areas = 4.0

    storage_area_length = 15.0
    storage_area_num = short_side_storage_area_num + long_side_storage_area_num

    # loading berth
    short_side_loading_berth_num = 22
    short_side_NC_loading_berth_num = 2
    short_side_unloading_berth_num = 5
    short_side_berth_num = short_side_NC_loading_berth_num + short_side_loading_berth_num
    loading_berth_short_side_begin_coordinate = COORDINATE(20.0, 37.5)
    loading_berth_short_side_end_coordinate = COORDINATE(132.0, 37.5)
    short_side_width_between_loading_berths = 4.0

    long_side_loading_berth_num = 27
    long_side_NC_loading_berth_num = 2
    long_side_unloading_berth_num = 5
    long_side_berth_num = long_side_NC_loading_berth_num + long_side_loading_berth_num
    loading_berth_long_side_begin_coordinate = COORDINATE(0.0, -37.5)
    loading_berth_long_side_end_coordinate = COORDINATE(132.0, -37.5)
    long_side_width_between_loading_berths = 4.0

    unloading_berth_num = short_side_unloading_berth_num + long_side_unloading_berth_num
    loading_berth_num = short_side_loading_berth_num + long_side_loading_berth_num
    NC_loading_berth_num = short_side_NC_loading_berth_num + long_side_NC_loading_berth_num


    # distance
    before_main_line_distance = 122.8412
    # big flow
    # sorting_sation_loads_ub = 30000
    sorting_sation_loads_ub = 12000

    sorting_sation_travel_level1_combine_rate_ub = 1.5
    sorting_sation_travel_level1_split_rate_lb = 2.0
    sorting_sation_travel_level1_num_ub = 2

    sorting_sation_travel_level2_combine_rate_ub = 1.2
    sorting_sation_travel_level2_split_rate_lb = 2.0
    sorting_sation_travel_level2_num_ub = 3

    sorting_sation_travel_level3_combine_rate_ub = 1.2
    sorting_sation_travel_level3_split_rate_lb = 2.0
    sorting_sation_travel_level3_num_ub = 2


    loading_berth_ub = 80000
    loading_berth_num_ub = 2

    # travel number
    travel_level_num_lb = 5
    # NC rate
    default_NC_rate = 0.0
    NC_rate_up_bound = 0.3
