"""
from django.test import TestCase
from rango.models import Category
# Create your tests here.

class CategoryTests(TestCase):
    
    def test_str(self):
        
        category = Category(name="testinimi", views=2, likes=2)
        
        self.assertEquals(
            str(category).
            'testinimi /folder/' 2 2'
        )


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    imgpath = models.CharField(max_length=128, blank=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    ran
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.name
"""