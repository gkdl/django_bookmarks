from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

class Contact(models.Model):
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'

# 사용자 모델을 몽키 패치하기 위해 장고 모델의 add_to_class 메서드를 사용한다.
# add_to_class를 사용하는 것은 모델에 필드를 추가를 위해 권장하는 방법이 아니다.
# 관계를 생성하는 ManyToManyField를 정의하면 장고는 관계가 대칭이 되도록 강제한다. 이 경우에는 대칭이 아닌 관계를 정의하기 위해 symmetrical=False를 설정한다.
user_model = get_user_model()
user_model.add_to_class('following',
                        models.ManyToManyField('self',
                            through=Contact,
                            related_name='followers',
                            symmetrical=False))
