import json
from typing import Any

import jinja2
from flamapy.core.discover import DiscoverMetamodels


# Icecream example
template_dir = 'examples/icecream/templates'
template_file = 'icecream_template.txt.jinja'
fm_filepath = 'examples/icecream/fm_models/icecream_fm.uvl'
config_filepath = 'examples/icecream/configurations/icecream_fm_cone.uvl.json'

# jMetal example
template_dir = 'examples/jmetal/templates'
template_file = 'AppExample.java.jinja'
fm_filepath = 'examples/jmetal/fm_models/jMetal.uvl'
config_filepath = 'examples/jmetal/configurations/jMetal.uvl.json'


class Configuration:

    def __init__(self, elements: dict[str, Any] = {}) -> None:
        self.elements = elements

    def is_selected(self, element: str) -> bool:
        return element in self.elements and self.elements[element]
    
    def get_value(self, element: str) -> Any:
        return self.elements[element]


def load_configuration_from_file(filepath: str) -> Configuration:
    with open(filepath) as file:
        json_dict = json.load(file)
    config = json_dict['config']
    return Configuration(config)


def main() -> None:
    
    # Initialization of Flamapy
    dm = DiscoverMetamodels()

    # Initialization of Jinja
    template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
    environment = jinja2.Environment(loader=template_loader, trim_blocks=True, lstrip_blocks=True)

    # Step 1. Load the FM
    fm = dm.use_transformation_t2m(fm_filepath, 'fm')

    # Step 2. Load a configuration of the FM
    config = load_configuration_from_file(config_filepath)
    
    # Step 2 (alternative). Generate a random configuration

    # Step 3 (opcional). Load the mapping model

    # Step 4. Load the templates
    template = environment.get_template(template_file)

    # Step 5. Generate the product from the configuration
    content = template.render(config.elements)
    print(content)
    # Save the product
    with open('product.txt', 'w', encoding='utf-8') as file:
        file.write(content)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='UVengine: Variability resolution engine for UVL with Jinja templates.')
    # parser.add_argument('-fm', '--feature_model', dest='feature_model', type=str, required=False, 
    #                     help='Feature model in UVL (.uvl).')
    # parser.add_argument('-c', '--configs', dest='configs_dir', type=str, required=True, 
    #                     help='Directory with the configurations files (.json).')
    # parser.add_argument('-t', '--templates', dest='templates_dir', type=str, required=True, 
    #                     help='Template directory with templates files (.jinja) over which the variability is resolved.')
    # parser.add_argument('-m', '--mapping', dest='mapping_file', type=str, required=False, 
    #                     help='File with the mapping between the variation points and the templates (.csv).')
    # args = parser.parse_args()

    # # Get parameters
    # feature_model = args.feature_model
    # configurations_files = utils.get_filepaths(args.configs_dir, ['.json'])
    # templates_dir = utils.get_filepaths(args.templates_dir, ['.jinja'])
    # mapping_file = args.mapping_file

    main()    

