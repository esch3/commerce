from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("close/<int:id>", views.close, name="close"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("watchlist/<int:uid>", views.watchlist, name="watchlist"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("listing/<int:id>", views.display_listing, name="display_listing")
]
