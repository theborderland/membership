from pretix.api.serializers.i18n import I18nAwareModelSerializer

from .models import LotteryEntry, RefundRequest

class LotteryEntrySerializer(I18nAwareModelSerializer):
    class Meta:
        model = LotteryEntry
        fields = "__all__"


class RefundRequestSerializer(I18nAwareModelSerializer):
    class Meta:
        model = RefundRequest
        fields = "__all__"
