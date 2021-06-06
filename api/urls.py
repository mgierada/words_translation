from django.urls import path, include
from rest_framework import routers

from .views import (TranslationsViewSet,
                    LanguageViewSet,
                    SingleTranslationViewSet,
                    UserViewSet,
                    GroupViewSet)

router = routers.DefaultRouter()
router.register(r'translations', TranslationsViewSet)
router.register(r'language', LanguageViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('translation/', SingleTranslationViewSet.as_view(),
         name='translation_single'),
    path('api-auth/', include('rest_framework.urls',
         namespace='rest_framework_test')),
]
