from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("placebid", views.placebid, name="placebid"),
    path("closelisting", views.closelisting, name="closelisting"),
    path("comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("category/<int:categoryid>", views.category, name="category"),
]
