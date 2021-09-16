# -*- encoding: utf-8 -*-
# @Time : 2021/9/7 9:05
# @Author : midww
# @File : salaryForecast.py

from .dataProcessing import *
import numpy as np
from sklearn.neighbors import KNeighborsRegressor


def salary_predict(ed, work_exp, cpy_size, job_label):
    file_path = 'E:/大学学业/大四上/行业大数据分析实践/IndustryBigDataAnalysisSystem/analysis/data/salaryForecast.csv'
    job_label_data, job_label_dict = get_job_label_data(file_path)
    ed_data = get_ed_data(file_path)
    work_exp_data = get_work_exp_data(file_path)
    salary_data = get_salary_data(file_path)
    cpy_size_date = get_cpy_size_data(file_path)
    x_data = np.hstack([ed_data, work_exp_data, cpy_size_date, job_label_data])
    kn_reg = KNeighborsRegressor(10)
    kn_reg.fit(x_data, salary_data)
    pre_data = [
        np.hstack((ed_pre([ed]), work_exp_pre([work_exp]), cpy_size_pre([cpy_size]), job_label_dict[job_label]))]
    return kn_reg.predict(pre_data)[0]
