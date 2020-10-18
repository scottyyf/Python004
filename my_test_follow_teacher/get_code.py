#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: get_code.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""

from PIL import Image
import pytesseract


img = Image.open('cap.jpg')
# img.show()

gray = img.convert('L')
gray.save('test_g.jpg')

# img.close()
# img.close()

threshold = 100
table = []

for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

out = gray.point(table, '1')
out.save('test_th.jpg')

th = Image.open('test_th.jpg')
print(pytesseract.image_to_string(th, lang='chi_sim+eng').strip())