import time
from django.contrib.auth import logout
from django.shortcuts import redirect

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = int(time.time())
            timeout = 900 # 15 minutos de inactividad

            last_activity = request.session.get('last_activity', now)
            if now - last_activity > timeout:
                logout(request)
                request.session.flush()
                request.session['session_expired'] = True
                return redirect('sign_in')

            request.session['last_activity'] = now

        return self.get_response(request)