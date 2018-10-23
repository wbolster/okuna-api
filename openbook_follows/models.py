from django.db import models

# Create your models here.
from openbook_auth.models import User

from openbook_lists.models import List


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows')
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='follows', null=True)
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', null=True)

    class Meta:
        unique_together = ('user', 'followed_user',)

    @classmethod
    def create_follow(cls, user_id, followed_user_id, list_id=None):
        return Follow.objects.create(user_id=user_id, followed_user_id=followed_user_id, list_id=list_id)

    @classmethod
    def delete_follow(cls, user_id, followed_user_id):
        follow = Follow.objects.get(user_id=user_id, followed_user_id=followed_user_id)
        follow.delete()

    @classmethod
    def follow_exists(cls, user_a_id, user_b_id):
        count = Follow.objects.filter(user_id=user_a_id, followed_user_id=user_b_id).count()

        if count > 0:
            return True

        return False

    @classmethod
    def follow_with_id_exists_for_user(cls, follow_id, user):
        count = user.follows.filter(pk=follow_id).count()

        if count > 0:
            return True

        return False
