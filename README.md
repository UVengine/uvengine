# Table of Contents
- [Table of Contents](#table-of-contents)
- [UVengine](#uvengine)
  - [Official website](#official-website)
  - [Description](#description)
  - [How to use it](#how-to-use-it)
  - [Using the library](#using-the-library)
    - [Requirements](#requirements)
    - [Download and install](#download-and-install)
    - [Usage](#usage)
    - [Execution](#execution)
      - [Executing the Case Studies](#executing-the-case-studies)
  - [References and third-party software](#references-and-third-party-software)

# UVengine
Universal Variability resolution engine for [UVL](https://universal-variability-language.github.io/) models and text-based artifacts with [Jinja templates](https://jinja.palletsprojects.com/en/stable/).

<p align="center">
  <img width="750" src="resources/uvengine_overview.png">
</p>


## Official website
- [UVengine](https://uvengine.github.io/)


## Description
*UVengine* is a variability resolution engine for [UVL](https://universal-variability-language.github.io/) models and text-based artifacts with [Jinja templates](https://jinja.palletsprojects.com/en/stable/).


Its main features are:
- A variability resolution engine for UVL models.
- Support all language level extensions of UVL.
- Feature traceability between UVL models and implementation artifacts.
- Language independence for any text-based artifacts using Jinja templates.
- Composition and annotation-based mechanisms to implement variability at different degrees of granularity.
- Easy integration with existing tools of the UVL ecosystem such as UVLS and flamapy.

## How to use it
The tool is currently deployed and available online in the following link so that you don't need to install any stuff: 

https://uvengine.github.io/

The main use case of the tool is uploading the files and it automatically resolves the variability.
- Inputs:
  - The feature model (.uvl).
  - A configuration of the feature model (.json).
  - The templates artifacts (.jinja)
  - A mapping model (optional) to relate the features in the feature model within the variation points in the artifacts.
- Outputs:
  - The artifacts with their variability resolved.


<video width="320" height="240" controls>
  <source src="resources/video_demo.mp4" type="video/mp4">
</video>


## Using the library
In case you want to use UVengine programatically as a library or using CLI.

### Requirements
- [Python 3.9+](https://www.python.org/)
- [Flamapy](https://www.flamapy.org/)
- [Jinja](https://jinja.palletsprojects.com/en/stable/)

### Download and install
1. Install [Python 3.9+](https://www.python.org/)
2. Clone this repository and enter into the main directory:

    `git clone https://github.com/UVengine/uvengine`

    `cd uvengine` 
3. Create a virtual environment: 
   
   `python -m venv env`

4. Activate the environment: 
   
   In Linux: `source env/bin/activate`

   In Windows: `.\env\Scripts\Activate`
   
5. Install the dependencies: 
   
   `pip install -r requirements.txt`


### Usage

The [derivation_engine.py](derivation_engine.py) script illustrate how to use UVengine programatically.

Basically:

```
# Import the UVengine 
from uvengine import UVEngine

# Instantiate the engine
uvengine = UVEngine(feature_model_path=<<path_to_your_feature_model>>,
                    configs_path=<<list_of_paths_to_your_configs_files>>,
                    templates_paths=<<list_of_paths_to_your_template_files>>,
                    mapping_model_filepath=<<path_to_your_mapping_model_files>>)
# Resolve the variability                    
resolved_templates = uvengine.resolve_variability()

# Save the resolved templates to file and print the content to the standard output
for template_path, content in resolved_templates.items():
    # Rename output file for avoiding overriding original templates and remove .jinja extension
    output_file = pathlib.Path(template_path).with_name(pathlib.Path(template_path).stem + '_resolved' + ''.join(pathlib.Path(template_path).suffixes).replace('.jinja', ''))  
    with open(output_file, 'w', encoding='utf-8') as file:
      file.write(content)
    print(content)
```

### Execution
The [derivation_engine.py](derivation_engine.py) script is also the entry point interface to resolve the variability from the given inputs.

To resolve the variability over any input, execute: 

  `python derivation_engine.py -fm FEATURE_MODEL -c CONFIGS [CONFIGS ...] -t TEMPLATES [TEMPLATES ...] [-m MAPPING_FILE]`

  where:

  `-fm FEATURE_MODEL`: Feature model in UVL (.uvl).

  `-c CONFIGS [CONFIGS ...]`: Configuration files (.json) or directy with configurations (in case of a single configuration split in multiple files).

  `-t TEMPLATES [TEMPLATES ...]`: Template files (.jinja) or directory with templates over which the variability is resolved.

  `[-m MAPPING_FILE]`: Optional file with the mapping between the features in the feature model and the variation points and variants in the templates (.csv).

Example:

  `python derivation_engine.py -fm case_studies/icecream/feature_model/icecream.uvl -c case_studies/icecream/configurations/cone.json -t case_studies/icecream/templates/main.txt.jinja -m case_studies/icecream/mapping_model/icecream.csv`

As result, the final product (i.e., the templates with the variability resolved) are generated in the same template folder provided with the suffixes `_resolved`.
    
#### Executing the Case Studies
To facilitate the execution of the different case studies, we have prepared a Python script for each case study:

- Ice cream: `python cs1_icecream.py`

- Docker: `python cs2_docker.py`


## References and third-party software
- [Flama](https://www.flamapy.org/)
- [Jinja](https://jinja.palletsprojects.com/en/stable/)
