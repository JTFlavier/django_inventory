from django.urls import path
from .views import(
    OrderHandlingView,
    ItemHandlingView
)

urlpatterns = [
    #path('items/', views.),
    path('orders/', OrderHandlingView.as_view()),
    path('items/', ItemHandlingView.as_view({'get': 'list'})),
    #path('orders/<int:pk>/', views.order_detail),
]