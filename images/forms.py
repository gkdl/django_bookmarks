from django import forms
from .models import Image
from django.core.files.base import ContentFile
from django.utils.text import slugify
import requests


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput,
        }

    # 제공된 이미지 URL이 유효한지 확인하기 위해 JPEG, PNG 파일만 공유할 수 있도록 파일의 확장자가 .jpg, jpeg 또는 .png로 끝나는지 확인한다.
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not ' \
                                        'match valid image extensions.')
        return url

    # 폼의 save 메서드를 commit=False로 호출해서 이미지 인스턴스를 만든다.
    # 이미지의 URL은 폼의 cleaned_data 딕셔너리에서 조회된다.
    # 이미지 이름은 image 제목을 슬러그화한 값과 이미지의 원본 파일의 확장자를 결합해서 만들어진다.
    # 파이썬 라이브러리 Requests는 이미지 URL로 HTTP GET 요청을 전송해 이미지를 다운로드하는 데 사용된다.
    # image 필드의 save 메서드가 호출될 때 다운로드한 파일 콘텐츠로 만들어진 contentFile 객체를 전달한다. 이런 방식으로 파일은 프로젝트의 미디어 디렉터리에 저장된다. 객체를 데이터베이스에 저장하지 않도록 save=False 매개 변수가 전달된다.
    # 모델 폼의 원래 save 메서드와 동일한 동작을 유지하기 위해 commit 매개 변수가 True인 경우에만 폼이 데이터베이스에 저장된다.
    def save(self, force_insert=False,
                   force_update=False,
                   commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'
        # download image from the given URL
        response = requests.get(image_url)
        image.image.save(image_name,
                         ContentFile(response.content),
                         save=False)
        if commit:
            image.save()
        return image
