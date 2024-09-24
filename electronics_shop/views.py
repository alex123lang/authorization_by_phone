from rest_framework import viewsets

from electronics_shop.models import NetworkNode, Product
from electronics_shop.permissions import IsActiveEmployee
from electronics_shop.serializers import NetworkNodeSerializer, ProductSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для узлов сети.
    """
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]
    filterset_fields = ['country']  # Фильтрация по стране


class ProductViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для продуктов.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployee]
