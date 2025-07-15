from derivation_engine import main


if __name__ == '__main__':
    feature_model_path = 'case_studies/docker/feature_model/docker.uvl'
    configs_paths = ['case_studies/docker/configurations/docker.uvl.json']
    templates_paths = ['case_studies/docker/templates/main.yaml.jinja']
    mapping_filepath = 'case_studies/docker/mapping_model/docker.csv'

    main(feature_model_path, configs_paths, templates_paths, mapping_filepath)
    