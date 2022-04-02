import pytest
from dates.models import Date, Popular


@pytest.mark.django_db(transaction=False, reset_sequences=True)
class TestDateModelsCase:
    def test_should_create_date_model(self, date_model):
        assert date_model.id == 1
        assert date_model.month_number == "12"
        assert date_model.fact == "Some fun fact"

    def test_should_create_popular_model(self, popular_model):
        assert popular_model.id == 1
        assert popular_model.month_number == "1"
        assert popular_model.days_checked == 31
