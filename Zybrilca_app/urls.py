from django.urls import path
from . import views

app_name = 'Zybrilca_app'
urlpatterns = [
    path('', views.index, name="index_url"),
    path('show_dict/', views.show_dictionaries, name='show_dictionaries'),
    path('temp_show_lists/', views.temp_show_lists, name='show_lists'),
    path('create_dictionary/', views.create_dictionary, name='create_dictionary'),
    path('dictionary_testing/<int:dict_id>/', views.dictionary_testing, name='dictionary_testing'),
    path('profile/', views.profile, name="profile"),
    path('edit_dictionary/<int:dict_id>/', views.edit_dictionary, name="edit_dictionary"),
    path('edit_word/<int:dict_id>/<int:wordpair_id>/', views.edit_word, name="edit_word"),
    path('remove_dictionary/', views.remove_dictionary, name='remove_dictionary'),
]
