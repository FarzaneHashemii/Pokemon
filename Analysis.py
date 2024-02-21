
#Starting off my importing required libraries
from urllib.parse import urlunparse
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

    def load_data(self, url='https://pokeapi.co/api/v2/pokemon/?limit=1025') :
        ''' Retrieve data from the Pokemon API

        This function makes an HTTPS request to Pokemon API and retrieves your selected data. The data is
        stored in the Analysis object.

        Parameters
        ----------
        url

        Returns
        -------
        data

        Examples
        --------
        if __name__ == "__main__":
        pokeapi_data = load_data()
        '''
        try:
                response = requests.get(url)
                # Check if the request was successful (status code 200)
                response.raise_for_status()
                    
                    # Parse JSON response
                data = response.json()
                return data
        except requests.exceptions.HTTPError as http_err:
                # Handle HTTP errors (e.g., response code 4xx, 5xx)
                print(f'HTTP error occurred: {http_err}')
                logging.error(f'HTTP error occurred: {http_err}')
        except Exception as err:
                # Handle other possible errors (e.g., network issues)
                 print(f'An error occurred: {err}')
                 logging.error(f'An error occurred: {err}')
                                    
    def compute_analysis(self) :
        '''Analyze previously-loaded data.

        This function runs an analytical measure of your choice (mean, median, linear regression, etc...)
        and returns the data in a format of your choice.

        Parameters
        ----------
        None

        Returns
        -------
        analysis_output : Any
        
        '''
        
        data=self.load_data()

        # Flatten data
        #df_nested_list = pd.json_normalize(data, record_path =['results'])
        
            
        data=self.load_data('https://pokeapi.co/api/v2/pokemon-color/')
        print(data)
    

        # Creating a dictionary with color ID as key and color name as value
        values = [result['name'] for result in data['results']]
        keys = [1,2,3,4,5,6,7,8,9,10]
        colors = dict(zip(keys, values))
    

        self.pokemon_colors_species={}
        self.pokemon_colors_count={}
        a= 0
        b= 1025
        for k,v in colors.items() :
            data=self.load_data(urlunparse+str(k)+'/')
            self.pokemon_colors_species[v] = [species['name'] for species in data['pokemon_species']]
            self.pokemon_colors_count[v] = len([species['name'] for species in data['pokemon_species']])
            x=len([species['name'] for species in data['pokemon_species']])
            if x > a :
                most_common_color = v
                a = x
            if x < b :
                least_common_color = v
                b = x

        print(self.pokemon_colors_species)
        print(self.pokemon_colors_count)
        print(most_common_color)
        print(least_common_color)

        def notify_done(self, message: str) -> None:
                """Notify the user that analysis is complete.

                Send a notification to the user through the ntfy.sh webpush service.

                Parameters
                ----------
                message : str
                    Text of the notification to send.

                Example
                --------
                if __name__ == "__main__":
                    notify_done("Your data analysis is complete and ready to view.")
                """
                try:
                    topic = '?topic'
                    title = 'Analysis Complete'
                    message = 'Your analysis has been successfully completed.'
                
                    url = f'https://ntfy.sh/'
                    response = requests.post(url + 'YSlYtkDXpplz4OqW',
                        data=message.encode('utf-8'),
                        headers={'Title': title}
                    )
                    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
                    print("Notification sent successfully.")
                except requests.exceptions.HTTPError as http_err:
                    print(f'HTTP error occurred: {http_err}')
                except Exception as err:
                    print(f'An error occurred: {err}')

        notify_done('Analysis has been completed')
    
    def plot_data(self, save_path=None):
         ''' Analyze and plot data

         Generates a plot, display it to screen, and save it to the path in the parameter `save_path`, or 
         the path from the configuration file if not specified.

         Parameters
         ----------
         save_path : str, optional
            Save path for the generated figure

         Returns
         -------
         fig : matplotlib.Figure

         '''

         # Create a figure and a set of subplots
         fig, axs = plt.subplots(2, 1, figsize=(10, 12))

         # Bar chart
         colors = list(self.pokemon_colors_count.keys())
         counts = list(self.pokemon_colors_count.values())
         axs[0].bar(colors, counts, color=colors, edgecolor='black')  # Adding edge color for visibility

         # Adding the count above each bar
         for i, bar in enumerate(axs[0].patches):
             yval = bar.get_height()
             axs[0].text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom')

         # Adding title and labels for bar chart
         axs[0].set_title('Color Counts')
         axs[0].set_xlabel('Color')
         axs[0].set_ylabel('Count')
         axs[0].set_xticklabels(colors, rotation=45)

         # Line chart
         # Correcting the dictionary name used for sorting
         sorted_color_counts = dict(sorted(self.pokemon_colors_count.items(), key=lambda item: item[1], reverse=True))
         sorted_colors = list(sorted_color_counts.keys())
         sorted_counts = list(sorted_color_counts.values())

         # Drawing the blue line
         axs[1].plot(sorted_colors, sorted_counts, marker='o', linestyle='-', color='blue', linewidth=2)

         # Plotting each point with its specific color and outlining white for visibility
         for i, (color, count) in enumerate(zip(sorted_colors, sorted_counts)):
             axs[1].plot(i, count, marker='o', markersize=10, linestyle='', color=color, markeredgecolor='black' if color == 'white' else 'none')
             axs[1].text(i, count, str(count), ha='center', va='bottom', fontsize=12)

         # Adding title and labels for line chart
         axs[1].set_title('Color Counts Sorted High to Low')
         axs[1].set_xlabel('Color')
         axs[1].set_ylabel('Count')
         axs[1].set_xticks(range(len(sorted_colors)))
         axs[1].set_xticklabels(sorted_colors, rotation=45)

         # Adjust layout to prevent overlap
         plt.tight_layout()

         # Display the plot
         plt.show()   
