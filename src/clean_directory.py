__author__ = 'Jonathan Rubin'

import os

def run(directory):
    for file1 in os.listdir(directory):
        os.system("rm " + file1)