from django.contrib.auth import get_user_model  # importing custom user model
from django.db import models

User = get_user_model()


class UserSubscription(models.Model):
    """ Intermediate model enabling Users to subscribe to one another. """
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followed_users'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
    )

    class Meta:
        verbose_name = 'User Subscription'
        verbose_name_plural = 'User Subscriptions'
        ordering = ['subscriber']

    def __str__(self):
        return self.subscriber.username + ' >>> ' + self.following.username
