import logging

from django.core.cache import cache
from django.db.models import Avg, Sum
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    extend_schema, OpenApiResponse, inline_serializer
)
from rest_framework import status
from rest_framework.fields import FloatField, DecimalField
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from bond.models import Bond
from bond.serializers import BondSerializer
from bond_service.base.cache_keys import investment_analysis_cache_key

logger = logging.getLogger('bond_service')


@extend_schema(tags=['Bond'])
class BondViewSet(ModelViewSet):
    serializer_class = BondSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bond.objects.filter(user=self.request.user, is_active=True)

    @extend_schema(
        description="Retrieve a bond by its ID",
        responses={
            200: BondSerializer,
            401: OpenApiResponse(
                description='Authentication credentials were not provided.'
            ),
            404: OpenApiResponse(description='Not Found')
        }
    )
    def retrieve(self, request, pk=None):
        bond = get_object_or_404(Bond, user=request.user, id=pk, is_active=True)
        serializer = self.serializer_class(bond)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="List all active bonds for the authenticated user",
        responses={
            200: BondSerializer(many=True),
            401: OpenApiResponse(
                description='Authentication credentials were not provided.'
            )
        }
    )
    def list(self, request):
        bonds = self.get_queryset()
        serializer = self.serializer_class(bonds, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Create a new bond",
        request=BondSerializer,
        responses={
            201: BondSerializer,
            400: OpenApiResponse(description='Bad Request'),
            401: OpenApiResponse(
                description='Authentication credentials were not provided.')
        }
    )
    def create(self, request):
        data = request.data.copy()
        data['user'] = request.user
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        description="Update an existing bond",
        request=BondSerializer,
        responses={
            200: BondSerializer,
            400: OpenApiResponse(description='Bad Request'),
            401: OpenApiResponse(
                description='Authentication credentials were not provided.'),
            404: OpenApiResponse(description='Not Found')
        }
    )
    def update(self, request, pk=None):
        data = request.data.copy()
        data['user'] = request.user

        bond = get_object_or_404(Bond, user=request.user, id=pk, is_active=True)
        serializer = self.serializer_class(bond, data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Partially update an existing bond",
        request=BondSerializer,
        responses={
            200: BondSerializer,
            400: OpenApiResponse(description='Bad Request'),
            401: OpenApiResponse(
                description='Authentication credentials were not provided.'),
            404: OpenApiResponse(description='Not Found')
        }
    )
    def partial_update(self, request, pk=None):
        bond = get_object_or_404(Bond, user=request.user, id=pk, is_active=True)
        serializer = self.serializer_class(bond, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Logically delete a bond (set is_active to False)",
        responses={
            204: OpenApiResponse(description='No Content'),
            401: OpenApiResponse(
                description='Authentication credentials were not provided.'),
            404: OpenApiResponse(description='Not Found')
        }
    )
    def delete(self, request, pk=None):
        bond = get_object_or_404(Bond, user=request.user, id=pk, is_active=True)
        bond.delete()

        logger.info(f'User ID: {request.user.id}, deactivated Bond ID: {bond.id}')

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['Bond'])
class InvestmentAnalysisViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Investment user analysis",
        responses={
            200: inline_serializer(
                name='AnalysisResponse',
                fields={
                    'average_interest_rate': FloatField(),
                    'nearest_maturity_bond': BondSerializer(),
                    'total_value': DecimalField(max_digits=10, decimal_places=2),
                    'future_value': DecimalField(max_digits=10, decimal_places=2)
                }
            ),
            401: OpenApiResponse(
                description='Authentication credentials were not provided.'),
            404: OpenApiResponse(description='Not Found')
        }
    )
    def retrieve(self, request):
        user = request.user

        cache_key = investment_analysis_cache_key(user.id)
        cached_response = cache.get(cache_key)

        if cached_response:
            return Response(cached_response, status=status.HTTP_200_OK)

        bonds = Bond.objects.filter(user=user, is_active=True)

        avg_interest_rate = bonds.aggregate(Avg('interest_rate'))['interest_rate__avg']
        nearest_maturity_bond = bonds.order_by('maturity_date').first()
        total_value = bonds.aggregate(Sum('value'))['value__sum']

        future_value = sum(bond.future_value for bond in bonds)

        response_data = {
            'average_interest_rate': avg_interest_rate,
            'nearest_maturity_bond': BondSerializer(
                nearest_maturity_bond).data if nearest_maturity_bond else None,
            'total_value': total_value,
            'future_value': future_value,
        }

        cache.set(key=cache_key, value=response_data, timeout=43200)

        return Response(response_data, status=status.HTTP_200_OK)
