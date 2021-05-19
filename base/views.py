from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json 
import datetime

from . utils import *
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


# Create your views here.
def Index(request):

	data = cartData(request)
	cartItems = data['cartItems']
	
	
		

	products = Product.objects.all().order_by('-date_added')
	page = request.GET.get('page', 1)
	paginator = Paginator(products, 6)
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)		


		
   

	context = {'products':products,'cartItems':cartItems,'users':users}
	return render(request, 'base/index.html',context)		
	
	
	


    
    
    



#Categories part

def Men(request):
	category=['1']
	data = cartData(request)
	cartItems = data['cartItems']

    
	

	products = Product.objects.filter(category=category)

	context = {'products':products,'cartItems':cartItems}
	return render(request, 'base/index.html', context)

def Women(request):
	category=['2']
	data = cartData(request)
	cartItems = data['cartItems']

	products = Product.objects.filter(category=category)

	context = {'products':products,'cartItems':cartItems}
	return render(request, 'base/index.html', context)

def Kids(request):
	category=['3']
	data = cartData(request)
	cartItems = data['cartItems']

	products = Product.objects.filter(category=category)

	context = {'products':products,'cartItems':cartItems}
	return render(request, 'base/index.html', context)

def Electronic(request):
	category=['4']
	data = cartData(request)
	cartItems = data['cartItems']

	products = Product.objects.filter(category=category)

	context = {'products':products,'cartItems':cartItems}
	return render(request, 'base/index.html', context)


def Mobile(request):
	category=['5']
	data = cartData(request)
	cartItems = data['cartItems']

	products = Product.objects.filter(category=category)

	context = {'products':products,'cartItems':cartItems}
	return render(request, 'base/index.html', context)


def Sports(request):
	category=['6']
	data = cartData(request)
	cartItems = data['cartItems']

	products = Product.objects.filter(category=category)

	context = {'products':products,'cartItems':cartItems}
	return render(request, 'base/index.html', context)    



def High(request):
	
	data = cartData(request)
	cartItems = data['cartItems']

	products = Product.objects.order_by('-price')

	context = {'products':products,'cartItems':cartItems}
	return render(request, 'base/index.html', context) 	


def Low(request):
	
	data = cartData(request)
	cartItems = data['cartItems']

	products = Product.objects.order_by('price')

	context = {'products':products,'cartItems':cartItems}
	return render(request, 'base/index.html', context) 		



def Cart(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']	


	context = {'items':items,'order':order,'cartItems':cartItems}
	return render(request, 'base/cart.html',context)




def Checkout(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items,'order':order,'cartItems':cartItems}
	return render(request, 'base/checkout.html',context)



def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
		messages.success(request, 'Your product added successfully!')
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
		messages.warning(request, 'Your product deleted successfully!')

		

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)



def ProcessOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id 

		if total == order.get_cart_total:
			order.complete = True
			order.isPaid = True
			order.totalprice = total
		order.save()
		messages.success(request, 'Your Order has been placed  successfully!')

		if order.shipping == True:
			ShippingAddress.objects.create(
				customer=customer,
				order = order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state =data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
				phone=data['shipping']['phone'],
			)
	else:
		print('user is not logged in')	
		print('COOKIES:', request.COOKIES)
		name = data['form']['name']
		email = data['form']['email']

		cookieData = cookieCart(request)
		items = cookieData['items']

		customer, created = Customer.objects.get_or_create(
			email=email
		)
		customer.name = name
		customer.save()

		order = Order.objects.create(
			customer=customer,
			complete=False
		)
		for item in items:
			product = Product.objects.get(id=item['product']['id'])

			orderItem = OrderItem.objects.create(
				product=product,
				order=order,
				quantity=item['quantity']
			)

		total = float(data['form']['total'])
		order.transaction_id = transaction_id 

		if total == order.get_cart_total:
			order.complete = True
			order.isPaid = True
			order.totalprice = total
		order.save()
		messages.success(request, 'Your Order has been placed  successfully!')


		if order.shipping == True:
			ShippingAddress.objects.create(
				customer=customer,
				order = order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state =data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
				phone=data['shipping']['phone'],
			)

	return JsonResponse('Payment completed.', safe=False)		




def ProcessOrderCash(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id 

		if total == order.get_cart_total:
			order.complete = True
			#order.isPaid = True
			order.totalprice = total
		order.save()
		messages.success(request, 'Your Order has been placed  successfully!')

		if order.shipping == True:
			ShippingAddress.objects.create(
				customer=customer,
				order = order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state =data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
				phone=data['shipping']['phone'],
			)
	else:
		print('user is not logged in')	
		print('COOKIES:', request.COOKIES)
		name = data['form']['name']
		email = data['form']['email']

		cookieData = cookieCart(request)
		items = cookieData['items']

		customer, created = Customer.objects.get_or_create(
			email=email
		)
		customer.name = name
		customer.save()

		order = Order.objects.create(
			customer=customer,
			complete=False
		)
		for item in items:
			product = Product.objects.get(id=item['product']['id'])

			orderItem = OrderItem.objects.create(
				product=product,
				order=order,
				quantity=item['quantity']
			)

		total = float(data['form']['total'])
		order.transaction_id = transaction_id 

		if total == order.get_cart_total:
			order.complete = True
			#order.isPaid = True
			order.totalprice = total
		order.save()
		messages.success(request, 'Your Order has been placed  successfully!')


		if order.shipping == True:
			ShippingAddress.objects.create(
				customer=customer,
				order = order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state =data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
				phone=data['shipping']['phone'],
			)

	return JsonResponse('Payment completed.', safe=False)




@staff_member_required
def ViewOrders(request):

	order = Order.objects.all()
	
	context = {'order':order}
	return render(request, 'base/orders.html',context)



def Search(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	query = request.GET['query']
	name = Product.objects.filter(name__icontains=query)
	description = Product.objects.filter(description__icontains=query)
	products = name.union(description)
	context = {'products':products, 'cartItems':cartItems}
	return render(request,'base/search.html', context)




def Productdetails(request,pk):
	

	data = cartData(request)
	cartItems = data['cartItems']
	products = Product.objects.get(pk=pk)
	top = Product.objects.all()[0:2]
	
	context = {'products':products, 'cartItems':cartItems,'top':top}
	return render(request, 'base/product_detail.html', context)


