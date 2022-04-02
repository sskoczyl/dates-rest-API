import pytest
from dates.models import Date, Popular
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture()
def january_data():
    return {
        "month": 1,
        "day": 20,
    }


@pytest.fixture()
def may_data():
    return {
        "month": 5,
        "day": 29,
    }


@pytest.fixture()
def november_data():
    return {
        "month": 11,
        "day": 21,
    }


@pytest.fixture(scope="module")
def date_model_data():
    return {
        "month_number": "12",
        "day": 1,
        "fact": "Some fun fact",
    }


@pytest.fixture(scope="module")
def popular_model_data():
    return {
        "month_number": "1",
        "days_checked": 31,
    }


@pytest.fixture()
def date_model(date_model_data):
    date_model, _ = Date.objects.get_or_create(
        month_number=date_model_data.get("month_number"),
        day=date_model_data.get("day"),
        fact=date_model_data.get("fact"),
    )
    return date_model


@pytest.fixture()
def popular_model(popular_model_data):
    popular_model, _ = Popular.objects.get_or_create(
        month_number=popular_model_data.get("month_number"),
        days_checked=popular_model_data.get("days_checked"),
    )
    return popular_model
