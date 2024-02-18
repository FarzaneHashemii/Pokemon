
import requests
from pprint import pprint


#def load_data()
''' Retrieve data from the Pokemon API

This function makes an HTTPS request to the Pokemon API and retrieves your selected 
data. The data is stored in the Analysis object.'''


response = requests.get(url='https://pokeapi.co/api/v2/')
                        
# print raw response
print(response.status_code)
print(response.text)

# parse json
response_json = response.json()
pprint(response_json)

# print some values
#print('Username: ' + response_json['login'])
#print('Name: ' + response_json['name'])

#topic = 'dsi_c2_brs'
#title = 'Hello, world!'
#message = 'Hello, world from Simeon!'

# send a message through ntfy.sh
#equests.post(
 #   'https://ntfy.sh/' + topic,
  #  data=message.encode('utf-8'),
   # headers={'Title': title}
#)

