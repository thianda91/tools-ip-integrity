#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from datetime import datetime
from IPy import IP, IPSet


__version__ = '0.1.0'
configFileName = 'config_{}.ini'.format(__version__)
config = configparser.ConfigParser()
config.read(configFileName)
t0 = datetime.now()


# 当前时间的字符串
def now():
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')


class ip_integriry(object):
    '''完整性类
    IP_FORMAT :
    0: single
    1: start-end
    '''

    def __init__(self, input_str=''):
        self.IP_FORMAT = 0
        self.input_str = input_str
        print(self.get_all_ip())

    def get_all_ip(self):
        '''获取完整的 IP 范围'''
        all_ip_file = config.get('common', 'all_ip_file')
        with open(all_ip_file, 'r') as f:
            all_ip_list = f.readlines()
        all_ip = IPSet([IP(x.strip()) for x in all_ip_list])
        return all_ip

    def get_input_ip(self, input_ip_str):
        '''获取输入的 IP'''
        input_ip = IPSet([IP(x.strip()) for x in input_ip_str.split('\n')])
        return input_ip

    def compare(self, all_ip, input_ip):
        '''将输入的 IP 范围与完整的 IP 范围做比较，输出缺少的部分'''
        self.result = [x.strCompressed() for x in (all_ip - input_ip)]
        return '\n'.join(self.result)



    def main(self):
        '''入口'''



if __name__ == '__main__':
    try:
        result = ip_integriry()
    except Exception as err:
        print('出错啦。错误信息：')
        print(err)

    t = datetime.now() - t0
    print('\n执行用时：%2.4f s' % t.total_seconds())
