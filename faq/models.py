from django.db import models


# Create your models here.
class FAQCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FAQItem(models.Model):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='items')
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question
