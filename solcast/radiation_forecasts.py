from datetime import datetime, timedelta

from isodate import parse_datetime, parse_duration
import requests

from solcast.base import Base


class RadiationForecasts(Base):

    end_point = 'radiation/forecasts'

    def __init__(self, latitude, longitude, *args, **kwargs):

        self.latitude = latitude
        self.longitude = longitude
        self.forecasts = None

        self.params = {'latitude' : self.latitude,
                       'longitude' : self.longitude}

        self._get(*args, **kwargs)

        if self.ok:
            self._generate_forecasts_dict()

    def _generate_forecasts_dict(self):

        self.forecasts = []

        for forecast in self.content.get('forecasts'):

            # Convert period_end and period. All other fields should already be
            # the correct type
            forecast['period_end'] = parse_datetime(forecast['period_end'])
            forecast['period'] = parse_duration(forecast['period'])

            self.forecasts.append(forecast)
