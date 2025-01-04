from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("listing_item/<int:listing_id>", views.listing_item, name="listing_item"),
    path("create/", views.create, name="create"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:category_name>/", views.category_listings, name="category_listings"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/count/", views.watchlist_count, name="watchlist_count"),
    path('listing_item/<int:listing_id>/place_bid/', views.place_bid, name='place_bid'),
    path("listing_item/<int:listing_id>/toggle_watchlist/", views.toggle_watchlist, name="toggle_watchlist"),
    path('listing_item/<int:listing_id>/close/', views.close_auction, name='close_auction'),

]

