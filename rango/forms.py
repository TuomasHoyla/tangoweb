from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Give category name")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page")
    url = forms.URLField(max_length=200, help_text="give URL")
    views = forms.IntegerField(initial=0)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

    # If url is not empty and doesn't start with 'http://', prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data
    
    class Meta:
        model = Page
        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('category','views',)
        #or specify the fields to include (i.e. not include the category field)
        fields = ('title', 'url')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
    