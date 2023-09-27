import datetime

from services import get_prognoz


def test_get_prognoz():
    date = datetime.date.today()

    assert get_prognoz('111', date) is False
    assert isinstance(get_prognoz('Москва', date), dict)
