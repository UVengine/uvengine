import os
import argparse
import csv
from typing import Any

import jinja2

from spl_implementation.utils import utils
from spl_implementation.models import VEngine

# CONSTANTS


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Variability resolution with Jinja templates.')
    # parser.add_argument('-c', '--configs', dest='configs_dir', type=str, required=True, 
    #                     help='Directory with the configurations files (.json).')
    # parser.add_argument('-t', '--template', dest='template_file', type=str, required=True, 
    #                     help='Template file (.jinja) over which the variability is resolved.')
    # parser.add_argument('-m', '--mapping', dest='mapping_file', type=str, required=True, 
    #                     help='File with the mapping between the variation points and the templates (.csv).')
    # args = parser.parse_args()

    # # Get parameters
    # configurations_files = utils.get_filepaths(args.configs_dir, ['.json'])
    # template_file = args.template_file
    # mapping_file = args.mapping_file

    # print('CONFIGURATION FILES:')
    # for i, config_file in enumerate(configurations_files, 1):
    #     print(f'|-{i}: {config_file}')
    # if not configurations_files:
    #     print('|-Warning: No configurations files detected. Use a folder with .json files.')
    
    # print('TEMPLATE FILES:')
    # if template_file.endswith('.jinja'):
    #     print(f'|-{template_file}')
    # else:
    #     print('|-Error: Wrong template file extension. Use a .jinja file.')

    # print('MAPPING MODEL:')
    # if mapping_file.endswith('.csv'):
    #     print(f'|-{mapping_file}')
    # else:
    #     print('|-Error: Wrong mapping model file extension. Use a .csv file.')

    vengine = VEngine()
    vengine.load_configuration('evaluation/case_studies/icecream/icecream_fm.uvl.json')
    raise Exception
    ##############
    # Load the feature models
    fms = load_feature_models()

    # Parse configurations and attributes
    configurations = [parse_configuration(file, fms) for file in configurations_files]
    attributes = [parse_attributes(file) for file in attributes_files]

    # Load the mapping model
    mapping_model = load_mapping_model('mapping_models/pgfplots_map.csv', fms)
    print(f'MAPPING MODEL:')
    for i, vp in enumerate(mapping_model.values()):
        print(f'|-vp{i}: {vp}')

    maps = build_template_maps(fms, mapping_model, configurations, attributes)
    print(f'TEMPLATE CONFIGURATION:')
    for h, v in maps.items():
        if isinstance(v, list):
            for i, multi_map in enumerate(v):
                print(f'|-plot{i}: {multi_map}')
        else:
            print(f'|-{h}: {v}')

    template_loader = jinja2.FileSystemLoader(searchpath="./")
    environment = jinja2.Environment(loader=template_loader)
    template = environment.get_template('templates/template.tex')
    content = template.render(maps)

    with open('visualization.tex', 'w', encoding='utf-8') as file:
        file.write(content)

    #print(f'MAPPING MODEL: {mapping_model}')
    #print(f'CONFIGURATIONS: {configurations}')
    #print(f'ATTRIBUTES: {attributes}')
    