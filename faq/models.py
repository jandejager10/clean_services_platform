from django.db import models
from django.utils.text import slugify


class FAQCategory(models.Model):
    """Model for FAQ categories"""
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
    )
    order = models.IntegerField(
        default=0,
        help_text="Order in which category appears",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "FAQ Category"
        verbose_name_plural = "FAQ Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class FAQItem(models.Model):
    """Model for individual FAQ items"""
    category = models.ForeignKey(
        FAQCategory,
        on_delete=models.CASCADE,
    )
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.IntegerField(
        default=0,
        help_text="Order in which question appears within category",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this FAQ is visible to users",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "FAQ Item"
        verbose_name_plural = "FAQ Items"
        ordering = ['category', 'order', 'question']
        indexes = [
            models.Index(fields=['category', 'order']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.question 