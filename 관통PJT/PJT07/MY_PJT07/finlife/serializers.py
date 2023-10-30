from rest_framework import serializers
from .models import DepositProducts, DepositOptions

class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'


class DepositOptionsSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='DepositOptions.product')
    class Meta:
        model = DepositOptions
        # fields =  ('fin_prdt_cd_id', 'intr_rate_type_nm', 'intr_rate', 'intr_rate2', 'save_trm', )
        fields = '__all__'
        