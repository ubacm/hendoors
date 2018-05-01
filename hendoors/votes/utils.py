from typing import Dict
import urllib.request
import json

from django.conf import settings


# TODO: cache this
def load_marks(url: str=settings.CHECKIN_SCORES_URL) -> Dict[str, int]:
    with urllib.request.urlopen(url) as response:
        response_bytes = response.read()
    data = json.loads(response_bytes.decode())
    scores = {d['slack_id']: int(d['score']) for d in data}
    return scores


def get_marks_by_id(slack_id: str) -> int:
    marks = load_marks()
    return marks.get(slack_id, 0)
