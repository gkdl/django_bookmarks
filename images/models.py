from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            blank=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    # 객체가 생성될때 시간을 자동으로 설정하도록 auto_now_add 설정을 true로
    created = models.DateField(auto_now_add=True)
    
    # 다대다 관계
    # ManyToManyField 필드를 정의할 때 장고는 두 모델의 기본 키를 사용해서 중간에 조인 테이블을 생성한다.
    # images_image_user_like 테이블은 images_image 테이블 및 auth_user 테이블에 대한 참조가 있는 중간 테이블로 장고에 의해 생성 된다.
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)
    total_likes = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['-total_likes']),
        ]
        ordering = ['-created']

    def __str__(self):
        return self.title

    # 제목 필드의 값을 기반으로 slug 필드를 자동으로 생성하도록 Image 모델의 save 메서드를 재정의한다.
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])
