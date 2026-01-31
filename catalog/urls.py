from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (
    ProductListView, 
    ContactsView, 
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductModerationListView,
    ProductUnpublishView,
    ProductPublishView,
    CategoryProductsView
)

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    
    # URL для категорий
    path('category/<int:category_id>/', CategoryProductsView.as_view(), name='category_products'),
    
    # URL для модерации
    path('moderation/', ProductModerationListView.as_view(), name='moderation_list'),
    path('moderation/unpublish/<int:pk>/', ProductUnpublishView.as_view(), name='product_unpublish'),
    path('moderation/publish/<int:pk>/', ProductPublishView.as_view(), name='product_publish'),
]
