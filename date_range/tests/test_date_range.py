import sys
from aidate.drange import get_date_range

def test_only_year():
    assert get_date_range('2021') == datetime(2021)
