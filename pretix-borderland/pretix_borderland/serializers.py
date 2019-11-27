from pretix.api.serializers.i18n import I18nAwareModelSerializer

from .models import LotteryForm

class LotteryFormSerializer(I18nAwareModelSerializer):
    class Meta:
        model = LotteryForm
        fields = "__all__"
