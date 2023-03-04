from django.db import models
from django.contrib.auth.models import User
from utils.time_helpers import utc_now

class Tweet(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        help_text='who posts this tweet',
    ) # better coding style
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (('user', 'created_at'),)
        ordering = ('user', '-created_at')
    

    @property
    def hours_to_now(self):
        return (utc_now() - self.created_at).seconds // 3600
    
    def __str__(self):
        # print an instance, we print the __str__ instead.
        return f'{self.created_at}{self.user}: {self.content}'