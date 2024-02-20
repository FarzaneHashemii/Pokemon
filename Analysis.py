
import yaml
import logging
import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
import os

#Starting off my importing required libraries

# Configure logging
# Set level to DEBUG, and assign filename to write logs to.
# Set log format: Time, level, line, message

logging.basicConfig(level=logging.DEBUG, filename='config.log',
                    format='%(asctime)s - %(levelname)s - %(lineno)s - %(message)s')

class Analysis:
    def __init__(self, analysis_config):
        ''' Load configurations into an Analysis object

        Load system-wide configuration from `configs/system_config.yml`, user configuration from
        configs/user_config.yml`, and the specified analysis configuration file

        Parameters
        ----------
        analysis_config : str
            Path to the analysis/job-specific configuration file

        Returns
        -------
        analysis_obj : Analysis
            Analysis object containing consolidated parameters from the configuration files

            
        Notes
        -----
        The configuration files should include parameters for:
            * ntfy.sh topic
            * Plot color
            * Plot title
            * Plot x and y axis titles
            * Figure size
            * Default save path

        Examples
        --------
        if __name__ == "__main__":
            analysis_obj = Analysis('configs/analysis_config.yml')
        '''
        config_paths = {
            'system_config_path': 'configs/system_config.yml',
            'user_config_path': 'configs/user_config.yml',
            'analysis_config_path': analysis_config
        }

        self.config = {}
        for config_name, config_path in config_paths.items():
            try:
                assert os.path.exists(config_path), f"{config_path} does not exist."
                with open(config_path, 'r') as file:
                    config_data = yaml.safe_load(file)
                    assert config_data is not None, f"{config_path} is empty or incorrectly formatted."
                    self.config = {**self.config, **config_data}
            except AssertionError as error:
                logging.error(f"Assertion Error: {error}")
                raise
            except Exception as e:
                logging.error(f"Failed to load {config_name}: {e}")
                raise

    def show_config(self):
        '''Show configurations loaded

        Shows the configurations loaded from `configs/system_config.yml`, user configuration from
        configs/user_config.yml`, and the specified analysis configuration file.
        
        Parameters
        -----------
        None

        Returns
        --------
        Prints configurations in key value pairs

        Examples
        ---------
        if __name__ == "__main__":
            analysis_obj.show_config()
        '''
        if not isinstance(self.config, dict):
            logging.info("self.config is not a dictionary")
            raise TypeError("Expected self.config to be a dictionary")  
    
        print("Consolidated Configuration:")
        for key, value in self.config.items():
            print(f"{key}: {value}")


