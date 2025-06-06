from derivation_engine import main


if __name__ == '__main__':
    feature_model_path = 'evaluation/case_studies/docker/fm_models/compose_specification_full.uvl'
    configs_paths = ['evaluation/case_studies/docker/configurations/docker.uvl.json']
    templates_paths = ['evaluation/case_studies/docker/templates/compose_specification_template.yaml.jinja']
    mapping_filepath = 'evaluation/case_studies/docker/mapping_models/docker_mapping.csv'

    main(feature_model_path, configs_paths, templates_paths, mapping_filepath)
    