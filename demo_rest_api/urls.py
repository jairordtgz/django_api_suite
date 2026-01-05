from django.urls import path
from . import views

urlpatterns = [
   path("index/", views.DemoRestApi.as_view(), name="demo_rest_api_resources" ),
   path("<str:item_id>/", views.DemoRestApi.as_view(), name="demo_rest_api_item" ),
]