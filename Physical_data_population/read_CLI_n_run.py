
"""
Sometime we use use a .py file as module.
However sometime we use a .py file as script.

While running the file as a script, there is no meaning of calculating root of the module path.
While calling the file as module, then need to identify the root of the module.

Argument:
    There are two types of arguments:
        Positional parameter 
        Optional parameter

parser.add_argument("square", type=int, help="display a square of a given number")
parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
args = parser.parse_args()
         
"""
import argparse
from Physical_data_population.read_configuration import *
from Physical_data_population.physical_data_population import *


def run_physical_data_population(config_path_p):
    config_path = config_path_p
    configuration_ob = read_configuration(config_path)

    sd_path = configuration_ob["sd_path"]
    planning_file = configuration_ob["planning_file"]
    out_put_data_dict_dir = configuration_ob["out_put_data_dict_dir"]
    profile_root_path = configuration_ob["profile_root_path"]
    input_type = configuration_ob["input_type"]
    input_delimiter = configuration_ob["input_delimiter"]

    data_processor = DataProcessor(input_type, input_delimiter)
    out_put_data_dict = data_processor.update_sd_by_planner_step1(planning_file, sd_path, profile_root_path_p=profile_root_path)
    # print(type(out_put_data_dict))
    # print(out_put_data_dict)
    data_writer(out_put_data_dict, out_put_data_dict_dir)


def main_method():
    parser = argparse.ArgumentParser()
    parser.add_argument("config_path", help="Please provide the path of the configuration file")
    args = parser.parse_args()
    config_path = args.config_path
    run_physical_data_population(config_path)


if __name__ == "__main__":

    main_method()
