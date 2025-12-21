from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from .models import Contact
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import logging
from actions.utils import create_action
from actions.models import Action

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
logger = logging.getLogger(__name__)

# login_required 데코레이터는 현재 사용자가 인증되었는지 확인한다.
# 사용자가 인증되었으면 데코레이트된 뷰를 실행한다. 사용자가 인증되지 않은 경우 원래 요청된 URL을 next라는 GET 매개 변수에 담아서 사용자를 로그인 URL로 리디렉션한다.
@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',
                                                       flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
        # 장고는 일대다 관계에 대해 관계된 객체를 조회할 수 있는 select_related 라는 QuerySet 메서드를 제공한다.
        # 이렇게 하면 하나의 더 복잡한 QuerySet 으로 변환되지만 관계된 객체에 액세스할 때 추가적인 쿼리를 피할수 있다.
        # select_related을 호출하면 모든 GoreignKey 관계로부터 객체들을 조회한다. 항상 select_related의 범위를 나중에 액세스할 관계만으로 제한하는 것이 좋다.

        # select_related 메서드는 각 관계마다 별도로 조회하고 파이썬을 사용해서 결과를 조인한다. GenericRelation과 GenericForeignKey 필드에 대한 prefetch_related를 추가한다.
    actions = actions.select_related('user', 'user__profile') \
        .prefetch_related('target')[:10]
    print(actions.query)
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard',
                   'actions': actions})

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
            create_action(new_user, 'has created an account')
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


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                  'account/user/list.html',
                  {'section': 'people',
                   'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    return render(request,
                  'account/user/detail.html',
                  {'section': 'people',
                   'user': user})



@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})
