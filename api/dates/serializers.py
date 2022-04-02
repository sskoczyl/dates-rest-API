from rest_framework import serializers

from .models import Date, Popular


class DateSerializer(serializers.ModelSerializer):
    month = serializers.CharField(source="get_month_number_display", read_only=True)

    class Meta:
        model = Date
        fields = ("id", "month_number", "month", "day", "fact")
        extra_kwargs = {
            "month_number": {"write_only": True},
        }


class PopularSerializer(serializers.ModelSerializer):
    month = serializers.CharField(source="get_month_number_display", read_only=True)

    class Meta:
        model = Popular
        fields = ("id", "month_number", "month", "days_checked")
        extra_kwargs = {
            "month_number": {"write_only": True},
        }
