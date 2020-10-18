#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: exception_test.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""

# import pretty_errors


class TestOpen:
    def __enter__(self):
        print('enter func is so called')
        f = open('/etc/passwd', 'r')
        self.f = f
        return f

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            self.f.close()
            return

        print('error')

    def __call__(cls, *args, **kwargs):
        print('============called')


class UserError(Exception):
    def __init__(self, error_info):
        self.info = error_info

    def __str__(self):
        return 'self designed error with info: {0}'.format(self.info)


def main1():
    user_input = 'a'

    try:
        if not user_input.isdigit():
            raise UserError('input error')

    except UserError as e:
        1/0

    finally:
        del user_input

    # print(user_input)


def main():
    with TestOpen() as f:
        print(f.read())


if __name__ == "__main__":
    main()
