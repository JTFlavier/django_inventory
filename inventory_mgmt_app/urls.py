from django.urls import path
from .views import(
    OrderHandlingApiView,
    ItemHandlingView
)

urlpatterns = [
    #path('items/', views.),
    path('orders/', OrderHandlingApiView.as_view()),
    path('items/', ItemHandlingView.as_view())
    #path('orders/<int:pk>/', views.order_detail),
]