import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 从CSV读取数据
class PicTool:
    def __init__(self, target):
        self.target = target
        self.data = pd.read_csv(f'./{target}', sep=',', header=0, encoding='utf-8')
    
    