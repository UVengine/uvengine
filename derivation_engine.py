from uvengine import UVEngine


# jMetal example
template_dir = 'resources/jmetal/templates'
template_file = 'AppExample.java.jinja'
template_filepath = 'resources/jmetal/templates/AppExample.java.jinja'
fm_filepath = 'resources/jmetal/fm_models/jMetal.uvl'
config_filepath = 'resources/jmetal/configurations/jMetal.uvl.json'
mapping_filepath = 'resources/jmetal/mapping_models/jMetal_mapping.csv'


def main() -> None:
    uvengine = UVEngine(fm_model_filepath=fm_filepath,
                        template_filepath=template_filepath,
                        config_filepath=config_filepath,
                        mapping_filepath=mapping_filepath)
    content = uvengine.resolve_variability()
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

