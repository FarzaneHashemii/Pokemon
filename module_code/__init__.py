
import yaml
import os
import logging

# Configure logging
# Set level to DEBUG, and assign filename to write logs to.
# Set log format: Time, line, message

logging.basicConfig(level=logging.DEBUG, filename='config.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Analysis:
    def __init__(self, analysis_config_path):
        config_paths = {
            'system_config_path': 'configs/system_config.yml',
            'user_config_path': 'configs/user_config.yml',
            'analysis_config_path': analysis_config_path
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
        print("Consolidated Configuration:")
        for key, value in self.config.items():
            print(f"{key}: {value}")

# Example usage
if __name__ == "__main__":
    analysis_obj = Analysis('configs/analysis_config.yml')
    analysis_obj.show_config()
