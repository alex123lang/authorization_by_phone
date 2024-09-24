from django.contrib import admin
from .models import NetworkNode, Product


@admin.action(description='Очистить задолженность перед поставщиком')
def clear_debt(modeladmin, request, queryset):
    """
    Очищает задолженность перед поставщиком для выбранных узлов сети.
    """
    queryset.update(debt=0)


class NetworkNodeAdmin(admin.ModelAdmin):
    """
    Настройки отображения узлов сети в административной панели.
    """
    list_display = ['name', 'city', 'country', 'level', 'supplier', 'debt', 'created_at']
    list_filter = ['city', 'country']
    search_fields = ['name']
    actions = [clear_debt]

    def get_readonly_fields(self, request, obj=None):
        """
        Определяет поля, которые доступны только для чтения в зависимости от контекста.
        """
        if obj:
            return ['created_at', 'level']
        return []


admin.site.register(NetworkNode, NetworkNodeAdmin)
admin.site.register(Product)
