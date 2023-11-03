from django.urls import path
from . import views

urlpatterns = [
    # path('normal_sort/', views.normal_sort),
    # path('priority_queue/', views.priority_queue),
    # path('bubble_sort/', views.bubble_sort),
    path('read_csv/', views.csv_return_json, name='read_csv'),
    path('read_csv_has_null/', views.csv_return_json_has_null, name='read_csv_has_null'),
    path('find_similar/', views.find_similar, name='find_similar'),
]

