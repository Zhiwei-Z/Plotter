from file_util import *
from data_util import *
from misc import *
from grapher import Graph


def split_plot_line(directory,
                   plot_key,
                   separate_label,
                   required_config=None,
                   split_line_keys=None,
                   split_graph_keys=None,
                   data_filename=PROGRESS_FILE,
                   extend_limit=None,
                   smooth_width=None,
                   x_label="Steps",
                   y_label="Average Returns",
                   title=None):

    if required_config is None:
        required_config = {}
    if split_line_keys:
        split_line_keys.sort()
    else:
        split_line_keys = []
    if split_graph_keys:
        split_graph_keys.sort()
    else:
        split_graph_keys = []
    split_line_keys.sort()
    split_graph_keys.sort()
    ret = defaultdict(list)
    unique_key_values = set()
    for file, config in iterate_file_and_config(directory, data_filename, required_config=required_config):
        graph_key = create_key_name(config, split_graph_keys)
        line_key = create_key_name(config, split_line_keys)
        data = csv_to_dict_list(file, extend_limit=extend_limit, smooth_width=smooth_width, keys=[plot_key])
        if data != 'ignored':
            df_list = dict_list_to_df(dict_list=data, keys=[plot_key, STEP_CONSTANT_KEY], constant_values_appended=[line_key])
            ret[graph_key] += df_list
            unique_key_values.add(line_key)

    unique_key_values = sorted(list(unique_key_values))
    for graph_key in sorted(ret.keys()):
        df_list = ret[graph_key]
        title_name = title or graph_key
        graph = Graph(title=title_name, x_label=x_label, y_label=y_label)
        graph.add_data(df_list)
        graph.plot_line(separate_label, order=unique_key_values)


def split_plot_box(directory,
                   plot_key,
                   required_config=None,
                   split_line_keys=None,
                   split_graph_keys=None,
                   data_filename=PROGRESS_FILE,
                   extend_limit=None,
                   smooth_width=None,
                   x_label="Steps",
                   y_label="Average Returns",
                   title=None):

    if required_config is None:
        required_config = {}
    if split_line_keys:
        split_line_keys.sort()
    else:
        split_line_keys = []
    if split_graph_keys:
        split_graph_keys.sort()
    else:
        split_graph_keys = []
    split_line_keys.sort()
    split_graph_keys.sort()
    ret = defaultdict(list)
    unique_key_values = set()
    for file, config in iterate_file_and_config(directory, data_filename, required_config=required_config):
        graph_key = create_key_name(config, split_graph_keys)
        line_key = create_key_name(config, split_line_keys)
        data = csv_to_dict_list(file, extend_limit=extend_limit, smooth_width=smooth_width, keys=[plot_key])
        if data != 'ignored':
            df_list = dict_list_to_df(dict_list=data, keys=[plot_key], constant_values_appended=[line_key])
            ret[graph_key] += df_list
            unique_key_values.add(line_key)

    unique_key_values = sorted(list(unique_key_values))
    for graph_key in sorted(ret.keys()):
        df_list = ret[graph_key]
        title_name = title or graph_key
        graph = Graph(title=title_name, x_label=x_label, y_label=y_label)
        graph.add_data(df_list)
        graph.plot_box(order=unique_key_values)


if __name__ == '__main__':

    split_plot_box(directory="../data/516-test/",
                   plot_key='RL-AverageReturn',
                   split_line_keys=['mode'],
                   split_graph_keys=['envType'],
                   x_label='method')

    split_plot_line(directory="../data/516-test/",
                    plot_key='RL-AverageReturn',
                    separate_label='method',
                    split_line_keys=['mode'],
                    split_graph_keys=['envType'])
