from django.urls import path
from. import views
urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("home", views.home, name='home'),
    path("room/<int:room_id>", views.room, name="room"),
    path("room", views.defs, name="def"),
    path("", views.home, name="home")
]
