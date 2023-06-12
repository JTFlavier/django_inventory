# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, mixins, viewsets
from .models import Order, Customer, Item
from .serializers import *
from .tasks import update_item_stock

# https://www.bezkoder.com/django-rest-api/

# class CreateListModelMixin(object):
#     def get_serializer(self, *args, **kwargs):
#         """ if an array is passed, set serializer to many """
#         if isinstance(kwargs.get('data', {}), list):
#             kwargs['many'] = True
#         return super(CreateListModelMixin, self).get_serializer(*args, **kwargs)

# TODO: add 
class OrderHandlingApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        todos = Order.objects.all()
        serializer = OrderSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        order_number = request.data.get("order_number")
        items = request.data.get("items")
        customer = request.data.get("customer")

        # filter items based on input 
        sku_ids = [x["sku"] for x in items]

        items_to_check = Item.objects.filter(sku__in=sku_ids).values()
        
        # check that items exist
        if (len(items) != items_to_check.__len__()):
            error_text = "We do not sell the following items: \n"

            for_sku_diff = [x["sku"] for x in items_to_check]
            sku_diff = list(set(sku_ids) - set(for_sku_diff))

            for sku in sku_diff:
                error_text = error_text + f"\n{sku}"

            return Response(error_text, status=status.HTTP_400_BAD_REQUEST)

        # check if there are enough items (item quantity >= input quantity)
        skus_wo_enough_stock = []

        for sku in items:
            curr_item = items_to_check.get(sku = sku["sku"])

            if (curr_item["quantity"] < sku["quantity"]):
                skus_wo_enough_stock.append(sku["sku"])
        # if not enough: return 401
        if (len(skus_wo_enough_stock) > 0):
            error_text = "The following items do not have enough stock: \n"

            for sku in skus_wo_enough_stock:
                error_text = error_text + f"\n{sku}"
            
            return Response(error_text, status=status.HTTP_400_BAD_REQUEST)


        # update stock w/ celery
        update_item_stock(items)

        # send email w/ celery

        items_after_update = Item.objects.filter(sku__in=sku_ids).values()

        return Response(items_after_update, status=status.HTTP_200_OK)
    
## TODO: refactor put
## TODO: add delete
class ItemHandlingView(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ItemSerializer

    def get_queryset(self):
        is_available = self.request.query_params.get('isAvailable')

        if (is_available == "True"):
            return Item.objects.filter(status = True)
        elif (is_available == "False"):
            return Item.objects.filter(status = False)
        else:
            return Item.objects.all()

    def get_item(self, sku, user_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return Item.objects.get(sku=sku)
        except Item.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        '''
        Get all items depending on 'isAvailable'
        '''
        
        #    items
    
        #if (isAvailable == "True"):
        #    items =  Item.objects.filter(status = True)
        #elif (isAvailable == "False"):
        #    items = Item.objects.filter(status = False)
        #else:
            #items = Item.objects.all()
        items = self.get_queryset()

        serializer = ItemSerializer(items, many=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(ItemHandlingView, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   # 4. Update
    def put(self, request, *args, **kwargs):
        '''
        Updates the todo item with given todo_id if exists
        '''

        sku = request.data.get('sku')
        item_instance = self.get_item(sku, request.user.id)
        if not item_instance:
            return Response(
                {"res": "SKU does not exist"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'quantity': request.data.get('quantity'), 
        }
        serializer = ItemSerializer(instance = item_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## TODO: add customer handler

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

