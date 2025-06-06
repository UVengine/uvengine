from derivation_engine import main


if __name__ == '__main__':
    feature_model_path = 'evaluation/case_studies/icecream/fm_models/icecream_fm.uvl'
    configs_paths = ['evaluation/case_studies/icecream/configurations/icecream_fm_cone.uvl.json']
    templates_paths = ['evaluation/case_studies/icecream/templates/icecream_template.txt.jinja']
    mapping_filepath = 'evaluation/case_studies/icecream/mapping_models/icecream_mapping.csv'

    main(feature_model_path, configs_paths, templates_paths, mapping_filepath)