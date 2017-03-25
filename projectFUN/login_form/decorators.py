from django.shortcuts import redirect

from login_form.models import User


def annon_required(redirect_url=None):
    if redirect_url is None:
        return redirect('/')

    def annon_requiredd(func):
        def decorated(request, *args, **kwargs):
            if 'email' in request.session.keys():
                return redirect(redirect_url)
            return func(request, *args, **kwargs)
        return decorated
    return annon_requiredd


def logout(request, redirect_url):
    u = User.objects.filter(email=request.session['email']).first()
    u.is_active = False
    u.save()
    try:
        del request.session['email']
    except KeyError:
        pass
    return redirect(redirect_url)


def login_required(redirect_url=None):
    if redirect_url is None:
        return redirect('/')

    def login_requiredd(func):
        def decorated(request, *args, **kwargs):
            if 'email' not in request.session.keys():
                return redirect(redirect_url)
            if request.method == 'POST':
                return logout(request, redirect_url)
            return func(request, *args, **kwargs)
        return decorated
    return login_requiredd
