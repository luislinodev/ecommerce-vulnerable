from django.urls import path
from . import views

app_name = 'debug_endpoints'

urlpatterns = [
    # VULNERABLE ENDPOINTS FOR PENETRATION TESTING
    path('sql-injection/', views.sql_injection, name='sql_injection'),
    path('cmd-injection/', views.command_injection, name='command_injection'),
    path('read-file/', views.file_read, name='file_read'),
    path('xml-parser/', views.xml_parser, name='xml_parser'),
    path('system-info/', views.system_info, name='system_info'),
    path('weak-auth/', views.weak_auth, name='weak_auth'),
    path('unsafe-pickle/', views.unsafe_pickle, name='unsafe_pickle'),
    path('log-data/', views.log_data, name='log_data'),
    path('get-logs/', views.get_logs, name='get_logs'),
    path('process-data/', views.process_data, name='process_data'),
]
