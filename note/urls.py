from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

app_name = 'note'
urlpatterns = [
    path('', views.index, name='index'),        
    path('notes/', views.notes, name='notes'),
    path('notes/<uuid:note_id>/', views.detail, name='detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]