"""
Name: MapReduce.py
Author: Quoc Cuong Nguyen
Contact: cuongbo2000@icloud.com
Time: 01/10/2021 08:13
Desc:
"""

import json


class MapReduce:
    def __init__(self):
        self.intermediate = {}
        self.result = []

    def emit_intermediate(self, key, value):
        self.intermediate.setdefault(key, [])
        self.intermediate[key].append(value)

    def emit(self, value):
        self.result.append(value)

    def execute(self, data, mapper, reducer):
        for line in data:
            record = json.loads(line)
            mapper(record)
        for key in self.intermediate:
            reducer(key, self.intermediate[key])
        # jenc = json.JSONEncoder(encoding='utf-8')
        jenc = json.JSONEncoder()
        for item in self.result:
            print(jenc.encode(item))

