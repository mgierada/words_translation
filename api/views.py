from .models import Translation, Language
from .serializers import (TranslationSerializers,
                          LanguageSerializers,
                          SingleTranslationSerializers,
                          AvailableLanguagesSerializers,
                          UserSerializer,
                          GroupSerializer)

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError


class TranslationsViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows to see translations.
    '''
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializers

    @action(detail=True, methods=['get'])
    def single(self, request, pk=None):
        queryset = Translation.objects.get(pk=pk)
        serializer = TranslationSerializers(queryset)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        Translation.objects.filter(pk=pk).delete()
        return Response({'pk': 'Successfully removed'})

    @action(detail=True, methods=['post'])
    def post(self, request, pk=None):

        data = request.data
        print(data)

        # conversion = request['conversion']
        conversion = 'en-pl'
        # i = request['i']
        i = 18
        frontCard = data['frontCard']
        backCard = data['backCard']
        pronunciation_frontCard = data['pronunciation_frontCard']
        pronunciation_backCard = data['pronunciation_backCard']
        source_language = data['source_language']
        target_language = data['target_language']

        try:
            Language.objects.create(
                conversion=conversion,
            )
        except IntegrityError:
            pass

        language_obj = Language.objects.filter(
            conversion__contains=conversion)[0]
        Translation.objects.create(
            translation=language_obj,
            i=i,
            frontCard=frontCard,
            backCard=backCard,
            pronunciation_frontCard=pronunciation_frontCard,
            pronunciation_backCard=pronunciation_backCard,
            source_language=source_language,
            target_language=target_language,
        )
        return Response({'POST': 'Object created successfully!'})


class LanguageViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows to see Languages.
    '''
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]
    queryset = Language.objects.all()
    serializer_class = LanguageSerializers
    lookup_field = 'conversion'

    @action(detail=True, methods=['get'])
    def single(self, request, conversion=None):
        queryset = Language.objects.get(conversion=conversion)
        serializer = LanguageSerializers(queryset)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def remove(self, request, conversion=None):
        Language.objects.filter(conversion=conversion).delete()
        return Response({'Conversion': 'Successfully removed'})


class AvailableLanguagesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Language.objects.all()
    serializer_class = AvailableLanguagesSerializers

    # ISO 639-1 code has always lenght of 2
    length = 2

    # def retrieve(self, request, *args, **kwargs):
    #     return Response({'something': 'my custom JSON'})

    def list(
            self,
            request,
            *args,
            **kwargs):
        ''' Overwrite the defaut list method to return flatten
        list of conversions '''
        from iso639 import languages
        from .iso639_to_iso3166 import iso_exceptions_dict

        languages_objects = Language.objects.all()
        serializers = self.get_serializer(languages_objects, many=True)
        conversions_list = []
        for id, item in enumerate(serializers.data):
            conversion = {}
            iso639_lang_code = item['conversion'][self.length+1:]
            language_name = languages.get(part1=str(iso639_lang_code)).name

            iso3166_lang_code = iso639_lang_code
            if iso639_lang_code in iso_exceptions_dict:
                iso3166_lang_code = iso_exceptions_dict[iso639_lang_code]

            # prepare a json response
            conversion['id'] = id
            conversion['conversion'] = item['conversion']
            conversion['target_language_iso639'] = iso639_lang_code
            conversion['target_language_iso3166'] = iso3166_lang_code
            conversion['name'] = language_name
            conversions_list.append(conversion)

        return Response({'available_conversions': conversions_list})


class SingleTranslationViewSet(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = SingleTranslationSerializers

    def get_queryset(self):
        '''
        Optionally show translations only for a given conversion,
        by filtering against a `conversion` query parameter in the URL.

        e.g.

        http://127.0.0.1:8000/translation/?conversion=en-de

        will show translation only for en-de conversion

        '''
        queryset = Translation.objects.all()
        conversion = self.request.query_params.get('conversion')
        if conversion is not None:
            queryset = queryset.filter(translation_id=conversion)
        return queryset


class TranslationsViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows to see translations.
    '''
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializers


class LanguageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Language.objects.all()
    serializer_class = LanguageSerializers


class SingleTranslationViewSet(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = SingleTranslationSerializers

    def get_queryset(self):
        '''
        Optionally show translations only for a given conversion,
        by filtering against a `conversion` query parameter in the URL.

        e.g.

        http://127.0.0.1:8000/translation/?conversion=en-de

        will show translation only for en-de conversion

        '''
        queryset = Translation.objects.all()
        conversion = self.request.query_params.get('conversion')
        if conversion is not None:
            queryset = queryset.filter(translation_id=conversion)
        return queryset


class TranslationsViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows to see translations.
    '''
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializers
    # permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows users to be viewed or edited.
    '''
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows groups to be viewed or edited.
    '''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
