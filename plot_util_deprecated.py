import os
import shutil
import json
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from collections import defaultdict

sns.set(font_scale=1.2)

cp = shutil.copyfile
cp_r = shutil.copytree
join = os.path.join
mv = shutil.move

PROGRESS_FILE = "progress.csv"
RL_PROGRESS_FILE = "RL_Progress.csv"
PARAMS_FILE = "params.json"
PRETRAIN_POLICY = "pretrain_params.pkl"


def create_name(keys, values):
    return ", ".join(["{}={}".format(str(k), str(v)) for k, v in zip(keys, values)])


def load_json(filename):
    with open(filename, "r+") as f:
        ret = json.load(f)
        f.close()
        return ret


def dump_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)
        f.close()


def smooth_data(l, width):
    length = len(l)
    target = [np.mean(l[max(0, i - width): min(i + width + 1, length)]) for i in range(length)]
    return target


def params_match(big, small):
    for k in small:
        if big[k] != small[k]:
            return False
    return True


def get_array_df(data):
    return [(i, d) for i, d in enumerate(data)]


def dict_to_kv_lists(d):
    sorted_keys = sorted(d.keys())
    return list(sorted_keys), [d[k] for k in sorted_keys]


def csv_to_dict_list(file_path, extend_limit=None, smooth_width=None, keys=None):
    """
    Return a dictionary of lists
    """
    return_dict = defaultdict(list)
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            for k in row.keys():
                if (keys is None) or (k in keys):
                    try:
                        return_dict[k].append(float(row[k]))
                    except:
                        pass

        if extend_limit is not None:
            for k in return_dict:
                length = len(return_dict[k])
                assert length <= extend_limit
                return_dict[k] += [return_dict[k][-1]] * (extend_limit - length)

        if smooth_width is not None:
            for k in return_dict:
                return_dict[k] = smooth_data(return_dict[k], width=smooth_width)
    return return_dict


def plot_single_df(data, label, color, line_style, axis, x_label, y_label):
    if color is None:
        sns.lineplot(data=data, x=x_label, y=y_label, ax=axis, label=label)
    else:
        sns.lineplot(data=data, x=x_label, y=y_label, ax=axis, label=label, c=color)
    axis.lines[-1].set_linestyle(line_style)


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

class LineGraph(Graph):

    def add_line_plot(self, data, label, color=None, line_style='-'):
        df = pd.DataFrame(data)
        df = df.rename(columns={0: self.x_label, 1: self.y_label})
        if color is None:
            sns.lineplot(data=df, x=self.x_label, y=self.y_label, ax=self.axis, label=label, style=line_style)
        else:
            sns.lineplot(data=df, x=self.x_label, y=self.y_label, ax=self.axis, label=label, c=color, style=line_style)

class BoxGraph(Graph):
    def add_box_data(self, data):
        self.data += data

    def plot_box(self):
        df = pd.DataFrame(self.data)
        df = df.rename(columns={0: self.x_label, 1: self.y_label})
        sns.boxplot(data=df, x=self.x_label, y=self.y_label, ax=self.axis)



# def split_plot(directory,
#                plot_key,
#                required_config=None,
#                split_line_keys=None,
#                split_graph_keys=None,
#                colors=None,
#                data_filename=PROGRESS_FILE,
#                extend_limit=None,
#                smooth_width=None,
#                x_label="Steps",
#                y_label="Average Returns",
#                title=None):
#     if required_config is None:
#         required_config = {}
#     if split_line_keys:
#         split_line_keys.sort()
#     else:
#         split_line_keys = []
#     if split_graph_keys:
#         split_graph_keys.sort()
#     else:
#         split_graph_keys = []
#     split_line_keys.sort()
#     split_graph_keys.sort()
#     ret = {}
#     for file, config in iterate_file_and_config(directory, data_filename, required_config=required_config):
#         data = csv_to_dict_list(file, extend_limit=extend_limit, smooth_width=smooth_width, keys=[plot_key])[plot_key]
#         df_list = get_array_df(data)
#
#         graph_key, line_key = [], []
#         for k in split_graph_keys:
#             graph_key.append(config[k])
#         for k in split_line_keys:
#             line_key.append(config[k])
#         graph_key, line_key = tuple(graph_key), tuple(line_key)
#
#         if graph_key not in ret:
#             ret[graph_key] = {}
#         if line_key not in ret[graph_key]:
#             ret[graph_key][line_key] = []
#         ret[graph_key][line_key] += df_list
#
#     for graph_key in sorted(ret.keys()):
#         d = ret[graph_key]
#         title_name = title or create_name(split_graph_keys, graph_key)
#         line_keys, line_values = dict_to_kv_lists(d)
#         labels = [create_name(split_line_keys, k) for k in line_keys]
#         if colors is not None:
#             assert type(colors) == list
#             assert len(line_values) == len(colors), "Number of unique lines and number of colors don't match"
#             plot_df(datas=line_values, labels=labels, title=title_name, line_styles='-', x_label=x_label,
#                     y_label=y_label, colors=colors)
#         else:
#             plot_df(datas=line_values, labels=labels, title=title_name, line_styles='-', x_label=x_label,
#                     y_label=y_label)


def plot_df(datas, title, labels, colors=None, line_styles='-', x_label='Steps', y_label='Returns'):
    fig, (axis) = plt.subplots(1, 1, figsize=(20 / 3., 5))
    axis.set_title(title)
    if colors is None:
        colors = [None for _ in datas]
    if type(line_styles) != list:
        line_styles = [line_styles for _ in datas]
    for d, l, c, l_style in zip(datas, labels, colors, line_styles):
        df = pd.DataFrame(d)
        df = df.rename(columns={0: x_label, 1: y_label})
        plot_single_df(df, l, c, l_style, axis, x_label, y_label)
    plt.show()


def iterate_file_and_config(directory, filename, required_config=None):
    for root, _, files in os.walk(directory):
        if PARAMS_FILE in files and filename in files:
            config = load_json(join(root, PARAMS_FILE))
            if (required_config is None) or params_match(config, required_config):
                yield join(root, filename), config


def get_df(dictionary, key, constant_value_appended):
    all_arrays = [dictionary[key]] + [[constant_value_appended for _ in dictionary[key]]]
    return list(zip(*all_arrays))


# def split_plot_box(directory,
#                plot_key,
#                required_config=None,
#                split_line_keys=None,
#                split_graph_keys=None,
#                colors=None,
#                data_filename=PROGRESS_FILE,
#                extend_limit=None,
#                smooth_width=None,
#                x_label="Steps",
#                y_label="Average Returns",
#                title=None):
#     if required_config is None:
#         required_config = {}
#     if split_line_keys:
#         split_line_keys.sort()
#     else:
#         split_line_keys = []
#     if split_graph_keys:
#         split_graph_keys.sort()
#     else:
#         split_graph_keys = []
#     split_line_keys.sort()
#     split_graph_keys.sort()
#     ret = {}
#     for file, config in iterate_file_and_config(directory, data_filename, required_config=required_config):
#         data = csv_to_dict_list(file, extend_limit=extend_limit, smooth_width=smooth_width, keys=[plot_key])[plot_key]
#         df_list = get_array_df(data)
#
#         graph_key, line_key = [], []
#         for k in split_graph_keys:
#             graph_key.append(config[k])
#         for k in split_line_keys:
#             line_key.append(config[k])
#         graph_key, line_key = tuple(graph_key), tuple(line_key)
#
#         if graph_key not in ret:
#             ret[graph_key] = {}
#         if line_key not in ret[graph_key]:
#             ret[graph_key][line_key] = []
#         ret[graph_key][line_key] += df_list
#
#     for graph_key in sorted(ret.keys()):
#         d = ret[graph_key]
#         title_name = title or create_name(split_graph_keys, graph_key)
#         line_keys, line_values = dict_to_kv_lists(d)
#         labels = [create_name(split_line_keys, k) for k in line_keys]
#         if colors is not None:
#             assert type(colors) == list
#             assert len(line_values) == len(colors), "Number of unique lines and number of colors don't match"
#             plot_df(datas=line_values, labels=labels, title=title_name, line_styles='-', x_label=x_label,
#                     y_label=y_label, colors=colors)
#         else:
#             plot_df(datas=line_values, labels=labels, title=title_name, line_styles='-', x_label=x_label,
#                     y_label=y_label)
