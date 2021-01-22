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


__version__ = '0.5.0'
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
        已通过下面 get_input_ip() 实现
        '''
        # all_ip_file = config.get('common', 'all_ip_file')
        with open(all_ip_file, 'r') as f:
            all_ip_list = f.readlines()
        # 不使用下面的单行函数返回结果，是为了在循环中使用try，若格式异常可跳过，不影响整体运行。
        # all_ip = IPSet([IP(x.strip(), make_net=True) for x in all_ip_list])
        all_ip = IPSet()
        for x in all_ip_list:
            try:
                _i = IP(x.strip(), make_net=True)
                all_ip.add(_i)
            except Exception as err:
                pft(str_red('忽略无效ip：{}，\n\t错误原因：{}'.format(x, err)))
        return all_ip

    def get_input_ip(self, input_ip_file):
        '''
        获取输入的 IP
        与 get_all_ip() 功能相同，运行原理不同而已，容错性更好
        '''
        with open(input_ip_file) as f:
            input_ip_str = f.read().strip().split('\n')
        # 不使用下面的单行函数返回结果，是为了在循环中使用try，若格式异常可跳过，不影响整体运行。
        #input_ip = IPSet([IP(x.strip(), make_net=True) for x in input_ip_str.split('\n')])
        input_ip = IPSet()
        for x in input_ip_str:
            try:
                _i = IP(x.strip(), make_net=True)
                input_ip.add(_i)
            except Exception as err:
                pft(str_red('忽略无效ip：{}，\n\t错误原因：{}'.format(x, err)))
        return input_ip

    def compare(self, all_ip=IPSet(), input_ip=IPSet()):
        '''将输入的 IP 范围与完整的 IP 范围做比较，输出缺少的部分'''
        t0 = datetime.now()
        self.result = '\n'.join([x.strCompressed()
                                 for x in (all_ip - input_ip)])
        t1 = (datetime.now() - t0).total_seconds()
        pft(str_blue_green('运行用时：', '{:4.2f} s'.format(t1)))

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


def ip_to_last(_ip: str):
    '''ip/mask 转换为 ip_start-ip_end'''
    return '{}\t{}'.format(IP(_ip)[0].strCompressed(), IP(_ip)[-1].strCompressed())


def ip_from_last(_ip: str):
    '''ip_start-ip_end 转换为 ip/mask'''
    _start, _end = '', ''
    try:
        if '\t' in _ip:
            _start, _end = _ip.split('\t')
        if '-' in _ip:
            _start, _end = _ip.split('-')
    except:
        pft(str_red('IP格式不对，请检查。'))
        exit('>>运行结束。')

    def ip_len(a, b):
        return IP(b).int()-IP(a).int()+1
    ip_len_bin_str = '{:b}'.format(ip_len(_start, _end))
    nn = []
    for x in range(len(ip_len_bin_str)):
        if ip_len_bin_str[x] == "1":
            nn.append(x)
    _ver_len = 129 if _ip.find(':') != -1 else 33
    ll = [_ver_len-len(ip_len_bin_str)+x for x in nn]
    _res = []
    for x in ll:
        _x = IP(_start).make_net(x)
        _res.append(_x.strNormal())
        _start = IP(_x[-1].int()+1).strNormal()
    return _res


def ip_convert(_ip: str):
    '''IP 地址格式转换，自动判断，在 ip/mask 与 ip_start-ip_end 之间转换'''

    res = []
    _ip_list = _ip.strip().split('\n')
    try:
        ip_list = [IP(x.strip()) for x in _ip_list]
        # 每行一个 IP，则转换成 ip_start-ip_end
        for x in ip_list:
            res.append(ip_to_last(x))
    except:
        for x in _ip_list:
            res.extend(ip_from_last(x.strip()))
    return '\n'.join(res)


def ip_merge(file_name: str):
    '''IP 地址合并计算'''
    ...


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        # try:
        result = ip_integriry()
        result.main()
        # except Exception as err:
        # print('出错啦。错误信息：')
        # print(err)
    elif args[1] == 'convert':
        print(ip_convert(args[2]))
    elif args[1] == 'merge':
        print(ip_merge(args[2]))
    else:
        print('输入有误，请查看使用说明！')
    print('\n>>>>>>>>>>\n按任意键退出...\n')
    input()
