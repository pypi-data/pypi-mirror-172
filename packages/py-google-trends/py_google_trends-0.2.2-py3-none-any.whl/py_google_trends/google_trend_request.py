from datetime import datetime, timedelta
import json
from typing import Dict, Generator, List, Literal, Tuple
import requests

from py_optional import Optional

URL_TRENDS_MAIN = "https://trends.google.com/?geo={}"
URL_EXPLORE = "https://trends.google.com/trends/api/explore"
URL_WIDGET_DATA_MULTILINE = "https://trends.google.com/trends/api/widgetdata/multiline"


TOKEN_EXTRACT_METHODS = {
    'interest_over_time': lambda widget: Optional.of(widget)
    .filter(lambda w: w['id'] == 'TIMESERIES')
    .or_else(None),

    'interest_by_region': lambda widget: Optional.of(widget)
    .filter(lambda w: w['id'] == 'GEO_MAP')
    .or_else(None),

    'related_topics': lambda widget: Optional.of(widget)
    .filter(lambda w: 'RELATED_TOPICS' in w['id'])
    .or_else(None),

    'related_queries': lambda widget: Optional.of(widget)
    .filter(lambda w: 'RELATED_QUERIES' in w['id'])
    .or_else(None),
}


class TimeRange:
    def __init__(self, start, end=datetime.now()):
        self.start = start
        self.end = end

    def to_google_format(self):
        diff = (self.end - self.start)
        assert diff.total_seconds(
        ) >= 0, "start must be before end. start: {}, end: {}".format(self.start, self.end)

        if diff.days < 8:
            return 'now 7-d'.format(diff.days)
        else:
            return "{} {}".format(self.start.strftime("%Y-%m-%d"), self.end.strftime("%Y-%m-%d"))

    def is_valid_timestamp(self, timestamp: int) -> bool:
        return datetime.fromtimestamp(timestamp) >= self.start and datetime.fromtimestamp(timestamp) <= self.end


class TimeRanges:
    WEEK_FROM_NOW = TimeRange(datetime.now() - timedelta(days=7))


class GoogleTrendRequest:
    def __init__(self):
        self._timeout = 5
        self._timerange = None

        self._payload = {}
        self._widgets = {}

    def _get_cookie(self, session: requests.Session) -> None:
        assert self._payload['hl'] is not None

        response = session.get(URL_TRENDS_MAIN.format(self._payload['hl'][-2:]),
                               timeout=self._timeout)
        assert response.status_code == 200, response.text + \
            '\n' + str(response.status_code)

    def _get_token(self, session: requests.Session) -> None:
        assert self._payload['hl'] is not None
        assert self._payload['tz'] is not None
        assert self._payload['req'] is not None

        session.headers.update({'accept-language': self._payload['hl'],
                                'content-type': 'application/json',
                                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                                })

        self._get_cookie(session)

        response = session.get(URL_EXPLORE,
                               params=self._payload,
                               timeout=self._timeout)
        assert response.status_code == 200, self._payload

        text = response.text[4:]
        data = json.loads(text)

        self._widgets.clear()
        for widget in data['widgets']:
            for name, fn in TOKEN_EXTRACT_METHODS.items():
                if fn(widget) is not None:
                    self._widgets[name] = widget
                    continue

    def _timeline_json(self, session: requests.Session) -> str:
        self._get_token(session)
        assert self._widgets['interest_over_time'] is not None

        widget = self._widgets['interest_over_time']
        payload = {
            'req': json.dumps(widget['request']),
            'token': widget['token'],
            'tz': self._payload['tz'],
        }

        response = session.get(URL_WIDGET_DATA_MULTILINE,
                               params=payload,
                               timeout=self._timeout)
        assert response.status_code == 200, response.text + \
            '\n' + str(response.status_code)

        return json.loads(response.text[5:])

    def interest_over_time(self, session: requests.Session) -> Generator[Tuple[int, int], None, None]:
        data = self._timeline_json(session)

        default = data['default']
        timelineData = default['timelineData']
        for each in timelineData:
            time_val = int(each['time'])
            if self._timerange.is_valid_timestamp(time_val):
                yield time_val, each['value']


class GoogleTrendRequestBuilder:
    def __init__(self):
        self._hl = "en-US"
        self._tz = 360
        self._geo = ""
        self._keyword = None
        self._time_range = None
        self._category = 0
        self._property = ""

        self._timeout = 5
        self._request = GoogleTrendRequest()

    def language(self, lang: str = 'en-US'):
        self._hl = lang
        return self

    def geographic(self, geo: str = 'US'):
        self._geo = geo
        return self

    def time_zone(self, tz: int = 360):
        self._tz = tz
        return self

    def timeout(self, timeout: int = 5):
        self._timeout = timeout
        return self

    def intent(self,
               keyword: str,
               time_range: TimeRange,
               category: int = 0,
               property: Literal['', 'images', 'news', 'youtube', 'froogle'] = ''):
        assert isinstance(keyword, str), "keyword must be a simple string"
        self._keyword = keyword
        self._time_range = time_range
        self._category = category
        self._property = property

        return self

    def build(self) -> GoogleTrendRequest:
        assert self._keyword is not None, "keyword must be set"

        self._request._timeout = self._timeout
        self._request._timerange = self._time_range

        self._request._payload['hl'] = self._hl
        self._request._payload['tz'] = self._tz
        self._request._payload['req'] = {}
        # self._request._payload['req']['comparisonItem'] = [{'keyword': k,
        #                                                     'time': self._time_range.to_google_format(),
        #                                                     'geo': self._geo} for k in self._keywords]
        # The above code forces google trend to return every keywords normalized relative to each other
        self._request._payload['req']['comparisonItem'] = [{'keyword': self._keyword,
                                                            'time': self._time_range.to_google_format(),
                                                            'geo': self._geo}]
        self._request._payload['req']['category'] = self._category
        self._request._payload['req']['property'] = self._property
        self._request._payload['req'] = json.dumps(
            self._request._payload['req'])

        return self._request
