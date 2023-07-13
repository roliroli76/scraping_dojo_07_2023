import os
import re
import json
import requests
from dotenv import load_dotenv


# Load parameters from .env file
load_dotenv()


class Scraper:
    def __init__(self, proxy, url, output_file):
        self.proxy = proxy
        self.url = url
        self.output = output_file

    def scrape_website(self):
        proxies = {'http': 'http://' + self.proxy, 'https': 'https://' + self.proxy}

        try:
            response = requests.get(self.url, proxies=proxies)
            response.raise_for_status()
            html = response.text

            # Search for the script section containing JSON data using a regular expression
            pattern = r'var data = (\[.*?\]);'
            match = re.search(pattern, html, re.DOTALL)
            if match:
                json_data = match.group(1)

                # Process the JSON data
                try:
                    data = json.loads(json_data)

                    # Create a new list three tags for each entry
                    modified_data = []
                    for item in data:
                        modified_item = {
                            'text': item.get('text'),
                            'author': item.get('author', {}).get('name'),
                            'tags': item.get('tags', [])[:3]
                        }
                        modified_data.append(modified_item)

                    # Save the data to a JSON file
                    with open(self.output, 'w') as file:
                        json.dump(modified_data, file, indent=4)

                except json.JSONDecodeError as e:
                    print('Błąd dekodowania JSON:', e)
                    return

            else:
                print('Nie znaleziono danych JSON.')
        except requests.exceptions.RequestException as e:
            print('Błąd pobierania strony:', e)


if __name__ == '__main__':
    proxy = os.environ.get('PROXY')
    url = os.environ.get('INPUT_URL')
    output_file = os.environ.get('OUTPUT_FILE')

    scraper = Scraper(proxy, url, output_file)
    scraper.scrape_website()
