from django.urls import path
from . import views

app_name = 'campagin'

urlpatterns = [
    path('', views.CampaginViewsList.as_view(), name="campagin-list"),
    path('<int:pk>/', views.CampaginDetailView.as_view(), name="campagin-detail"),
]
