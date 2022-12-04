from django.urls import path
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ads.views import AdsView, AdsCreateView, AdsDetailView, AdsUpdateView, AdsDeleteView, AdsAddImage, CategoryView, \
    CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, UsersView, UsersDetailView, \
    UsersCreateView, UsersUpdateView, UsersDeleteView, CompilationView, CompilationDetailView, CompilationCreateView, \
    Logout, CompilationDeleteView, CompilationUpdateView

urlpatterns = [
    path('ad/', AdsView.as_view()),
    path('ad/create/', AdsCreateView.as_view()),
    path('ad/<int:pk>/', AdsDetailView.as_view()),
    path('ad/<int:pk>/update/', AdsUpdateView.as_view()),
    path('ad/<int:pk>/delete/', AdsDeleteView.as_view()),
    path('ad/<int:pk>/upload_image/', AdsAddImage.as_view()),

    path('cat/', CategoryView.as_view()),
    path('cat/<int:pk>/', CategoryDetailView.as_view()),
    path('cat/create/', CategoryCreateView.as_view()),
    path('cat/<int:pk>/update/', CategoryUpdateView.as_view()),
    path('cat/<int:pk>/delete/', CategoryDeleteView.as_view()),

    path('user/', UsersView.as_view()),
    path('user/<int:pk>/', UsersDetailView.as_view()),
    path('user/create/', UsersCreateView.as_view()),
    path('user/<int:pk>/update/', UsersUpdateView.as_view()),
    path('user/<int:pk>/delete/', UsersDeleteView.as_view()),

    path('compilation/', CompilationView.as_view()),
    path('compilation/<int:pk>/', CompilationDetailView.as_view()),
    path('compilation/create/', CompilationCreateView.as_view()),

    path('compilation/<int:pk>/update/', CompilationUpdateView.as_view()),
    path('compilation/<int:pk>/delete/', CompilationDeleteView.as_view()),

    path('login/', views.obtain_auth_token),
    path('logout/', Logout.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
