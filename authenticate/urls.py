from django.urls import path
from . import views
urlpatterns = [
    path('',views.Loginapi),
    path('homev2/',views.home,name='homev2'),
    path('orders/<str:pk>/',views.leadList.as_view(),name='orders'),
    path('home/',views.listGet,name='listget'),

]
