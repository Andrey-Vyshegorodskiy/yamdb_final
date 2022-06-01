from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .pagination import ObjectsPagination
from .permissions import (AdminOrReadOnly, IsAdmin,
                          IsUserOrAdminOrModerOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializers,
                          GenreSerializer, ReviewSerializer, SignupSerializer,
                          TitleGetSerializer, TitlePostSerializer,
                          TokenSerializer, UserSerializer)

EMAIL_SUBJECT = 'YaMDb: confirmation code!'
EMAIL_MESSAGE = ('Здравствуйте, {}! \n Используйте приведенный ниже код '
                 ', чтобы получить токен доступа: \n {}')
ERR_CODE_MESSAGE = {'confirmation code': 'Некорректный код подтверждения!'}
ERR_MESSAGE = 'Пользователь с данным username или email уже существует'


class BaseCategoryGenreViewSet(CreateListDestroyViewSet):
    queryset = None
    serializer_class = None
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = ('slug')


class CategoryViewSet(BaseCategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseCategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('-id')
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = ObjectsPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitlePostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsUserOrAdminOrModerOrReadOnly,)
    pagination_class = ObjectsPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializers
    permission_classes = (IsUserOrAdminOrModerOrReadOnly,)
    pagination_class = ObjectsPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, created = User.objects.get_or_create(
            email=serializer.validated_data.get('email'),
            username=serializer.validated_data.get('username'),)
    except (IntegrityError, User.DoesNotExist):
        raise ValidationError(ERR_MESSAGE)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(EMAIL_SUBJECT,
              EMAIL_MESSAGE.format(user.username, confirmation_code),
              None,
              (user.email,))
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def access_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username'),)
    if not default_token_generator.check_token(
            user,
            serializer.data['confirmation_code'],):
        return Response(ERR_CODE_MESSAGE, status=status.HTTP_400_BAD_REQUEST)
    return Response({'token': str(AccessToken.for_user(user)), })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)

    @action(methods=('GET', 'PATCH'), detail=False,
            permission_classes=(IsAuthenticated,),)
    def me(self, request, **kwargs):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
