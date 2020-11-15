from django import forms
from adsv2.models import Pic
from .templatetags import sizify
from django.core.files.uploadedfile import InMemoryUploadedFile


class CreateForm(forms.ModelForm):
    max_upload_limit = 2*1024*1024
    picture = forms.FileField(required=False, label= f'File to Upload <= 2Mb')
    upload_field_name = 'picture'

    class Meta:
        model = Pic
        fields = ['title', 'text', 'price', 'picture']

    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('picture', "File size must be smaller than 2 Mb")

    def save(self, commit=True):
        instance = super(CreateForm, self).save(commit=False)

        f = instance.picture
        if isinstance(f, InMemoryUploadedFile):
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr

        if commit:
            instance.save()

        return instance


class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)