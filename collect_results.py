#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import json
from collections import defaultdict
import matplotlib.pyplot as plt
from tabulate import tabulate

rows = defaultdict(list)

for dname in glob.glob('results/*'):
    if not os.path.isdir(dname):
        continue
    if not os.path.exists('{}/log'.format(dname)):
        print(dname)
        continue
    log = json.load(open('{}/log'.format(dname)))
    args = json.load(open('{}/args'.format(dname)))
    rows[args['model_name']].append(
        (log[-1]['val/main/accuracy'], log, args, dname))

headers = [
    'model_name',
    'val/main/accuracy',
    'epoch',
    'batchsize',
    'crop_size',
    'expand_ratio',
    'pca_sigma',
    'random_angle',
    'weight_decay',
    'initial_lr',
    'lr_decay_rate',
    'lr_decay_epoch',
]

values = defaultdict(list)
for model_name, rows in rows.items():
    rows = sorted(rows, reverse=True)
    for acc, log, args, dname in rows:
        for key, value in log[-1].items():
            if key not in headers:
                continue
            values[key].append(value)
        for key, value in args.items():
            if key not in headers:
                continue
            values[key].append(value)
for key, val in values.items():
    print(key, len(val))
print(tabulate(values, headers='keys', tablefmt='pipe'))

# print('=' * 20)

# for model_name, row in rows.items():
#     dname = sorted(row)[-1][2]
#     print(dname)
#     acc = [l['val/main/accuracy']
#            for l in json.load(open('{}/log'.format(dname)))]
#     plt.plot(acc, label='')

# print('=' * 20)

# for model_name, row in rows.items():
#     for r in sorted(row, reverse=True):
#         print(r[1])
