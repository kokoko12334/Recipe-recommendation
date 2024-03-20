from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularJSONAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView
from drf_spectacular.views import SpectacularYAMLAPIView
from user.views import main_page, CustomUserViewSet, test
from recipe.views import RecipeViewSet, IngredientViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(prefix='users', viewset=CustomUserViewSet, basename="user")
router.register(prefix='recipes', viewset=RecipeViewSet, basename="recipe")
router.register(prefix='ingredients', viewset=IngredientViewSet, basename="ingredient")

urlpatterns = [
    path("", main_page, name="main_page"),
    # Open API 자체를 조회 : json, yaml, 
    path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
    path("docs/yaml/", SpectacularYAMLAPIView.as_view(), name="swagger-yaml"),
    # Open API Document UI로 조회: Swagger, Redoc
    path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui",),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema-json"), name="redoc",),
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("test/",test)
]
