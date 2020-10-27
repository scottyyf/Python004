#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: test.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import os
import re
from lxml.etree import HTML
import glob


class ProjectPara:
    def __init__(self, project_dir, tail_tag='html'):
        self.tail_tag = tail_tag
        self.abs_project_dir = project_dir
        self._project_name = os.path.basename(self.abs_project_dir)

        self.abs_files_list = []
        self.files_name = []
        self._get_file_list()

    def _get_file_list(self):
        self.abs_files_list = glob.glob(
            f'{self.abs_project_dir}/*.{self.tail_tag}')

    @property
    def files_list(self):
        return self.abs_files_list

    @property
    def project_name(self):
        return self._project_name


class GetProjectFiles:
    def __init__(self,
                 xunjian_dir='/home/scott/work/xunjian/巡检分析报'
                             '告SLES-2020-YYF/待分析数据'):
        self.xunjian_dir = xunjian_dir
        self._projects_list = []

    def get_projects_list(self):
        xunjian_projects = glob.glob(f'{self.xunjian_dir}/*')
        for project_dir in xunjian_projects:
            project_data = ProjectPara(project_dir)
            self._projects_list.append(project_data)

    @property
    def projects_list(self):
        return self._projects_list


class Parse:
    def __init__(self, file_path):
        self.selector = None
        self.file_path = file_path
        self._set_selector()

    def dumplicate_check(self, start_num, xpath_reg: str, step=4):
        """due to html wrong set"""
        start_at = start_num - step
        stop_at = start_num + step + 1
        if start_at < 0:
            start_at = 0

        ret = []
        # '/html/body/table/tr[{0}]/td[2]/text()'
        for i in range(start_at, stop_at):
            if i == start_num:
                continue

            _xpath = xpath_reg.format(i)
            _ret = self.selector.xpath(_xpath)
            ret.extend(_ret)

        return ret

    def _set_selector(self):
        content = ''
        try:
            with open(self.file_path, 'r') as f:
                content = f.read()
        except UnicodeDecodeError as e:
            print(self.file_path, '8' * 8)

        if content:
            self.selector = HTML(content)

    def host_name(self):
        if self.selector is None:
            return ''

        _host_name = ''
        try:
            _host_name = self.selector.xpath('/html/body/div/h3/u[1]/text()')[0]
        except Exception as e:
            print(f'Failed to get host name, details: {e}')
        return _host_name

    def risk_kernel_info(self):
        if self.selector is None:
            return ''

        _kernel_version = ''
        try:
            _kernel_version = self.selector.xpath(
                '/html/body/table/tr[2]/td[2]/text()')[2][5:]
            if '2.6.32.12-0.7' not in _kernel_version:
                _kernel_version = ''

        except Exception:
            pass

        if not _kernel_version:
            ret = self.dumplicate_check(
                2, '/html/body/table/tr[{0}]/td[2]/text()')
            for value in ret:
                if '2.6.32.12-0.7' in value:
                    _kernel_version = value
                    break

        return _kernel_version

    def risk_disk_usage(self):
        if self.selector is None:
            return []

        disk_info = self.selector.xpath('/html/body/table/tr[7]/td[2]/text()')
        disk_usage_risk = []
        percent = re.compile(r'(.*)([0-9]{2}%)?([0-9]{2})%(.*)')
        for i in disk_info:
            ret = percent.search(i)
            if not ret:
                continue

            if int(ret.group(3)) >= 90:
                disk_usage_risk.append(i)
            elif ret.group(2) and int(ret.group(2)[:-2]) >= 90:
                disk_usage_risk.append(i)

        if not disk_usage_risk:
            ret = self.dumplicate_check(
                7, '/html/body/table/tr[{0}]/td[2]/text()', step=1)
            for i in ret:
                if '(%)' in i:
                    continue

                result = percent.search(i)
                if not result:
                    continue

                if int(result.group(3)) >= 90:
                    disk_usage_risk.append(i)
                elif result.group(2) and int(result.group(2)[:-2]) >= 90:
                    disk_usage_risk.append(i)

        return disk_usage_risk

    def risk_mem_usage(self, mem_risk_percent=85, swap_risk_percent=50):
        if self.selector is None:
            return []

        mem_data = []
        mem_info = self.selector.xpath('/html/body/table/tr[6]/td[2]/text()')
        for i in mem_info:
            if '内存使用率(%)：' in i:
                _c = re.compile(r'(.*)：(.*)%')
                ret = _c.search(i)
                mem_percent = ret.group(2)
                if float(mem_percent) >= mem_risk_percent:
                    mem_data.append(i)

            if 'Swap总容量(MB)：0MB' in mem_info:
                mem_data.append('Swap总容量(MB)：0MB, 未设置swap')
                break

            if 'Swap使用率(%)' in i:
                _c = re.compile(r'(.*)：(.*)%')
                ret = _c.search(i)
                swap_percent = ret.group(2)
                if float(swap_percent) >= swap_risk_percent:
                    mem_data.append(i)

        if not mem_data:
            ret = self.dumplicate_check(
                6, '/html/body/table/tr[{0}]/td[2]/text()', step=3)
            for i in ret:
                if '内存使用率(%)：' in i:
                    _c = re.compile(r'(.*)：(.*)%')
                    ret = _c.search(i)
                    mem_percent = ret.group(2)
                    if float(mem_percent) >= mem_risk_percent:
                        mem_data.append(i)

                if 'Swap总容量(MB)：0MB' in mem_info:
                    mem_data.append('Swap总容量(MB)：0MB, 未设置swap')
                    break

                if 'Swap使用率(%)' in i:
                    _c = re.compile(r'(.*)：(.*)%')
                    ret = _c.search(i)
                    swap_percent = ret.group(2)
                    if float(swap_percent) >= swap_risk_percent:
                        mem_data.append(i)

        return mem_data

    def risk_file_sys_not_clean(self):
        if self.selector is None:
            return []

        file_system_info = self.selector.xpath(
            '/html/body/table/tr[7]/td[2]/text()')
        file_sys_not_clean = []
        for file_sys in file_system_info:
            if 'filesystem state:' in file_sys.lower() and 'not clean' in \
                    file_sys.lower():
                file_sys_not_clean.append(file_sys)

        if not file_sys_not_clean:
            ret = self.dumplicate_check(
                7, '/html/body/table/tr[{0}]/td[2]/text()')
            for i in ret:
                if 'filesystem state:' in i.lower() and 'not clean' in \
                        i.lower():
                    file_sys_not_clean.append(i)

        return file_sys_not_clean

    def risk_disk_io_error(self):
        if self.selector is None:
            return []

        disk_io_error_in_message = self.selector.xpath(
            '/html/body/table/tr[12]/td[2]/text()')
        disk_io_error = self.selector.xpath(
            '/html/body/table/tr[13]/td[2]/text()')
        disk_io_error.extend(disk_io_error_in_message)
        io_error_data = set()
        for io_error in disk_io_error:
            if 'i/o error' in io_error.lower():
                if 'dev fd0' in io_error.lower():
                    continue

                io_error_data.add(io_error.strip())

        if not io_error_data:
            ret = self.dumplicate_check(
                12, '/html/body/table/tr[{0}]/td[2]/text()', step=2)
            for io_error in ret:
                if 'i/o error' in io_error.lower():
                    if 'dev fd0' in io_error.lower():
                        continue

                    io_error_data.add(io_error.strip())

        return list(io_error_data)

    def risk_zombie_process(self):
        if self.selector is None:
            return ''

        process_state = self.selector.xpath(
            '/html/body/table/tr[10]/td[2]/text()')
        tasks = process_state[1]
        _c = re.compile(r'.*, +(\d{1,10}) zombie.*')
        ret = _c.search(tasks)
        if ret:
            ret = int(ret.group(1))
            if ret > 0:
                return tasks

        if not ret:
            ret = self.dumplicate_check(
                10, '/html/body/table/tr[{0}]/td[2]/text()')
            for i in ret:
                result = _c.search(i)
                if not result:
                    continue

                if int(result.group(1)) > 0:
                    return i

        return ''

    def risk_nproc_spell_error(self):
        if self.selector is None:
            return []

        sysctl_info = self.selector.xpath(
            '/html/body/table/tr[20]/td[2]/text()')
        noproc_err = []
        for i in sysctl_info:
            if 'noproc' in i.strip().lower():
                noproc_err.append(i)

        if not noproc_err:
            ret = self.dumplicate_check(
                20, '/html/body/table/tr[{0}]/td[2]/text()')
            for i in ret:
                if 'hard noproc' in i.strip().lower():
                    print('type of i is ')
                    print(type(i))
                    noproc_err.append(i)

        return noproc_err

    def risk_bond_down(self):
        if self.selector is None:
            return []

        bond_info = self.selector.xpath('/html/body/table/tr[9]/td[2]/text()')
        bond_down_info = []
        _c = re.compile(r'Slave Interface: +(.*)')
        for i, value in enumerate(bond_info):
            if 'MII Status: down' in value:
                ret = _c.search(bond_info[i - 1])
                if not ret:
                    continue

                ret = f'{bond_info[i - 1]} MII Status: down'
                bond_down_info.append(ret)

        if not bond_down_info:
            ret = self.dumplicate_check(
                9, '/html/body/table/tr[{0}]/td[2]/text()', 2)
            for i, value in enumerate(bond_info):
                if 'MII Status: down' in value:
                    ret = _c.search(bond_info[i - 1])
                    if not ret:
                        continue

                if not bond_info[i - 1].strip().lower().startswith(
                        'Slave Interface'):
                    continue

                ret = f'{bond_info[i - 1]} MII Status: down'
                bond_down_info.append(ret)

        return bond_down_info

    def risk_ntp_not_running(self):
        if self.selector is None:
            return ''

        ntp_info = self.selector.xpath('/html/body/table/tr[14]/td[2]/text()')
        if ntp_info:
            is_not_running = ntp_info[0]
            if 'ntp is not running' in is_not_running:
                return is_not_running

        ret = self.dumplicate_check(
            14, '/html/body/table/tr[{0}]/td[2]/text()')
        for i in ret:
            if 'ntp is not running' in i:
                return i

        return ''

    def risk_hardware_error(self):
        if self.selector is None:
            return []

        hardware_error_sum = set()
        hardware_in_message = self.selector.xpath(
            '/html/body/table/tr[12]/td[2]/text()')
        hardware_in_dmesg = self.selector.xpath(
            '/html/body/table/tr[13]/td[2]/text()')
        hardware_in_dmesg.extend(hardware_in_message)
        for i in hardware_in_dmesg:
            if 'this is not a software error' in i.lower():
                hardware_error_sum.add(i)

        if hardware_error_sum:
            return list(hardware_error_sum)[:3]

        ret = self.dumplicate_check(
            12, '/html/body/table/tr[{0}]/td[2]/text()', step=8)

        for i in ret:
            if 'this is not a software error' in i.lower():
                hardware_error_sum.add(i)

        if hardware_error_sum:
            return list(hardware_error_sum)[:3]

        return []

    def risk_ntp_out_scope(self):
        if self.selector is None:
            return ''

        ret = self.selector.xpath('/html/body/table/tr[14]/td[2]/text()')
        _c = re.compile(
                r'(\S*) *(\S*) *(\S*) *(\S]*) *(\S*) *(\S*) *(\S*) *(\S*) *('
                r'\S*) *(\S*)')

        ret = self._ntp_le_500(ret, _c)
        if ret:
            return ret

        ret = self.dumplicate_check(
            14, '/html/body/table/tr[{0}]/td[2]/text()', step=5)
        for i in ret:
            result = self._ntp_le_500(i, _c)
            if result:
                return result

        return ''

    def _ntp_le_500(self, ret: list, _c):
        if not ret:
            return ''

        if len(ret) < 3:
            return ''

        if 't when poll reach' not in ret[0] or '===' not in ret[1]:
            return ''

        ret = _c.search(ret[2])
        if abs(float(ret.group(9))) >= 500:
            return ret.group(9)

        return ''


project_files = GetProjectFiles()
project_files.get_projects_list()


def main1():
    sum = 0
    for project_data in project_files.projects_list:
        for simple_file in project_data.files_list:
            sum += 1

    print(sum)

def main():
    total_data = {}
    for project_data in project_files.projects_list:
        result = []

        for i, every_file in enumerate(project_data.files_list):
            per_sub_data = {}
            file_data = {}
            parse = Parse(every_file)
            host_name = parse.host_name()
            risk_kernel = parse.risk_kernel_info()
            disk_risk = parse.risk_disk_usage()
            risk_mem = parse.risk_mem_usage()
            risk_fs_not_clean = parse.risk_file_sys_not_clean()
            risk_disk_io_err = parse.risk_disk_io_error()
            risk_zomb_process = parse.risk_zombie_process()
            risk_nproc_error = parse.risk_nproc_spell_error()
            risk_bond_down = parse.risk_bond_down()
            risk_ntp_out_scope = parse.risk_ntp_out_scope()
            risk_ntp_not_run = parse.risk_ntp_not_running()
            risk_hardware_error = parse.risk_hardware_error()

            file_data.setdefault('risk_kernel', risk_kernel)
            file_data.setdefault('risk_disk_usage', disk_risk)
            file_data.setdefault('risk_mem', risk_mem)
            file_data.setdefault('risk_fs_not_clean', risk_fs_not_clean)
            file_data.setdefault('risk_disk_io_err', risk_disk_io_err)
            file_data.setdefault('risk_zomb_process', risk_zomb_process)
            file_data.setdefault('risk_nproc_error', risk_nproc_error)
            file_data.setdefault('risk_bond_down', risk_bond_down)
            file_data.setdefault('risk_ntp_out_scope', risk_ntp_out_scope)
            file_data.setdefault('risk_ntp_not_run', risk_ntp_not_run)
            file_data.setdefault('risk_hardware_error', risk_hardware_error)

            per_sub_data.setdefault(host_name, file_data)

            result.append(per_sub_data)

        total_data.setdefault(project_data.project_name, result)

    for project_name, list_data in total_data.items():
        print()
        print('*' * 70)
        print('*' * 70)
        print("*" * 20, project_name, '*' * 20)
        print('1). hosts name')
        for i, host_dict in enumerate(list_data):
            if i % 4 == 0:
                print()

            for i, data in host_dict.items():
                print(i, end='\t')

        print()
        print("#" * 20, 'risk kernel', '#' * 20)
        print('2) kernel risk info')
        for i, host_dict in enumerate(list_data):
            for i, data in host_dict.items():
                ret = data.get('risk_kernel')
                if ret:
                    print(
                        i, '#', f'还在使用有bug的默认kerne {ret.strip()} ，建议升级')

        print()
        print("#" * 20, 'risk disk usage', '#' * 20)
        print('3) disk usage risk info')
        for i, host_dict in enumerate(list_data):
            for i, data in host_dict.items():
                ret = data.get('risk_disk_usage')
                if ret:
                    print(i, '#', ''.join(ret).replace('\n', '@'))

        print()
        print("#" * 20, 'risk mem usag', '#' * 20)
        print('4) risk memery usage info')
        for i, host_dict in enumerate(list_data):
            for i, data in host_dict.items():
                ret = data.get('risk_mem')
                if ret:
                    print(i, '#',
                          ''.join(ret).replace('\n', '@'))

        print()
        print("#" * 20, 'risk filesystem not clean', '#' * 20)
        print('5) risk filesystem not clean')
        for i, host_dict in enumerate(list_data):
            for i, data in host_dict.items():
                ret = data.get('risk_fs_not_clean')
                if ret:
                    print(i, '#',
                          ''.join(ret).replace('\n', '@'))

        print()
        print("#" * 20, 'risk disk io error', '#' * 20)
        print('6) risk disk io error')
        for i, host_dict in enumerate(list_data):
            for i, data in host_dict.items():
                ret = data.get('risk_disk_io_err')
                if ret:
                    print(i, '#',''.join(ret[:3]).replace('\n', '@'))

        print()
        print("#" * 20, 'risk zombie process', '#' * 20)
        print('7) risk zombie process')
        for i, host_dict in enumerate(list_data):
            for i, data in host_dict.items():
                ret = data.get('risk_zomb_process')
                if ret:
                    print(i, '#', ret)

        print()
        print("#" * 20, 'risk nproc spell error', '#' * 20)
        print('8) risk nproc spell error')
        for i, host_dict in enumerate(list_data):
            for i, data in host_dict.items():
                ret = data.get('risk_nproc_error')
                if ret:
                    print(i, '#', ''.join(ret).replace('\n', '@'))

        print()
        print("#" * 20, 'risk bonding interface down', '#' * 20)
        print('9) risk bonding interface down')
        for i, host_dict in enumerate(list_data):
            for i, data in host_dict.items():
                ret = data.get('risk_bond_down')
                if ret:
                    print(i, '#', ''.join(ret).replace('\n', '@'))

        print()
        print("#" * 20, 'risk ntp out scope', '#' * 20)
        print('10) risk ntp out scope')
        for i, host_dict in enumerate(list_data):
            for i, data in host_dict.items():
                ret = data.get('risk_ntp_out_scope')
                if ret:
                    print(i, '\t', ret)

        print()
        print("#" * 20, 'risk ntp not running', '#' * 20)
        print('11) risk ntp not running')
        for i, host_dict in enumerate(list_data):
            for i, data in host_dict.items():
                ret = data.get('risk_ntp_not_run')
                if ret:
                    print(i, '#', ret)

        print()
        print("#" * 20, 'risk hardware error', '#' * 20)
        print('12) risk hardware error')
        for i, host_dict in enumerate(list_data):
            for i, data in host_dict.items():
                ret = data.get('risk_hardware_error')
                if ret:
                    print(i, '#', ''.join(ret).replace('\n', '@'))


if __name__ == '__main__':
    main()
