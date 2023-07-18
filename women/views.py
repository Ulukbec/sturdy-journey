import requests
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .permissions import IsOwnerOrReadOnly
from .serializers import *


class ImageSearchView(APIView):
    def get(self, request):
        keyword = request.GET.get('keyword', None)
        if not keyword:
            return Response({'error': 'Please provide a keyword in the request.'}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f'images_{keyword}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        # Ваш ключ API и URL внешнего сервиса для поиска изображений
        api_key = 'ВАШ_API_КЛЮЧ'
        api_url = f'https://example.com/api/images?keyword={keyword}&api_key={api_key}'

        try:
            # Запрос к внешнему сервису для получения данных об изображениях
            response = requests.get(api_url)
            data = response.json()
        except requests.RequestException as e:
            return Response({'error': 'Failed to fetch data from the external service.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        images = []
        for item in data['images']:
            # Сохранение данных об изображениях в базе данных
            image, _ = Image.objects.get_or_create(
                url=item['url'],
                description=item['description'],
                source=item['source']
            )
            images.append(image)

        serializer = ImageSerializer(images, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 15)  # Кэширование на 15 минут
        return Response(serializer.data, status=status.HTTP_200_OK)





class WomenAPIList(ListCreateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = [IsAuthenticated]


class WomenAPIUpdate(RetrieveUpdateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = [IsOwnerOrReadOnly]


class WomenAPIDestroy(RetrieveDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = [IsOwnerOrReadOnly]

    # def get_queryset(self):
    #     pk = self.kwargs.get('pk')
    #
    #     if not pk:
    #         return Women.objects.all()[:3]
    #
    #     return Women.objects.filter(pk=pk)
    #
    # @action(methods=['get'], detail=True)
    # def category(self, request, pk=None):
    #     cats = Category.objects.get(pk=pk)
    #     return Response({'cats': cats.name})
