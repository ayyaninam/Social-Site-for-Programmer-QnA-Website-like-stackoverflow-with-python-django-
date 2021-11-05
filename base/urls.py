from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='home'),
    path('create-room/', views.create_room, name='create-room'),
    path('room/<int:pk>/', views.roompage, name='room-page'),
    path('update-room/<int:pk>', views.update_room, name='update-room'),
    path('login-page/', views.login_page, name='login-page'),
    path('logout-page/', views.logout_page, name='logout-page'),
    path('signup-page/', views.signup_page, name='signup-page'),
    path('profile-page/<int:pk>', views.profile_page, name='profile-page'),
    path('edit-user/<int:pk>', views.edit_user, name='edit-user'),
    path('delete-message/<int:pk>', views.delete_message, name='delete-message'),
    path('delete-room/<int:pk>', views.delete_room, name='delete-room'),
    path('topic-page/', views.topic_page, name='topic-page'),
]
