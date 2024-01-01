import json
from weather.models import Lang, City


class DataLoader:
    def __init__(self, json_file):
        self.json_file = json_file

    def load_data(self):
        n=0
        with open(self.json_file, 'r',encoding='utf-8', errors='ignore') as file:
            data = json.load(file)
            for item in data:
                
                n=n+1
                print(n, item['name'])
                location = City.objects.create(
                    id=item['id'],
                    lon=item['coord']['lon'],
                    lat=item['coord']['lat'],
                    country=item['country'],
                    cl=item['geoname']['cl'],
                    code=item['geoname']['code'],
                    parent=item['geoname']['parent'],
                    name=item['name'],
                    level=item['stat']['level'],
                    population=item['stat']['population'],
                    # zoom=item['zoom'],
                )
                if 'langs' in item:    
                    for lang in item['langs']:
                        language = Lang.objects.create(lang=list(lang.values())[0])
                        location.langs.add(language)
                # for station in item['stations']:
                #     station_obj = Station.objects.create(
                #         ids=station['id'],
                #         dist=station['dist'],
                #         kf=station['kf']
                #     )
                #     location.stations.add(station_obj)

