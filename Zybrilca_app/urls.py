from django.urls import path
from . import views

app_name = 'Zybrilca_app'
urlpatterns = [
    path('', views.index, name="index_url"),
    path('show_dict/', views.show_dictionaries, name='show_dictionaries')
]