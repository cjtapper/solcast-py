import logging
import time

# Package name has changed between Python 2.7 and 3
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import requests

from solcast import api_key

_BASE_URL = 'https://api.solcast.com.au/'

class Base(object):

    throttled = False
    throttle_release = None

    def _get(self, api_key=api_key, **kwargs):

        if api_key == None:
            raise TypeError('{type}() missing 1 required argument: \'api_key\''\
                            .format(type=type(self)))

        logger = logging.getLogger()

        self.url = urljoin(_BASE_URL, self.end_point)
        self.status_code = 'Unknown'
        self.content = None
        self.api_key = api_key
        self.rate_limited = kwargs.get('rate_limited', True)
        self.throttle_release_padding = kwargs.get('throttle_release_padding', 2)

        params = self.params.copy()
        params['format'] = 'json'

        now = time.time()

        if self.rate_limited and Base.throttled and now < Base.throttle_release:
            sleep_time = int(Base.throttle_release - now +
                             self.throttle_release_padding)
            logger.info('Solcast API rate limit reached. Waiting {seconds} seconds'.\
                        format(seconds=sleep_time))

            time.sleep(sleep_time)
            Base.throttled = False

        try:

            r = requests.get(self.url, auth=(self.api_key, ''), params=params)

            if self.rate_limited and r.status_code == 429:
                now = time.time()
                Base.throttle_release = r.headers.get('X-Rate-Limit-Reset')

                if Base.throttle_release:
                    Base.throttle_release = float(Base.throttle_release)

                sleep_time = int(Base.throttle_release - now + self.throttle_release_padding)
                logger.info('HTTP status 429: Solcast API rate limit reached. Waiting {seconds} seconds'.\
                            format(seconds=sleep_time))

                time.sleep(sleep_time)
                Base.throttled = False


            self.status_code = r.status_code
            self.url = r.url
            self.headers = r.headers

            if self.rate_limited:
                Base.throttle_release = self.headers.get('X-Rate-Limit-Reset')

                if Base.throttle_release:
                    Base.throttle_release = float(Base.throttle_release)

                if self.headers.get('X-Rate-Limit-Remaining') == '0':
                    Base.throttled = True

        except (KeyboardInterrupt, SystemExit):
            raise

        # Attempt to open json from Request connection
        try:
            self.content = r.json()
        except:
            self.content = r.content


    @property
    def ok(self):

        if self.status_code == 200:
            return True
        else:
            return False
