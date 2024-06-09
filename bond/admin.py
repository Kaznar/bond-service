from django.contrib import admin
from django.utils.html import format_html

from .models import Bond


@admin.register(Bond)
class BondAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'user', 'isin', 'value', 'interest_rate', 'purchase_date', 'is_active',
        'maturity_date', 'formatted_future_value'
    )
    list_filter = ('user', 'is_active', 'purchase_date', 'maturity_date')
    search_fields = ('name', 'isin', 'user__email')
    readonly_fields = ('future_value',)
    date_hierarchy = 'created_at'

    def formatted_future_value(self, obj):
        return format_html('<b>{}</b>', obj.future_value)

    formatted_future_value.short_description = 'Future Value'
