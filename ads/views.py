from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from ads.models import Ads, Category, Users, Locations, Compilation
from django.views.decorators.csrf import csrf_exempt
import json

from ads.permissions import PermissionsForCompilation, PermissionsForAds
from ads.serializers import UserCreateSerializer, LocationSerializer, UserListSerializer, UserDetailSerializer, \
    UserUpdateSerializer, UserDestroySerializer, CompilationListSerializer, CompilationDetailSerializer, \
    CompilationCreateSerializer, AdsDetailSerializer, CompilationDestroySerializer, CompilationUpdateSerializers, \
    AdsDeDestroySerializer, AdsUpdateSerializer


class LocAPIListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class Index(View):
    def get(self, request):
        return JsonResponse({'status': 'ok'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsView(ListView):
    model = Ads

    def get(self, request, *args, **kwargs):
        ad_list = Ads.objects.all()
        ad_list = ad_list.select_related('category', 'author').order_by('-price')

        num_id = request.GET.get('cat', None)
        if num_id:
            ad_list = ad_list.filter(category__id__exact=num_id)

        ad_text = request.GET.get('text', None)
        if ad_text:
            ad_list = ad_list.filter(name__icontains=ad_text)

        name_loc = request.GET.get('location', None)
        if name_loc:
            ad_list = ad_list.filter(author__location__name__icontains=name_loc)

        price_from = request.GET.get('price_from', None)
        price_to = request.GET.get('price_to', None)
        if price_from and price_to:
            ad_list = ad_list.filter(price__range=(int(price_from), int(price_to)))


        list_data = []
        for dt in ad_list:
            list_data.append({
                'Id': dt.id,
                'name': dt.name,
                'author_id': dt.author_id,
                'author': dt.author.first_name,
                'price': dt.price,
                'description': dt.description,
                'is_published': dt.is_published,
                'logo': dt.logo.url if dt.logo else None,
                'category': dt.category.name
            })
        return JsonResponse(list_data, safe=False)


class AdsDetailView(RetrieveAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


@method_decorator(csrf_exempt, name='dispatch')
class AdsCreateView(CreateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'is_published']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            category = Category.objects.get(pk=data['category_id'])
        except  Category.DoesNotExist as error:
            return JsonResponse({"ERROR": f"{error}"})
        try:
            author = Users.objects.get(first_name=data['author'])
        except  Category.DoesNotExist as error:
            return JsonResponse({"ERROR": f"{error}"})

        ad = Ads.objects.create(
            name=data['name'],
            author=author,
            price=data['price'],
            description=data['description'],
            is_published=data['is_published'],
            logo=data['logo'],
            category=category
        )

        return JsonResponse({'res': 'ok'}, status=200)


class AdsUpdateView(UpdateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsUpdateSerializer
    permission_classes = [IsAuthenticated, PermissionsForAds]
    authentication_classes = [JWTAuthentication]


class AdsDeleteView(DestroyAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsDeDestroySerializer
    permission_classes = [IsAuthenticated, PermissionsForAds]
    authentication_classes = [JWTAuthentication]


@method_decorator(csrf_exempt, name='dispatch')
class AdsAddImage(UpdateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'is_published', 'logo', 'category']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.logo = request.FILES["logo"]
        self.object.save()
        return JsonResponse({
            'name': self.object.name,
            'author': self.object.author.first_name,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'logo': self.object.logo.url if self.object.logo else None,
            'category': self.object.category.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by('name')
        list_data = []
        for dt in self.object_list:
            list_data.append({
                'id': dt.id,
                'name': dt.name
            })
        return JsonResponse(list_data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            caregory = self.get_object()
            return JsonResponse({
                'Id': caregory.id,
                'name': caregory.name})
        except:
            return JsonResponse({'error': 'not found'}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        category = Category.objects.create(
            name=data['name'],
        )
        category.save()
        return JsonResponse({'res': 'ok'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data['name']
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = 'cat'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, status=200)


class UsersView(ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UserListSerializer


class UsersDetailView(RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UserDetailSerializer


class UsersCreateView(CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserCreateSerializer


class UsersUpdateView(UpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserUpdateSerializer


class UsersDeleteView(DestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserDestroySerializer


class CompilationView(ListAPIView):
    queryset = Compilation.objects.all()
    serializer_class = CompilationListSerializer
    pagination_class = LocAPIListPagination
    authentication_classes = [JWTAuthentication]


class CompilationDetailView(RetrieveAPIView):
    queryset = Compilation.objects.all()
    serializer_class = CompilationDetailSerializer


class CompilationCreateView(CreateAPIView):
    queryset = Compilation.objects.all()
    serializer_class = CompilationCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class CompilationUpdateView(UpdateAPIView):
    queryset = Compilation.objects.all()
    serializer_class = CompilationUpdateSerializers
    permission_classes = [IsAuthenticated, PermissionsForCompilation]
    authentication_classes = [JWTAuthentication]


class CompilationDeleteView(DestroyAPIView):
    queryset = Compilation.objects.all()
    serializer_class = CompilationDestroySerializer
    permission_classes = [IsAuthenticated, PermissionsForCompilation]
    authentication_classes = [JWTAuthentication]


class LocationViewSet(ModelViewSet):
    queryset = Locations.objects.all()
    serializer_class = LocationSerializer
    pagination_class = LocAPIListPagination


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
