# python stuff
from asyncio.log import logger
import os
import io
import unittest
import json

# our testing code starts here
# -----------------------------------------------------------------------------
from stepwise_plugin.models import Locale

# setup test data
HERE = os.path.abspath(os.path.dirname(__file__))
TEST_DATA = os.path.join(HERE, "data")
EXT = (".json",)


def load_json(test_file):
    test_file = test_file + ".json"
    with io.open(os.path.join(TEST_DATA, test_file), "rt", encoding="utf8") as f:
        return json.loads(f.read(), strict=False)


class TestLocale(unittest.TestCase):
    def test_persist_data(self):
        def persist(event_str: str):

            Locale(
                element_id="element_id",
                language="en-US",
                url="https://mx.stepwisemath.ai/contact/",
                value="Contacto",
            ).save()
