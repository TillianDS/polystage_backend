from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def user_profile(request):
    attributes = request.session.get('attributes', {})
    return render(request, 'user_profile.html', {
        'user': request.user,
        'attributes': attributes,
    })
