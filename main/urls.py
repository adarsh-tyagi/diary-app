from django.urls import path
from . import views

app_name="main"
urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('entries/', views.entries_view, name="entries"),
    path('entry/<int:entry_pk>/', views.entry_view, name="entry"),
    path('entry/<int:entry_pk>/delete', views.entry_delete, name="delete_entry"),
    path('add/', views.entry_add, name="add_entry")
]
