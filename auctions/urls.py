from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>/", views.Particularlistingspage, name="Particularlistingspage"),
    path("Watchlist/", views.Watchlist, name="Watchlist"),
    path("Categories/", views.Categories, name="Categories"),
    path("listings/", views.listings, name="listings"),
    path("add/", views.add_listing, name="add_listing")
]
