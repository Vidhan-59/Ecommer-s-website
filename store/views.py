from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from . utils import *
import datetime
import json
import os 
def processOrder(request):
    # counter = counter +1
    print('Data : ', request.body) 
    if request.method == 'POST':
        # Decode the bytes object to a string
        data_str = request.body.decode('utf-8')
        
        # Parse the JSON content
        data = json.loads(data_str)
        
        # Access specific fields
        form_data = data.get('form', {})
        name = form_data.get('name')
        email = form_data.get('email')
        total = form_data.get('total')

        shipping_data = data.get('shipping', {})
        address = shipping_data.get('address')
        city = shipping_data.get('city')
        state = shipping_data.get('state')
        zipcode = shipping_data.get('zipcode')

    print(zipcode)
    transaction_id  = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        total  = float(data['form']['total'])
        order.transaction_id  = transaction_id
        if total == float(order.get_cart_total):
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
                
    
            )
        for item in order.orderitem_set.all():
        # Accessing product name, quantity, and price for each item
            product_name = item.product.name
            quantity = item.quantity
            price = item.get_total
            print("Product Name :", product_name)
                    
            
            # define the path to the folder where you want to create the file 
            # folder_path = '\Desktop\New Project\ecommerce\Cills' 
            
            # create the folder if it doesn't exist 
            # if not os.path.exists(folder_path): 
            #     os.makedirs(folder_path) 
            
            # define the file name and path 
            # file_name = 'bill1.txt' 
            # file_path = os.path.join('/Cills/', file_name) 
            
            # create the file 
            # print('Hello world')
            with open('bill2.txt', 'w') as f: 
                f.write(f'Name  : {name}\n')
                f.write(f'Email  : {email}\n')
                f.write(f'Quantity: {quantity}\n')
                f.write(f'Price: {price}\n')
                f.write(f'Address  : {address}\n')
                f.write(f'City : {city}\n')
                f.write(f'State : {state}\n')
                f.write(f'ZipCode : {zipcode}\n')
                f.close()
                        
        # You can process these values as needed in your application
        # f = open("bills/myfile.txt", "w")
        # f.write('Name  : ',name)
        # f.write('Email  : ',email)
        # f.write("Quantity:", quantity)
        # f.write("Price:", price)
        # f.write("address  :", address)
        # f.write("City :", city)
        # f.write("State :",state)
        # f.write("ZipCode :",zipcode)
        # f.close()



        
        

            
    else:
       customer,order = guestOrder(request,data)

    total  = float(data['form']['total'])
    order.transaction_id  = transaction_id
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()


    if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
    )


    return JsonResponse('Payment subbmitted.. ', safe=False)


def store(request):
    data = cartData(request)
    cartItems= data['cartItems']
    

    products = Product.objects.all()

    context = {'products':products , 'cartItems' : cartItems}
    return render(request , 'store/store.html' , context)

def cart(request):
        data= cartData(request)
        items=  data['items']
        order = data['order']
        cartItems= data['cartItems'] 

        context = {'items' : items , 'order' : order ,'cartItems' : cartItems}
        return render(request , 'store/cart.html' , context)

def checkout(request):
    data = cartData(request)
    items=  data['items']
    order = data['order']
    cartItems= data['cartItems'] 
    context = {'items' : items , 'order' : order, 'cartItems' : cartItems}
    print(items)
    return render(request , 'store/checkout.html' , context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['Action']

    print('Action  : ' ,action)
    print('ProductID  : ' , productId)
    print(request.body)
    customer = request.user.customer
    product  = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer , complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order ,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity+1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity-1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
        
    

    return JsonResponse('Item was added', safe=False)


