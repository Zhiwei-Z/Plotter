import os
import shutil
import json
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from collections import defaultdict


class Graph:
    def __init__(self, title, x_label, y_label):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.fig, (self.axis) = plt.subplots(1, 1)
        self.axis.set_title(self.title)
        self.axis.set_xlabel(self.x_label)
        self.axis.set_ylabel(self.y_label)
        self.data = []

    def show(self):
        self.fig.show()

    def add_data(self, new_data):
        self.data += new_data

    def plot_line(self, hue_label, order):
        print('plotting line')
        df = pd.DataFrame(self.data)
        df = df.rename(columns={0: self.y_label, 1: self.x_label, 2: hue_label})
        sns.lineplot(data=df, x=self.x_label, y=self.y_label, ax=self.axis, hue=hue_label, hue_order=order)
        self.show()

    def plot_box(self, order):
        print('plotting box')
        df = pd.DataFrame(self.data)
        df = df.rename(columns={0: self.y_label, 1: self.x_label})
        sns.boxplot(data=df, x=self.x_label, y=self.y_label, ax=self.axis, hue=self.x_label, hue_order=order)
        self.show()
