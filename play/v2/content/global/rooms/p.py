import os
import requests

# URL to fetch the JSON data
json_url = 'https://media.cpps.to/play/v2/client/rooms.json'

# Base URL for downloading SWF files
base_download_url = 'https://media.cpps.to/play/v2/content/global/rooms/'

# Directory to save the downloaded files
download_directory = 'D:\\pcvm'

# Ensure the download directory exists
os.makedirs(download_directory, exist_ok=True)

try:
    # Fetch the JSON data
    response = requests.get(json_url)
    response.raise_for_status()
    rooms = response.json()
except requests.RequestException as e:
    print(f'Failed to fetch JSON data: {e}')
    rooms = {}

# Check if the data is a dictionary
if isinstance(rooms, dict):
    for room_id, room_info in rooms.items():
        # Ensure each value is a dictionary with a 'path' key
        if isinstance(room_info, dict) and 'path' in room_info:
            room_name = room_info.get('name', 'unknown')
            swf_filename = room_info['path']
            swf_url = f'{base_download_url}{swf_filename}'
            swf_path = os.path.join(download_directory, swf_filename)
            try:
                # Download the SWF file
                swf_response = requests.get(swf_url)
                if swf_response.status_code == 200:
                    with open(swf_path, 'wb') as swf_file:
                        swf_file.write(swf_response.content)
                    print(f'Successfully downloaded {swf_filename} ({room_name})')
                else:
                    print(f'Failed to download {swf_filename} ({room_name}); HTTP status code: {swf_response.status_code}')
            except requests.RequestException as e:
                print(f'Error downloading {swf_filename} ({room_name}): {e}')
        else:
            print(f'Unexpected data format for room ID {room_id}: {room_info}')
else:
    print('Unexpected data format: JSON data should be a dictionary.')
