from django.urls import path,include
from . import views

urlpatterns = [
    path('leads/',views.LeadsList.as_view()),
    path('leads/get/',views.LeadsgetList.as_view()),
    path('leads/update/<int:pk>',views.UpdateList.as_view()),
    path('create/',views.CreateList.as_view()),
    path('get/',views.Listget.as_view()),
]
