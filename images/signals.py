from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image

# receiver 데코레이터를 사용해서 users_like_changed 함수를 수신 함수로 등록한다.
# 이 함수를 m2m_changed 시그널에 연결한다.
# 그런 다음 이 함수를 Image.users_like.through에 연결해서 이 발신자에 의해 m2m_changed 신호가 시작된 경우에만 함수가 호출되도록 한다.
@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()
