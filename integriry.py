#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from IPy import IP, IPSet
from prompt_toolkit import prompt
# from prompt_toolkit import PromptSession
# from prompt_toolkit.history import FileHistory
from prompt_toolkit import print_formatted_text as pft
from prompt_toolkit.formatted_text import FormattedText
import sys


__version__ = '0.4.0'
__author__ = ''.join(chr(x) for x in [20110, 26174, 36798, 46, 38081, 23725])

_RED = '#ff0066'
_GREEN = '#44ff00'
_BLUE = '#6600ff'


# 当前时间的字符串
def now():
    return datetime.strftime(datetime.now(), '%Y-%m-%d.%H%M%S')


def str_red(s):
    return FormattedText([(_RED, s)])


def str_green(s):
    return FormattedText([(_GREEN, s)])


def str_blue(s):
    return FormattedText([(_BLUE, s)])


def str_blue_green(s1, s2):
    return FormattedText([(_BLUE, s1), (_GREEN, s2)])


class ip_integriry(object):
    '''完整性类
    IP_FORMAT :
    1: single
    2: start-end
    '''

    def __init__(self, input_str=''):
        self.IP_FORMAT = 1
        self.input_str = input_str

    def now(self):
        return datetime.strftime(datetime.now(), '%Y-%m-%d.%H%M%S')

    def get_all_ip(self, all_ip_file):
        '''
        获取完整的 IP 范围
        使用 .readlines() 时，若文件结尾空行大于1，则会报错。
        使用 .read().strip().split('\n') 则不会。
        '''
        # all_ip_file = config.get('common', 'all_ip_file')
        with open(all_ip_file, 'r') as f:
            all_ip_list = f.readlines()
        # all_ip = IPSet([IP(x.strip(), make_net=True) for x in all_ip_list])
        all_ip = IPSet()
        for x in all_ip_list:
            try:
                _i = IP(x.strip(),make_net=True)
                all_ip.add(_i)
            except Exception as err:
                pft(str_red('忽略无效ip：{}，\n\t错误原因：{}'.format(x,err)))
        return all_ip

    def get_input_ip(self, input_ip_file):
        '''
        获取输入的 IP
        与 get_all_ip() 功能相同，运行原理不同而已
        '''
        with open(input_ip_file) as f:
            input_ip_str = f.read().strip()
        #input_ip = IPSet([IP(x.strip(), make_net=True) for x in input_ip_str.split('\n')])
        input_ip = IPSet()
        for x in input_ip_str.split('\n'):
            try:
                _i = IP(x.strip(),make_net=True)
                input_ip.add(_i)
            except Exception as err:
                pft(str_red('忽略无效ip：{}，\n\t错误原因：{}'.format(x,err)))
        return input_ip

    def compare(self, all_ip=IPSet(), input_ip=IPSet()):
        '''将输入的 IP 范围与完整的 IP 范围做比较，输出缺少的部分'''
        t0 = datetime.now()
        self.result = '\n'.join([x.strCompressed()
                                 for x in (all_ip - input_ip)])
        t1 = (datetime.now() - t0).total_seconds()
        pft(str_blue('运行用时：{:4.2f} s'.format(t1)))

    def incomplete(self):
        if sys.argv[-1] == '--cli':
            print('遗漏的 IP 段如下：\n'.format('\n'.join(self.result)))
        else:
            result_file = 'result-{}.txt'.format(self.now())
            with open(result_file, 'w') as f:
                f.write(self.result)
            pft(str_blue_green('存在漏报的IP！请注意查收。结果已输出到：', '{}'.format(result_file)))

    def complete(self):
        pft(str_green('本次完整性检查无问题，好棒！'))

    def main(self):
        '''入口'''
        title = '*** 欢迎使用IP地址完整性核查工具 ***'
        pft(str_green(title))
        print('→→ 版本：V{}\n→→ 作者：{}'.format(__version__, __author__))
        # session = PromptSession(history=FileHistory('.myhistory'))
        pft(str_blue('输入包含完整IP地址范围的文件名：(默认 all.txt)'))
        _all_ip_file = prompt('> ')
        if(_all_ip_file == ''):
            _all_ip_file = 'all.txt'
        all_ip = self.get_input_ip(_all_ip_file)
        pft(str_blue('输入要验证的文件名：(默认 input.txt)'))
        _input_ip_file = prompt('> ')
        if(_input_ip_file == ''):
            _input_ip_file = 'input.txt'
        pft(str_blue('选择输入的IP格式：(默认 1)'))
        _ip_format = prompt('1. 每行1个IP\n2. 每行含2个IP（起、止IP）\n> ')
        if _ip_format == 1:
            pass
        elif _ip_format == 2:
            # todo
            pass
        else:
            _ip_format = self.IP_FORMAT
        input_ip = self.get_input_ip(_input_ip_file)
        self.compare(all_ip, input_ip)
        print('--------')
        if(self.result):
            self.incomplete()
        else:
            self.complete()


if __name__ == '__main__':
    # try:
    result = ip_integriry()
    result.main()
    # except Exception as err:
        # print('出错啦。错误信息：')
        # print(err)
    print('\n>>>>>>>>>>\n按任意键退出...\n')
    input()
