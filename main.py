import time

from inputData import INPUTDATA
from model import MODEL
from flow import FLOWINFO
from algs import ALGS
from dynamicBerths import DYNAMICBERTHS

if __name__ == '__main__':
    start = time.process_time()
    print('start: ', start)
    input_file = './input/'
    data_list = ['20200301-20200325', '20200402-20200408', '20200401-20200416','20200301-20200429']
    input_data = INPUTDATA(input_file + data_list[3] + '/')

    flow_info = FLOWINFO(input_data,False,False)
    model = MODEL(flow_info)
    algs = ALGS(model)
    algs.model.show_encoding()
    algs.model.show_fit()
    # encoding_record = algs.model.set_encoding_record()

    # dynamic loading berths
    dynamicBerths = DYNAMICBERTHS(input_data)
    # no NC functions
    dynamicBerths.no_NC_plots()
    # NC functions
    dynamicBerths.NC_plots()

    print('end: ', time.process_time() - start)