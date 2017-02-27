from datetime import datetime, timedelta

from isodate import parse_datetime, parse_duration
import requests

from solcast.base import Base


class RadiationEstimatedActuals(Base):

    end_point = 'radiation/estimated_actuals'

    def __init__(self, latitude, longitude, *args, **kwargs):

        self.latitude = latitude
        self.longitude = longitude
        self.latest = kwargs.get('latest', False)
        self.estimated_actuals = None

        self.params = {'latitude' : self.latitude, 'longitude' : self.longitude}

        if self.latest:
            self.end_point = self.end_point + '/latest'

        self._get(*args, **kwargs)

        if self.ok:
            self._generate_est_acts_dict()

    def _generate_est_acts_dict(self):

        self.estimated_actuals = []

        for est_act in self.content.get('estimated_actuals'):

            # Convert period_end and period. All other fields should already be
            # the correct type

            est_act['period_end'] =  parse_datetime(est_act['period_end'])
            est_act['period'] = parse_duration(est_act['period'])

            self.estimated_actuals.append(est_act)
