from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache


@never_cache
def login(request):
    redirect_to = request.GET.get('next', reverse('index'))
    url_is_safe = is_safe_url(
        url=redirect_to,
        allowed_hosts=[request.get_host()],
        require_https=True,
    )
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(
            request,
            template_name='login.html',
            context={
                'next': redirect_to if url_is_safe else '',
            }
        )


@never_cache
def logout_view(request):
    logout(request)
    return redirect('/')
