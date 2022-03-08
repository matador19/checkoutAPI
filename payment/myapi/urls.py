from django.urls import include, path
from . import views



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('',views.getData),
    path('addcustomer',views.addcustomer),
    path('getdetailphoneNumber/<str:pk>',views.getdetailphoneNumber),
    path('getphone',views.getphoneNumber),
    path('addphone',views.addphone),
    #path('safaricomauth',views.safaricomauth),
    path('stkpush/<str:phone>/<str:cost>',views.stkpush),
    path('getcart',views.getcart),
    path('addcart',views.addcart)
]