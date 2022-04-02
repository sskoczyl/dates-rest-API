from django.urls import path

from . import views

app_name = "dates"

urlpatterns = [
    path(
        "dates/",
        views.ListCreateDates.as_view(),
        name="list_create_dates",
    ),
    path(
        "dates/<int:pk>/",
        views.DeleteDate.as_view(),
        name="delete_dates",
    ),
    path(
        "popular/",
        views.GetPopular.as_view(),
        name="get_popular",
    ),
]
