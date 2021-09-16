# -*- encoding: utf-8 -*-
# @Time : 2021/9/6 11:14
# @Author : midww
# @File : dataProcessing.py
import pandas as pd
import numpy as np
import re


def get_data(file_path, data_name):
    data_file = open(file_path, 'r', encoding='UTF-8')
    data = pd.read_csv(data_file)[data_name]
    data_file.close()

    return data


def ed_pre(data):
    edu_bg_dict = {'学历不限': 0.05, '大专': 0.15, '本科': 0.20, '硕士': 0.30, '博士': 0.40}
    return [edu_bg_dict[i] for i in data]


def get_ed_data(file_path):
    data = get_data(file_path, '学历要求')
    edu_bg_list = ed_pre(data)
    return np.array(edu_bg_list)[:, np.newaxis]


def get_salary_data(file_path):
    data = get_data(file_path, '工资')
    SalaryList = []
    for OldSalary in data:
        NumList = [int(i) for i in re.findall('[0-9]+', OldSalary)]
        SalaryList.append(NumList[0])

    return np.array(SalaryList)


def work_exp_pre(data):
    work_exp_dict = {'经验不限': 0.1, '1-3年': 0.2, '3-5年': 0.4, '5-10年': 0.7, '10年以上': 1}
    return [work_exp_dict[i] for i in data]


def get_work_exp_data(file_path):
    data = get_data(file_path, '工作经验')
    work_exp_list = work_exp_pre(data)
    return np.array(work_exp_list)[:, np.newaxis]


def cpy_size_pre(data):
    cpy_size_dict = {'0-20人': 0.001, '20-99人': 0.005, '100-499人': 0.025, '500-999人': 0.05, '1000-9999人': 0.5,
                     '10000人以上': 1}
    return [cpy_size_dict[i] for i in data]


def get_cpy_size_data(file_path):
    data = get_data(file_path, '公司规模')
    cpy_size_list = cpy_size_pre(data)
    return np.array(cpy_size_list)[:, np.newaxis]


def get_job_label_data(file_path):
    data = get_data(file_path, '标签')
    label_list = list(set(data))
    label_list.sort()
    label_dict = dict(zip(label_list, range(len(label_list))))

    num_label_list = [label_dict[data[i]] for i in range(len(data))]
    return np.array(num_label_list)[:, np.newaxis], label_dict
