import requests
from django.db.models import F
from rest_framework import status
from rest_framework.generics import DestroyAPIView, ListAPIView, ListCreateAPIView
from rest_framework.response import Response

from api.settings import NUMBER_API_GET_FACT

from .models import Date, Popular
from .permissions import HasAPIHeader
from .serializers import DateSerializer, PopularSerializer


class ListCreateDates(ListCreateAPIView):
    queryset = Date.objects.all()
    serializer_class = DateSerializer

    fact_url = NUMBER_API_GET_FACT

    def create(self, request, *args, **kwargs):
        date_info = request.data.dict()
        resp = requests.get(  # Get fact from external API for given date
            self.fact_url.format(day=date_info.get("day"), month=date_info.get("month"))
        )

        try:
            resp.raise_for_status()
        except requests.HTTPError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer_data = {
            "day": date_info.get("day"),
            "month_number": date_info.get("month"),
            "fact": resp.text,
        }

        serializer = self.serializer_class(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        date = serializer.save()

        # Create popular model if one DOES NOT exists
        popular, created = Popular.objects.get_or_create(
            month_number=date_info.get("month")
        )

        if not created:  # If popular model for given date exist increment days_checked
            popular.days_checked = F("days_checked") + 1
            popular.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteDate(DestroyAPIView):
    queryset = Date.objects.all()
    serializer_class = DateSerializer
    permission_classes = [
        HasAPIHeader,
    ]


class GetPopular(ListAPIView):
    queryset = Popular.objects.all()
    serializer_class = PopularSerializer
