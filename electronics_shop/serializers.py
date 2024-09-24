from rest_framework import serializers
from .models import NetworkNode, Product


class NetworkNodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для узлов сети.
    """
    level = serializers.IntegerField(read_only=True)

    class Meta:
        model = NetworkNode
        exclude = ['debt']  # Запрещаем обновление поля "debt"


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для продуктов.
    """
    class Meta:
        model = Product
        fields = '__all__'
