# { "Depends": "py-genlayer:test" }
from genlayer import *

class WeatherOracle(gl.Contract):
    """
    A library-style contract for GenLayer that fetches real-time weather.
    Eliminates the need for traditional oracles by using native web access.
    """
    last_temp: float

    def __init__(self):
        self.last_temp = 0.0

    @gl.public.write
    def update_weather(self, lat: float, lon: float):
        """
        Fetches the current temperature for a specific location.
        Uses GenLayer's Equivalence Principle to reach consensus on web data.
        """
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=True"

        # This block is 'non-deterministic' (data changes). 
        # Validators will run this and agree on the result.
        def fetch_weather():
            data = gl.get_webpage(api_url, mode='json')
            return float(data['current_weather']['temperature'])

        # We use strict_eq because temperature is a specific numerical value.
        self.last_temp = gl.eq_principle_strict_eq(fetch_weather)
        return self.last_temp

    @gl.public.view
    def get_stored_temp(self) -> float:
        return self.last_temp
