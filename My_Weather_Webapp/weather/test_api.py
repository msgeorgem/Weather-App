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
api_requester = ApiRequester('http://api.openweathermap.org/data/2.5/forecast?id=3081368&appid=cb871da155cb0de83225c7bfa2dcf06f')
api_requester.print_temp_from_data()
