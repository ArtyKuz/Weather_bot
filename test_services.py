import datetime

from services import get_forecast


def test_get_forecast():
    date = datetime.date.today()

    assert get_forecast('111', date) is False
    assert isinstance(get_forecast('Москва', date), dict)
