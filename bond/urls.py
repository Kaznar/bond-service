from django.urls import path

from bond.views import BondViewSet, InvestmentAnalysisViewSet

urlpatterns = [
    path('', BondViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='bond-list-create'),
    path('<int:pk>/', BondViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'delete'
    }), name='bond-detail'),
    path('analysis/', InvestmentAnalysisViewSet.as_view({
        'get': 'retrieve'
    }), name='bond-analysis')
]
