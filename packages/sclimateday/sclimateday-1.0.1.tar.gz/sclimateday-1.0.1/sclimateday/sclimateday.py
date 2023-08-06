import requests


class TheWeather:
    """ Creates weather object getting an apikey from https:// openweathermap.com
    and input the city or the coordinates
    
    Packages examples use :
    
    
    Get Apikey from https:// openweathermap.com
    #create object :
        
    #using coordinates
    >>> w = TheWeather(apikey="c648e2ad3499e0a62ecac46320ab692d", lat="44.34", lon="10.99" )
    
    #using city
    >>> w = TheWeather(apikey="c648e2ad3499e0a62ecac46320ab692d", city="Tegucigalpa" )
    
    #Get complete weather for the next 12 hours
    >>> w.next_12h()
    
    #simplefied data (date, temparature and sky condition) for the next 12 hours
    >>> w.next_12h_simplified():
            
    """
    
    def __init__(self, apikey, city=None, lat=None, lon=None):
 
        if city:
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}&units=meters"
            r = requests.get(url)
            self.data = r.json()
        elif lat and lon:
            url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={apikey}&units=meters"
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError("it's need the city or the lat and lot arguments") # el tipo espera argumento
        
        if self.data["cod"] != "200":
            raise ValueError(self.data["message"]) # el valor es incorrecto

    def next_12h(self):
        """Return 3 hours data form the next 12 hours
        """
        return self.data['list'][:4]
        
    
    def next_12h_simplified(self):
        """Return 3 hours date, temperature and sky condition from every 3 hours
        """
        collect_data = []
        for dicty in self.data['list'][:4]:
            collect_data.append((dicty['dt_txt'], dicty['main']['temp'], dicty['weather'][0]['description']))
        return collect_data
        #return (self.data['list'][0]['dt_txt'], self.data['list'][0]['main']['temp'], self.data['list'][0]['weather'][0]['description'])
    

