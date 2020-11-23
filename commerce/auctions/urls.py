from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("listing/<int:id>", views.display_listing, name="display_listing")
]
