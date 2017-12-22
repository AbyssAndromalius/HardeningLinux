# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 10:29:42 2017

@author: abyss
"""

import string
import random

def pass_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

