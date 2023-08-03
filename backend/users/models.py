from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class User(models.Model):
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
    )

    username = models.CharField(
        max_length=150,
        unique=True,
    )

    class Meta:
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.username
    

class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписан'
    )

    class Meta:
        verbose_name = 'Подписка на авторов'
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name='unique_follow'),
            models.CheckConstraint(check=~models.Q(user=models.F('following')),
                                   name='check_follow'),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.following.username}'
