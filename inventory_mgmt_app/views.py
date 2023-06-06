# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Order, Customer, Item
from .serializers import *

# Create your views here.

class OrderHandlingApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    #def get_all_items(self, request, *args, **kwargs):
    def get(self, request, *args, **kwargs):
        '''
        Get all items, regardless of availability
        '''

        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# def items_list(request): 
#     """
#     GET: return all items
#     POST: n/a
#     PUT: update item status (aka quantity)
#     DELETE: delete item 
    
#     TODO: add behavior for available vs out of stock items
#     """

# @csrf_exempt
# def order_list(request):
#     """
#     List all code orders, or create a new order.
#     """
#     if request.method == 'GET':
#         orders = Order.objects.all()
#         serializer = OrderSerializer(orders, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = OrderSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
    
# @csrf_exempt
# def order_detail(request, pk):
#     """
#     Retrieve, update or delete a code order.
#     """
#     try:
#         order = Order.objects.get(pk=pk)
#     except order.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = OrderSerializer(order)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = OrderSerializer(order, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         order.delete()
#         return HttpResponse(status=204)

