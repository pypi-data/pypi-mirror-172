import pprint
import requests

class the_geographer:
    """
    description about our class
    """
    APIkey = "248bc0b69805d8c3b73821c846bb7b0b"

    def __init__(self, cityname=None, lat=None, lon=None):
        self.cityname = cityname
        self.lat = lat
        self.lon = lon

    def bringer(self):
        """
        description about our method
        """

        if ((self.lon == None or self.lat == None) and self.cityname == None):
            raise TypeError("you didnt enter lat, lon or city")

        thelink = f"https://api.openweathermap.org/data/2.5/forecast?lat={self.lat}&lon={self.lon}&appid={self.APIkey}"
        thelink2 = f"https://api.openweathermap.org/data/2.5/forecast?q={self.cityname}&appid={self.APIkey}"

        r = requests.get(thelink)
        the_data = r.json()

        r2 = requests.get(thelink2)
        the_data2 = r2.json()

        if the_data["cod"] != 200 or the_data2["cod"] != 200:
            raise ValueError(the_data2["message"])

        if self.cityname:

            if the_data2["cod"] != 200:
                raise ValueError(the_data2["message"])

            for dicty in the_data2['list'][:4]:
                print(dicty['dt_txt'], dicty['weather'][0]['description'])


        elif self.lat and self.lon:

            if the_data["cod"] != 200:
                raise ValueError(the_data["message"])

            for dicty in the_data['list'][:4]:
                print(dicty['dt_txt'], dicty['weather'][0]['description'])

            return the_data['list'][:4]

        # else:
        #     raise TypeError("you didnt enter lat, lon or city")


# the_ins = the_geographer(cityname="ridze").bringer()
# pprint.pprint(the_ins)
