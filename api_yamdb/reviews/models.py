from datetime import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models


class UserRole:
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


CHOICES = {
    'user': UserRole.USER,
    'moderator': UserRole.MODERATOR,
    'admin': UserRole.ADMIN,
}

ROLE_LEN = max(len(v) for v in CHOICES.values())


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z',)]
    )
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField('имя', max_length=150, blank=True)
    last_name = models.CharField('фамилия', max_length=150, blank=True)
    bio = models.TextField('биография', blank=True)
    role = models.CharField('роль',
                            max_length=ROLE_LEN,
                            choices=CHOICES.items(),
                            default=UserRole.USER,
                            )

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        unique_together = ('email', 'username')
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    @property
    def is_moderator(self):
        return self.is_staff or self.role == UserRole.MODERATOR

    @property
    def is_admin(self):
        return (self.is_superuser
                or self.role == UserRole.ADMIN
                or self.is_staff)


class BaseCategoryGenre(models.Model):
    name = models.CharField(
        max_length=256,
        db_index=True
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        abstract = True

    def str(self):
        return self.name[:20]


class Category(BaseCategoryGenre):

    class Meta(BaseCategoryGenre.Meta):
        verbose_name = 'Категория'


class Genre(BaseCategoryGenre):

    class Meta(BaseCategoryGenre.Meta):
        verbose_name = 'Жанр'


class Title(models.Model):
    name = models.TextField(
        db_index=True
    )
    year = models.IntegerField(
        validators=(
            MaxValueValidator(
                limit_value=dt.now().year,
                message='Произведение ещё не вышло'),
            MinValueValidator(
                limit_value=868,
                message='Появилась первая печатная книга)')
        )
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва', auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]
        ordering = ['-id']

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        null=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва', auto_now_add=True
    )

    class Meta:
        ordering = ['-id']
