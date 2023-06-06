from django.urls import path
from .views import(
    OrderHandlingApiView
)

urlpatterns = [
    #path('items/', views.),
    path('orders/', OrderHandlingApiView.as_view()),
    #path('orders/<int:pk>/', views.order_detail),
]