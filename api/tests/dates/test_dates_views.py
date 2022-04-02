import json

import pytest
from dates.models import Date, Popular
from django.urls import reverse

from api.settings import X_API_KEY


@pytest.mark.django_db(transaction=False, reset_sequences=True)
@pytest.mark.vcr
class TestDatesViewsCase:
    def test_should_create_date(self, client, january_data):
        response = client.post(reverse("dates:list_create_dates"), data=january_data)
        response_content = json.loads(response.content)

        assert response.status_code == 201
        assert response_content["id"] == 1
        assert response_content["month"] == "January"
        assert response_content["day"] == 20
        assert response_content["fact"] not in (None, "")

    def test_should_list_dates(self, client, january_data, may_data):
        client.post(reverse("dates:list_create_dates"), data=january_data)
        client.post(reverse("dates:list_create_dates"), data=may_data)

        response = client.get(reverse("dates:list_create_dates"))
        response_content = json.loads(response.content)

        assert response.status_code == 200
        assert len(response_content) == 2

        assert response_content[0]["id"] == 1
        assert response_content[0]["month"] == "January"
        assert response_content[0]["day"] == 20
        assert response_content[0]["fact"] not in (None, "")

        assert response_content[1]["id"] == 2
        assert response_content[1]["month"] == "May"
        assert response_content[1]["day"] == 29
        assert response_content[1]["fact"] not in (None, "")

    def test_should_list_popular(self, client, january_data, may_data, november_data):
        for _ in range(2):
            client.post(reverse("dates:list_create_dates"), data=january_data)
        for _ in range(3):
            client.post(reverse("dates:list_create_dates"), data=may_data)
        client.post(reverse("dates:list_create_dates"), data=november_data)

        response = client.get(reverse("dates:get_popular"))
        response_content = json.loads(response.content)

        assert response.status_code == 200
        assert len(response_content) == 3

        assert response_content[0]["id"] == 1
        assert response_content[0]["month"] == "January"
        assert response_content[0]["days_checked"] == 2

        assert response_content[1]["id"] == 2
        assert response_content[1]["month"] == "May"
        assert response_content[1]["days_checked"] == 3

        assert response_content[2]["id"] == 3
        assert response_content[2]["month"] == "November"
        assert response_content[2]["days_checked"] == 1

    def test_should_delete_date(self, client, january_data):
        client.post(reverse("dates:list_create_dates"), data=january_data)

        response = client.delete(
            reverse("dates:delete_dates", kwargs={"pk": 1}), HTTP_X_API_KEY=X_API_KEY
        )

        assert response.status_code == 204


@pytest.mark.django_db(transaction=False, reset_sequences=True)
@pytest.mark.vcr
class TestDatesErrors:
    def test_delete_not_found(self, client, january_data):
        response = client.delete(
            reverse("dates:delete_dates", kwargs={"pk": 1}), HTTP_X_API_KEY=X_API_KEY
        )
        response_content = json.loads(response.content)

        assert response.status_code == 404
        assert response_content["detail"] == "Not found."

    def test_delete_not_authorized(self, client, january_data):
        response = client.delete(
            reverse("dates:delete_dates", kwargs={"pk": 1}),
        )
        response_content = json.loads(response.content)

        assert response.status_code == 403
        assert (
            response_content["detail"]
            == "Authentication credentials were not provided."
        )

    @pytest.mark.parametrize(
        "data",
        [
            {"day": 1},
            {"month": 1},
            {"month": 0, "day": 1},
            {"month": 13, "day": 5},
            {"month": 1, "day": -1},
            {"month": 12, "day": 40},
            {"month": 22, "day": 40},
            {"month": "wrong", "day": 40},
            {"month": 22, "day": "data"},
            {"month": "nope", "day": "nope"},
        ],
    )
    def test_post_date_bad_parameters(self, client, data):
        response = client.post(reverse("dates:list_create_dates"), data=data)

        assert response.status_code == 400
