from derivation_engine import main


if __name__ == '__main__':
    feature_model_path = 'case_studies/icecream/feature_model/icecream.uvl'
    configs_paths = ['case_studies/icecream/configurations/cone.json']
    templates_paths = ['case_studies/icecream/templates/main.txt.jinja']
    mapping_filepath = 'case_studies/icecream/mapping_model/icecream.csv'

    main(feature_model_path, configs_paths, templates_paths, mapping_filepath)