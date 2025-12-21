

### 장고는 인증을 처리하기 위해 다음과 같은 클래스 기반 뷰를 제공한다
#### django.contrib.auth.views 에 있다.
- LoginView : 로그인 폼을 처리하고 사용자를 로그인시킨다.
- LogoutView : 사용자를 로그아웃 시킨다.
- PasswordChangeView : 사용자의 패스워드를 변경하는 폼을 처리한다.
- PasswordChangeOneView : 성공적인 패스워드 변경 후 사용자가 리디렉션되는 성공 뷰이다.
- PasswordResetView : 사용자가 패스워드를 재설정할 수 있다. 토큰으로 일호용 링크를 생성해서 사용자의 이메일 계정으로 보낸다.
- PasswordResetDoneView : 사용자에게 패스워드 재설정 링크가 포함된 이메일이 저송되었음을 알린다.
- PasswordResetConfirmView : 사용자가 패스워드를 설정할 수 있다.
- PasswordResetCompleteView : 사용자가 패스워드를 성공적으로 재설정한 후 리디렉션 되는 성공 뷰이다.


### wsgi.py 와 asgi.py 파일의 차이점
| 항목 | wsgi.py | asgi.py |
|------|---------|---------|
| 목적 | WSGI 서버와 Django 연결 | ASGI 서버와 Django 연결 |
| 실행 방식 | 동기(Synchronous) | 비동기(Asynchronous) |
| 지원 프로토콜 | HTTP | HTTP + WebSocket |
| 개발 서버 실행 | 사용 안 함 (runserver는 ASGI) | 사용 가능 (runserver) |
| 운영 서버 예시 | Gunicorn, uWSGI | Uvicorn, Daphne |
| async view 지원 | ❌ | ✅ |
| 장시간 연결 지원 | ❌ | ✅ |
| 주 용도 | 전통적인 CRUD, REST API | 실시간 채팅, 알림, SSE, WebSocket |
| Django 버전 | 모든 버전 | Django 3.x 이상 |
| 기본 코드 | ```python import os<br>from django.core.wsgi import get_wsgi_application<br>os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')<br>application = get_wsgi_application()``` | ```python import os<br>from django.core.asgi import get_asgi_application<br>os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')<br>application = get_asgi_application()``` |

**한 줄 요약:**  
WSGI = 동기 서버 진입점(`wsgi.py`), ASGI = 비동기 서버 진입점(`asgi.py`), 기능과 사용 환경이 달라진다.


### 시그널
- 장고는 특정 작업이 발생할 때 수신자 함수가 알림을 받을 수 있는 시그널 디스패처가 함께 제공된다.
- 시그널은 어떤 일이 발생할 때마다 코드가 무언가를 수행해야 할 때 매우 유용하다.
- pre_save 및 post_save는 모델의 save 메서드를 호출하기 전이나 후에 발생한다.
- pre_delete 및 post_delete는 모델 또는 QuerySet의 delete 메서드를 호출하기 전이나 후에 발생한다.
- m2m_changed는 모델의 ManyToManyField가 변경될 때 발생한다.

python .\manage.py runserver_plus --cert-file .\cert.crt