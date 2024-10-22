from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/codes/', search_codes),  # GET
    path('api/codes/<int:code_id>/', get_code_by_id),  # GET
    path('api/codes/<int:code_id>/update/', update_code),  # PUT
    path('api/codes/<int:code_id>/update_image/', update_code_image),  # POST
    path('api/codes/<int:code_id>/delete/', delete_code),  # DELETE
    path('api/codes/create/', create_code),  # POST
    path('api/codes/<int:code_id>/add_to_tax/', add_code_to_tax),  # POST

    # Набор методов для заявок
    path('api/taxs/', search_taxs),  # GET
    path('api/taxs/<int:tax_id>/', get_tax_by_id),  # GET
    path('api/taxs/<int:tax_id>/update/', update_tax),  # PUT
    path('api/taxs/<int:tax_id>/update_status_user/', update_status_user),  # PUT
    path('api/taxs/<int:tax_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/taxs/<int:tax_id>/delete/', delete_tax),  # DELETE

    # Набор методов для м-м
    path('api/taxs/<int:tax_id>/update_code/<int:code_id>/', update_code_in_tax),  # PUT
    path('api/taxs/<int:tax_id>/delete_code/<int:code_id>/', delete_code_from_tax),  # DELETE

    # Набор методов пользователей
    path('api/users/register/', register), # POST
    path('api/users/login/', login), # POST
    path('api/users/logout/', logout), # POST
    path('api/users/<int:user_id>/update/', update_user) # PUT
]
