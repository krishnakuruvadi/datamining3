from django.urls import path


from .views import (
    common_list_view,
    ZipCodeListView,
    attractions_list_view,
    UserListView,
    add_user,
    add_zip_code_view
)

app_name = 'internals'

urlpatterns = [
    path('', common_list_view, name='common-list'),
    path('zip_codes', ZipCodeListView.as_view(), name='zip-code-list'),
    path('attractions', attractions_list_view, name='attractions-list'),
    path('users', UserListView.as_view(), name='user-list'),
    path('add_user', add_user, name='add-user'),
    path('add_zip_code', add_zip_code_view, name='add-zip-code'),
]