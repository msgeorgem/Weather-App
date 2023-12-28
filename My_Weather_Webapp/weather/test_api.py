import requests

class ApiRequester:
    def __init__(self, url):
        self.url = url

    def get_data(self):
        response = requests.get(self.url)
        data = response.json()
        return data

    def print_data(self):
        data = self.get_data()
        print(data)

    def print_temp_from_data(self):
        data = self.get_data()
        data = data['list'][0]['main']['temp']
        
        print(data)

# Usage
api_requester = ApiRequester('yourapi')
api_requester.print_temp_from_data()
