from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator


class Pic(models.Model):
    title = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    price = models.DecimalField(max_digits=9, decimal_places=2)
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    picture = models.BinaryField(null=True, blank=True, editable=True)
    content_type = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )
    ad = models.ForeignKey(Pic, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        if len(self.text) < 15 : return self.text
        return self.text[:11] + "..."