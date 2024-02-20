
import requests
import logging
from pprint import pprint
import pandas as pd
import json
import matplotlib.pyplot as plt

def load_data() :
    ''' Retrieve data from the Pokemon API

    This function makes an HTTPS request to the Pokemon API and retrieves your selected 
    data. The data is stored in the Analysis object.'''

    url = 'https://pokeapi.co/api/v2/pokemon/?limit=1025'
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
    except Exception as err:
            # Handle other possible errors (e.g., network issues)
            print(f'An error occurred: {err}')
                            
    # print raw response
    print(response.status_code)
    print(response.text)

    # parse json
    Analysis = response.json()

# Example usage
if __name__ == "__main__":
    pokeapi_data = load_data()
    if pokeapi_data:
        print(pokeapi_data)
    else:
        print('Failed to retrieve data from PokeAPI.')

# print some values
#print('Username: ' + response_json['login'])
#print('Name: ' + response_json['name'])

def notify_done(message: str) -> None:
    """Notify the user that analysis is complete.

    Send a notification to the user through the ntfy.sh webpush service.

    Parameters
    ----------
    message : str
        Text of the notification to send.
    """
    try:
        topic = '?topic'
        title = 'Analysis Complete'
        message = 'Your analysis has been successfully completed.'
    
        url = f'https://ntfy.sh/'
        response = requests.post(url + topic,
            data=message.encode('utf-8'),
            headers={'Title': title}
        )
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        print("Notification sent successfully.")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'An error occurred: {err}')

# Example usage
if __name__ == "__main__":
    notify_done("Your data analysis is complete and ready to view.")



data=load_data(url)
print(data)


# Flatten data
df_nested_list = pd.json_normalize(data, record_path =['results'])
print(df_nested_list)
      
url = 'https://pokeapi.co/api/v2/pokemon-color/'
data=load_data(url)
print(data)

# Creating a dictionary with color ID as key and color name as value
values = [result['name'] for result in data['results']]
keys = [1,2,3,4,5,6,7,8,9,10]
colors = dict(zip(keys, values))
print(colors)

pokemon_colors_species={}
pokemon_colors_count={}
a= 0
b= 1025
for k,v in colors.items() :
    data=load_data(url+str(k)+'/')
    pokemon_colors_species[v] = [species['name'] for species in data['pokemon_species']]
    pokemon_colors_count[v] = len([species['name'] for species in data['pokemon_species']])
    x=len([species['name'] for species in data['pokemon_species']])
    if x > a :
        most_common_color = v
        a = x
    if x < b :
        least_common_color = v
        b = x

print(pokemon_colors_species)
print(pokemon_colors_count)
print(most_common_color)
print(least_common_color)



# Create a figure and a set of subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 12))

# Bar chart
colors = list(pokemon_colors_count.keys())
counts = list(pokemon_colors_count.values())
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
sorted_color_counts = dict(sorted(pokemon_colors_count.items(), key=lambda item: item[1], reverse=True))
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

def compute_analysis() :

    #pokemon_names = ()
    #n=data['count']
    #print(n)

