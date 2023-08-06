# -*- coding: utf-8 -*-
# /usr/bin/env python

'''
Author: wenqiangw
Email: wqwangchn@163.com
Date: 2022/10/20 14:55
Desc:
'''
import pandas as pd
import numpy as np
import dill

class InteractingMultipleModel(object):
    def __init__(self):
        self.multiple_model = None
        self.rule_function = None
        self.raw_model = None

    def load(self, model_name:str):
        model = dill.load(open(model_name, "rb"))
        self.multiple_model = model.get('models')
        self.rule_function = model.get('rule_function')
        self.preprocessing_function = model.get('preprocessing_function', self.func_preprocessing)
        self.interacting_function = model.get('interacting_function',self.func_interaction)
        self.info = model.get('info')
        self.raw_model = model.get('raw_model')
        self.calc_interactive_rules = lambda x: self.interacting_function(self.multiple_model, self.rule_function, x)

    def dump(self, model_list, model_name,  rule_function=None, interacting_function=None, preprocessing_function=None,
             raw_model_list=None, info=None):
        assert len(model_list)>1
        model = {
            'models': model_list,
            'rule_function': rule_function,
            'info': info,
            'raw_model':raw_model_list
        }
        if preprocessing_function != None:
            model.update({'preprocessing_func':preprocessing_function})
        if interacting_function != None:
            model.update({'interacting_function':interacting_function})
        dill.dump(model, open(model_name, "wb"), protocol=3)

    def save(self, model_name, type='all'):
        assert type in ['all', 'pure'], 'all for backup, pure for online'
        if type == 'pure':
            raw_model = None
        else:
            raw_model = self.raw_model
        model = {
            'models': self.multiple_model,
            'rule_function': self.rule_function,
            'preprocessing_function': self.preprocessing_function,
            'interacting_function': self.interacting_function,
            'info': self.info,
            'raw_model':raw_model
        }
        dill.dump(model, open(model_name, "wb"), protocol=3)

    def predict(self,data_):
        data=data_.copy()
        if self.multiple_model==None:
            multiple_model=[]
        elif isinstance(self.multiple_model,list):
            multiple_model=self.multiple_model
        else:
            multiple_model = [self.multiple_model]

        result_list = []
        for i,model_i in enumerate(multiple_model):
            result_i = model_i.predict(data)
            data,result_i = self.preprocessing_function(data,result_i)
            result_list.append(result_i)
        result = self.calc_interactive_rules(result_list)
        return result

    def func_interaction(self, model_list,rule_func,result_data):
        if len(result_data)<1:
            return {'score':0,'level':-1}
        return result_data[0]

    def func_preprocessing(self, data, result_i):
        return data, result_i


if __name__ == '__main__':
    model_name = "../data/score_card_model_online_o2o_tangshan_v3.2.0.pkl"
    model_interacting = InteractingMultipleModel()
    model_interacting.load(model_name)

    data = {
        'carnum': 'LBZ447DB1KA009342',
        'trip_cnt': 143,
        'run_meters': 12275107.380000005,
        'run_seconds': 771092,
        'trip_avg_meters': 85839.91174825176,
        'trip_avg_seconds': 5392.251748251748,
        'trip_avg_distance': 44253.81818181818,
        'high_meters_ratio': 0.002143811796129477,
        'province_meters_ratio': 0.34486200315422405,
        'high_trip_cnt_ratio': 0.0,
        'province_trip_cnt_ratio': 0.5874125874125874,
        'curvature_g2_trip_meters_ratio': 0.5600617817161611,
        'ng_23_6_seconds_ratio': 0.2924709373200604,
        'ng_23_6_trip_cnt_ratio': 0.4335664335664336,
        'daily_run_kmeters': 84.41548247018672,
        'daily_run_hours': 1.4729923918800238,
        'daily_trip_cnt': 0.9834059792344316,
        'daily_nohigh_kmeters': 84.23451156309116,
        'daily_ng_23_6_hours': 0.43080746551846827,
        'trip_long_cnt_ratio': 0.0,
        'day_high_meters_ratio': 0.0017513956769965135,
        'ng_province_meters_ratio': 0.10545102620519804,
        'morn_6_10_seconds_ratio': 0.13508245449310846,
        'dusk_17_20_seconds_ratio': 0.19514792009254409,
        'ng_23_6_avg_speed': 60.85796919147581,
        'morn_6_10_avg_speed': 55.72396178992139,
        'dusk_17_20_avg_speed': 51.151944177515524,
        'low_speed_seconds_ratio': 0.3662662821038216,
        'low_speed_block_cnt_ratio': 0.2351517298382336,
        'week_1_5_seconds_ratio': 0.29913551171585234,
        'geohash4_top10_meters_ratio': 0.9702472802319388,
        'trip_r30m_cnt_ratio': 0.4795918367346938,
        'common_line_top30_cnt_ratio': 0.030769230769230767,
        'mil_ratio_province_hb': 1.0,
        'mil_ratio_province_tj': 0.0,
        'mil_ratio_province_else': 0.0,
        'mil_ratio_city_ts': 1.0,
        'mil_ratio_city_around': 0.0,
        'mil_ratio_city_else': 0.0,
        'mil_ratio_county_west': 0.0015470292366599212,
        'mil_ratio_county_south': 0.5677351500284784,
        'mil_ratio_county_east': 0.2494958703978352,
        'mil_ratio_county_else': 0.18122195033702654,
        'top1_city_mileage_rate': 1.0,
        'top2_city_mileage_rate': 1.0,
        'top1_province_mileage_rate': 1.0,
        'top2_province_mileage_rate': 1.0,
        'top1_county_mileage_rate': 0.3229254357854749,
        'top2_county_mileage_rate': 0.5677351500284797,
        'ratio_nonglinmufu': 0.0290325496489345,
        'ratio_meitan': 0.0006003401293231343,
        'ratio_gangtie': 0.1395834542570436,
        'ratio_shashi': 0.017055577543834046,
        'ratio_kuaidi': 0.08425476464525228,
        'ratio_jiadian': 0.004164982562417855,
        'ratio_fengdian': 0.0,
        'ratio_jixie': 0.6604690662393785,
        'ratio_qiche': 0.0006478740548063132,
        'ratio_other': 0.06419139091900974,
        'pred': '机械',
        'triggertime': '2021-04-02 02:35:52',
        'triggertime_end': '2021-08-29 22:33:06',
        'source': 10
     }
    out = model_interacting.predict(data)
    print(out)