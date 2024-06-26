from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("list/<int:listid>", views.list, name="list"),
    path("closelist", views.closelist, name='closelist'),
    path("watchlist", views.watchlist, name='watchlist'),
    path("createcomment", views.createcomment, name="createcomment"),
    path("category", views.category, name="category"),
    path("category/<int:categoryid>/",
         views.categoryselect, name="index_with_category"),
    path('inactive/', views.inactive_index, name='inactive_index'),

]
