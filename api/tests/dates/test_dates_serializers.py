import pytest
from dates.serializers import DateSerializer, PopularSerializer
from rest_framework.serializers import ValidationError


@pytest.mark.django_db(transaction=False, reset_sequences=True)
class TestDateSerializersCase:
    def test_should_serialize_date_model(self, date_model):
        serializer = DateSerializer(instance=date_model)
        data = serializer.data

        assert data.get("month") == "December"
        assert data.get("id") == 1
        assert data.get("day") == 1
        assert data.get("fact") == "Some fun fact"

    def test_should_serialize_date_data(self, date_model_data):
        serializer = DateSerializer(data=date_model_data)
        serializer.is_valid(raise_exception=True)
        date = serializer.save()

        assert date.id == 1
        assert date.month_number == "12"
        assert date.fact == "Some fun fact"

    def test_should_serialize_popular_model(self, popular_model):
        serializer = PopularSerializer(instance=popular_model)
        data = serializer.data

        assert data.get("month") == "January"
        assert data.get("id") == 1
        assert data.get("days_checked") == 31

    def test_should_serialize_popular_data(self, popular_model_data):
        serializer = PopularSerializer(data=popular_model_data)
        serializer.is_valid(raise_exception=True)
        popular = serializer.save()

        assert popular.id == 1
        assert popular.month_number == "1"
        assert popular.days_checked == 31


@pytest.mark.django_db(transaction=False, reset_sequences=True)
class TestDateSerializersErrorsCase:
    @pytest.mark.parametrize(
        "data",
        [
            {"month_number": "1", "day": 35, "fact": "Fact"},
            {"month_number": "0", "day": 4, "fact": "Fact"},
            {"month_number": "12", "day": 0, "fact": "Fact"},
            {"month_number": 13, "day": 1, "fact": "Fact"},
            {"month_number": "0", "day": 5, "fact": ""},
            {"month_number": "3", "day": 3},
            {"month_number": "5", "fact": "Fact"},
            {"day": 25, "fact": "Fact"},
        ],
    )
    def test_should_raise_date_error(self, data):
        serializer = DateSerializer(data=data)

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    @pytest.mark.parametrize(
        "data",
        [
            {"month_number": 1, "days_checked": -1},
            {"month_number": "January", "days_checked": 0},
            {"month_number": "12", "days_checked": 0},
        ],
    )
    def test_should_raise_popular_error(self, data):
        serializer = PopularSerializer(data=data)

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
