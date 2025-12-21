import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action

# create_action 함수를 사용하면 필요에 따라 대상 객체를 포함하는 활동 객체를 만들 수 있다.
def create_action(user, verb, target=None):
    # 마지막 순간에 비슷한 활동이 있었는지 확인
    # datetime.datetime.now()와 동일한 작업을 수행하지만 시간대를 인식하는 객체를 반환한다.
    # 장고는 시간대 지원을 활성화하거나 비활성화기 위해 USE_TZ이라는 설정을 제공한다.
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id,
                                       verb= verb,
                                       created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(
                                             target_ct=target_ct,
                                             target_id=target.id)
    if not similar_actions:
        # no existing actions found
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
