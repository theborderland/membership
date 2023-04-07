from pretix.api.serializers.i18n import I18nAwareModelSerializer

from .models import LotteryEntry, RefundRequest

class LotteryEntrySerializer(I18nAwareModelSerializer):
    class Meta:
        model = LotteryEntry
        fields = ["id", "email", "first_name", "last_name", "dob", "low_income", "timestamp", "ip", "cookie", "browser"]

class RefundRequestSerializer(I18nAwareModelSerializer):
    class Meta:
        model = RefundRequest
        fields = "__all__"
