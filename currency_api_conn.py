import requests
from config import Config


class CurrencyAPI:
    API_URL = Config.EXCHANGE_RATE_API_URL
    API_KEY = Config.API_KEY

    def get(self, endpoint, *args, **kwargs):
        headers = {
            'apikey': self.API_KEY
        }

        response = requests.get(url=self.API_URL + endpoint, headers=headers, params=kwargs)
        if response.status_code == 200:
            return response
        else:
            return None

    def live(self, source='USD', *currencies):
        endpoint = 'live'
        currencies = ','.join(currencies)
        return self.get(endpoint, source=source, currencies=currencies).json()

    def list(self):
        endpoint = 'list'
        return self.get(endpoint).json()

    def convert(self):
        pass

    def historical(self):
        pass

    def timeframe(self):
        pass

    def change(self):
        pass


# print(CurrencyAPI().live())
print(CurrencyAPI().list())
