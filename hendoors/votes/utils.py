from typing import Dict
import urllib.request
import json

from django.core.cache import cache
from django.conf import settings


def load_marks(url: str=settings.CHECKIN_SCORES_URL) -> Dict[str, int]:
    marks = cache.get('marks')
    if marks is None:
        with urllib.request.urlopen(url) as response:
            response_bytes = response.read()
        data = json.loads(response_bytes.decode())
        marks = {d['slack_id']: int(d['score']) for d in data}
        cache.set('marks', marks, 60 * 2)
    return marks


def get_marks_by_id(slack_id: str) -> int:
    marks = load_marks()
    return marks.get(slack_id, 0)
