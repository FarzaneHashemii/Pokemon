
import requests
from pprint import pprint


def load_data() :
    ''' Retrieve data from the Pokemon API

    This function makes an HTTPS request to the Pokemon API and retrieves your selected 
    data. The data is stored in the Analysis object.'''

    url = 'https://pokeapi.co/api/v2/'
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


def compute_analysis()
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
#most & least common Pokemon
print('Pokemon: ' + pokeapi_data['pokemon'])
data=load_data(pokeapi_data['pokemon'])
print(data['results'])
