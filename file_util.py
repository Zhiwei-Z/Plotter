import shutil
import os
import json
import csv
from collections import defaultdict, OrderedDict
from data_util import *



cp = shutil.copyfile
cp_r = shutil.copytree
join = os.path.join
mv = shutil.move

STEP_CONSTANT_KEY = '#STEP_KEY'
PROGRESS_FILE = "progress.csv"
RL_PROGRESS_FILE = "RL_Progress.csv"
PARAMS_FILE = "params.json"
PRETRAIN_POLICY = "pretrain_params.pkl"


def load_json(filename):
    with open(filename, "r+") as f:
        ret = json.load(f)
        f.close()
        return ret


def dump_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)
        f.close()


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
                        print("Float conversion of ", row[k], " failed.")

        if extend_limit is not None:
            for k in return_dict:
                length = len(return_dict[k])
                assert length <= extend_limit
                return_dict[k] += [return_dict[k][-1]] * (extend_limit - length)

        if smooth_width is not None:
            for k in return_dict:
                return_dict[k] = smooth_data(return_dict[k], width=smooth_width)
        if len(list(return_dict.values())) > 0:
            data_length = len(list(return_dict.values())[0])
            return_dict[STEP_CONSTANT_KEY] = list(range(data_length))
        else:
            return 'ignored'
    return OrderedDict(return_dict.items())


def iterate_file_and_config(directory, filename, required_config=None):
    for root, _, files in os.walk(directory):
        if PARAMS_FILE in files and filename in files:
            config = load_json(join(root, PARAMS_FILE))
            if (required_config is None) or params_match(config, required_config):
                yield join(root, filename), config


