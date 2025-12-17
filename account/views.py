from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
import logging

logging.basicConfig(level=logging.DEBUG)
def user_login(request):
    if request.method == 'POST':
        # user_login 뷰가 GET 요청으로 호출되면 새로운 로그인 폼이 form = LoginForm() 으로 인스턴스화된다.
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # 폼 데이터가 유효한 경우 사용자는 authenticate 메서드를 사용해 데이터베이스에 인증한다.
            # 올바른 경우 User 객체를 반환한다.
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                # 사용자가 성공적으로 인증되면 is_active 속성을 체크해서 사용자의 상태를 확인한다.
                if user.is_active:
                    # login 메서드는 현재 세션에 사용자를 설정한다.
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

# login_required 데코레이터는 현재 사용자가 인증되었는지 확인한다.
# 사용자가 인증되었으면 데코레이트된 뷰를 실행한다. 사용자가 인증되지 않은 경우 원래 요청된 URL을 next라는 GET 매개 변수에 담아서 사용자를 로그인 URL로 리디렉션한다.
@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            messages.success(request, 'Profile updated '\
                                      'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        # ProfileEditForm은 커스텀 Profile 모델의 추가 개인 데이터를 지정한다.
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})