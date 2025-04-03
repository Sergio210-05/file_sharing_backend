from django.urls import path

from . import views


urlpatterns = [
    path('csrf/', views.get_csrf, name='api-csrf'),
    path('login/', views.login_view, name='api-login'),
    path('logout/', views.logout_view, name='api-logout'),
    path('session/', views.session_view, name='api-session'),
    path('user_info/', views.user_info, name='api-userInfo'),
    path('user_info/<int:member_id>', views.user_info, name='api-userInfo-id'),
    path('registration/', views.registration_view, name='api-registration'),
    path('profile/', views.change_userdata, name='api-change_userdata'),
    path('get_all_users/', views.get_all_users, name='api-get_all_users'),
    path('change_admin_status/<int:member_id>/', views.change_admin_status, name='api-change_admin_status'),
    path('remove_user/<int:member_id>/', views.remove_user, name='api-remove_user'),
    path('remove_user_sessions/', views.remove_user_sessions, name='api-userRemoveSessions'),
]
