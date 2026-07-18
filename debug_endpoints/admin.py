from django.contrib import admin
from .models import DebugLog


@admin.register(DebugLog)
class DebugLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'message')
    search_fields = ('user', 'message')
    list_filter = ('timestamp', 'user')
    readonly_fields = ('timestamp',)
