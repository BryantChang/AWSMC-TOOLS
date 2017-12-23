import re
import os


class Properties:
    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}

        fopen = open(self.file_name, 'r')
        for line in fopen:
            line = line.strip()
            if line.find('=') > 0 and not line.startswith('#'):
                strs = line.split('=')
                self.properties[strs[0].strip()] = strs[1].strip()
        fopen.close()

    def has_key(self, key):
        return key in self.properties

    def get(self, key, default_value=''):
        if key in self.properties:
            return self.properties[key]
        return default_value



def parse(file_name):
    return Properties(file_name)


