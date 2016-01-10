from tastypie.resources import ModelResource
from rango.models import Page, Category
from tastypie.constants import ALL


class PageResource(ModelResource):
    
    class Meta:
        resource_name='page'
        queryset = Page.objects.all()
        #allowed_methods = ['get']
        filtering = { "title" : ALL }
        


class CategoryResource(ModelResource):
    
    class Meta:
        resource_name='category'
        queryset = Category.objects.all()
        #toimii http://localhost:8000/api/v1/category/?format=json&name__contains=rekki
        #Tähän vois tulla että if query &filter=name then filtering "name ": all else..
        filtering = { "name" : ALL }
        excludes = ['slug', 'id', 'likes', 'views', 'imgpath']
        
        #oma custom field
    def dehydrate(self, bundle):
        bundle.data['custom_field'] = "empty"
        return bundle
    
