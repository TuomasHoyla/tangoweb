# myapp/api.py
from tastypie.resources import ModelResource
from rango.models import Category


class CategoryResource(ModelResource):
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'Category'
        allowed_methods = ('get', 'post', 'put','delete', 'patch')
		filtering = { "id" : ALL }