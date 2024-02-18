
import yaml
import logging


class Analysis:
    def __init__(self, analysis_config_path):
        # Load system-wide configuration
        with open('configs/system_config.yml', 'r') as file:
            self.system_config = yaml.safe_load(file)
        
        # Load user configuration
        with open('configs/user_config.yml', 'r') as file:
            self.user_config = yaml.safe_load(file)
        
        # Load analysis/job-specific configuration
        with open(analysis_config_path, 'r') as file:
            self.analysis_config = yaml.safe_load(file)
        
        # Consolidate configurations
        self.config = {**self.system_config, **self.user_config, **self.analysis_config}

    def show_config(self):
        print("Consolidated Configuration:")
        for key, value in self.config.items():
            print(f"{key}: {value}")

# Example usage
if __name__ == "__main__":
    analysis_obj = Analysis('configs/analysis_config.yml')
    analysis_obj.show_config()


