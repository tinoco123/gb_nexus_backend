from django.shortcuts import redirect


def terms_accepted_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.terms_accepted:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('terms_conditions')
    return wrapper
