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

