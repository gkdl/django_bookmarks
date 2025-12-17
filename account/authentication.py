from django.contrib.auth.models import User
from account.models import Profile


class EmailAuthBackend:
    """
    Authenticate using an e-mail address.
    """

    # authenticate : 주어진 이메일 주소를 가진 사용자를 조회하고 내장된 사용자 모델의 check_password 메서드를 사용해서 패스워드를 확인한다.
    # DoesNotExist : 지정된 이메일 주소를 가진 사용자가 없을때
    # MultipleObjectsReturned : 동일한 이메일 주소를 가진 여러 사용자가 발견될때
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    # user_id 매개 변수에 제공된 ID를 통해 사용자를 획득힌다.
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

# backend : 사용자 인증에 사용되는 소셜 인증 백엔드이다. 프로젝트의 AUTHENTICATION_BACKENDS 설정에 소셣 인증 백엔드를 추가했다.
# user : 인증된 산규 또는 기존 사용자의 User 인스턴스입니다.
def create_profile(backend, user, *args, **kwargs):
    """
    Create user profile for social authentication
    """
    Profile.objects.get_or_create(user=user)
