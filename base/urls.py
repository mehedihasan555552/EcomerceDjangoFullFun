from django.urls import path

from . import views


urlpatterns = [

	path('', views.Index, name="index"),
	path('mens/', views.Men, name='men'),
	path('women/', views.Women, name='women'),
	path('kids/', views.Kids, name='kids'),
	path('electronic/', views.Electronic, name='electronic'),
	path('mobile/', views.Mobile, name='mobile'),
	path('sports/', views.Sports, name='sports'),
	path('high/', views.High, name='high'),
	path('low/', views.Low, name='low'),


	path('cart/', views.Cart, name='cart'),
	path('checkout/', views.Checkout, name='checkout'),
	path('update_item/', views.updateItem, name='update_item'),
	path('process_order/', views.ProcessOrder, name='process_order'),
	path('process_order_cash/', views.ProcessOrderCash, name='process_order_cash'),
	
	

	path('orders/', views.ViewOrders, name='orders'),

	path('search/', views.Search, name='search'),
	path('products/<int:pk>/', views.Productdetails, name='product-detail'),

	



]