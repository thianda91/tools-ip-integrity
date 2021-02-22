#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from IPy import IPint, IP, IPSet
from prompt_toolkit import prompt
# from prompt_toolkit import PromptSession
# from prompt_toolkit.history import FileHistory
from prompt_toolkit import print_formatted_text as pft
from prompt_toolkit.formatted_text import FormattedText
import sys
import traceback

__version__ = '0.7.0'
__author__ = ''.join(chr(x) for x in [20110, 26174, 36798, 46, 38081, 23725])

_RED = '#ff0066'
_GREEN = '#44ff00'
_BLUE = '#6600ff'
DEBUG_FILE = 'debug_log.txt'


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
    '''完整性类'''

    def __init__(self):
        ...

    def now(self) -> str:
        return datetime.strftime(datetime.now(), '%Y-%m-%d.%H%M%S')

    def get_input_ip(self, input_ip_file) -> IPSet:
        '''
        获取输入的 IP
        '''
        input_ip_str = _read_file(input_ip_file)
        # 不使用下面的单行函数返回结果，是为了在循环中使用try，若格式异常可跳过，不影响整体运行。
        #input_ip = IPSet([IP(x.strip(), make_net=True) for x in input_ip_str.split('\n')])
        input_ip = IPSet()
        for x in input_ip_str:
            try:
                # 尝试按照 ip / mask 解析
                _i = IP(x.strip(), make_net=True)
                input_ip.add(_i)
            except Exception as err:
                # 尝试按照 ip_start - ip_end 解析
                try:
                    _i = ip_from_last(x.strip(), True)
                    for xx in _i:
                        input_ip.add(xx)
                except Exception as err:
                    pft(str_red('忽略无效 ip：{}，\n\t错误原因：{}'.format(x, err)))
        return input_ip

    def compare(self, all_ip=IPSet(), input_ip=IPSet()) -> None:
        '''将输入的 IP 范围与完整的 IP 范围做比较，输出缺少的部分'''
        t0 = datetime.now()
        self.result = '\n'.join([x.strCompressed()
                                 for x in (all_ip - input_ip)])
        t1 = (datetime.now() - t0).total_seconds()
        pft(str_blue_green('运行用时：', '{:4.2f} s'.format(t1)))

    def incomplete(self) -> None:
        pft(str_blue('存在漏报的 IP：'))
        if sys.argv[-1] == '--cli':
            print('\n'.join(self.result))
        else:
            result_file = '遗漏.-{}.txt'.format(self.now())
            _write_file(result_file, self.result)
            pft(str_blue_green('结果已输出到：', '{}'.format(result_file)))

    def complete(self) -> None:
        pft(str_green('本次完整性检查无问题，好棒！'))

    def main(self) -> None:
        '''入口'''
        title = '*** 欢迎使用 IP 地址完整性核查工具 ***'
        pft(str_green(title))
        print('→→ 版本：V{}\n→→ 作者：{}'.format(__version__, __author__))
        pft(str_red('更多功能请阅读 README 或命令行运行：{} help'.format(sys.argv[0])))
        # session = PromptSession(history=FileHistory('.myhistory'))
        pft(str_blue('输入包含完整 IP 地址范围的文件名：(默认 all.txt)'))
        _all_ip_file = prompt('> ')
        if(_all_ip_file == ''):
            _all_ip_file = 'all.txt'
        all_ip = self.get_input_ip(_all_ip_file)
        pft(str_blue('输入要验证的文件名：(默认 input.txt)'))
        _input_ip_file = prompt('> ')
        if(_input_ip_file == ''):
            _input_ip_file = 'input.txt'
        input_ip = self.get_input_ip(_input_ip_file)
        self.compare(all_ip, input_ip)
        print('--------')
        if(self.result):
            self.incomplete()
        else:
            self.complete()


def _read_file(filename: str) -> list:
    '''
    获取输入的 IP

    使用 .readlines() 时，若文件结尾空行大于1，则会报错。
    使用 .read().strip().split('\n') 则不会。
    '''
    with open(filename, 'r') as f:
        # all_ip_list = f.readlines()
        input_ip_str = f.read().strip().split('\n')
    return input_ip_str


def _write_file(filename: str, res: str) -> None:
    '''把结果写到文件'''
    with open(filename, 'w') as f:
        f.write(res)


def ip_compare(filename_all: str, filename_in: str):
    ...


def ip_to_last(_ip) -> str:
    '''ip / mask 转换为 ip_start - ip_end'''
    ip = _ip if isinstance(_ip, IP) else IP(_ip)
    return '{}\t{}'.format(ip[0].strCompressed(), ip[-1].strCompressed())


def ip_from_last(_ip: str, ip_type: bool = False) -> list:
    '''
    ip_start - ip_end 转换为 ip / mask

    ip_type == Ture: return [IP()] else : [ip_str]
    '''
    _start, _end = '', ''
    if '\t' in _ip:
        _start, _end = _ip.split('\t')
    elif '-' in _ip:
        _start, _end = _ip.split('-')
    else:
        try:
            return ip_to_last(_ip)
        except:
            pft(str_red('IP 格式不对，请检查。'))
            exit('>>运行结束。')
    _start_int = IPint(_start).ip
    _end_int = IPint(_end).ip
    ip_len = _end_int-_start_int+1
    # IP 范围个数转成二进制文本
    ip_len_bin_str = '{:b}'.format(ip_len)
    # 计算二进制文本的长度
    _len = len(ip_len_bin_str)
    # 判断 ipv4 or ipv6
    _ver_len = 128 if _ip.find(':') != -1 else 32
    # 计算最小掩码
    _mask_min = _ver_len-_len+1
    # 构建计算结果
    def ip_handler(arg: IP):
        return arg if ip_type else arg.strCompressed()
    _res = []
    _res_1 = IP(_start).make_net(_mask_min)
    if _res_1.ip < _start_int:
        _res_1 -= IP(_start_int-1)
        for x in _res_1:
            if x.ip >= _start_int:
                _res.append(ip_handler(x))
        _middle = IP(_start_int+2**(_len-1)).make_net(_mask_min)
        _res.append(ip_handler(_middle))
    else:
        _res.append(ip_handler(_res_1))
    _res_2 = IP(_end).make_net(_mask_min)
    if _res_2[-1].ip > _end_int:
        _res_2 -= IP(_end_int+1)
        for x in _res_2:
            if x.ip <= _end_int:
                _res.append(ip_handler(x))
    return _res


def ip_convert(_input: str) -> str:
    '''IP 地址格式转换，自动判断，在 ip/mask 与 ip_start-ip_end 之间转换'''
    if _input == '-f':
        # 传入文件名
        res = []
        _ip_list = _read_file(sys.argv[3])
        for x in _ip_list:
            try:
                # 尝试将 ip/mask 转换为 IP()
                # 每行一个 IP()，则转换成 ip_start-ip_end
                res.append(ip_to_last(x.strip()))
            except:
                    res.extend(ip_from_last(x.strip()))
        return '\n'.join(res)
    else:
        try:
            ip = IP(_input, make_net=True)
            res = ip_to_last(ip)
        except:
            res = '\n'.join(ip_from_last(_input))
        return res


def ip_merge(_input: str):
    '''IP 地址合并计算'''
    res = IPSet()
    if _input == '-f':
        # 传入文件名
        ip_list = _read_file(sys.argv[3])
    else:
        # 传入若干 ip
        ip_list = sys.argv[2:]

    _ip_list = []
    for x in ip_list:
        if x.find('/') == -1:
            # 先转换为 ip / mask 格式
            _ip_list.extend(ip_from_last(x.strip(), True))
        else:
            res.add(IP(x.strip()))
    for xx in _ip_list:
        res.add(xx)
    return '\n'.join([x.strCompressed() for x in res])


def help():
    self_name = sys.argv[0]
    print(self_name)
    pft(str_red('更多使用说明请查看 README.pdf'))


if __name__ == '__main__':
    args = sys.argv
    try:
        if len(args) == 1:
            result = ip_integriry()
            result.main()
            print('\n>>>>>>>>>>\n按回车退出...\n')
            input()
        elif args[1] == 'compare' or args[1] == 'cp':
            print(ip_convert(args[2]))
        elif args[1] == 'convert' or args[1] == 'cv':
            print(ip_convert(args[2]))
        elif args[1] == 'merge' or args[1] == 'm':
            print(ip_merge(args[2]))
        elif args[1] == 'help' or args[1] == 'h':
            help()
        else:
            print('输入有误，请查看使用说明！')
    except Exception as err:
        print(err)
        traceback.print_exc(file=open(DEBUG_FILE, 'w'))
        pft(str_blue_green('出错啦。请反馈目录中的文件：', DEBUG_FILE))
