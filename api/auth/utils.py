from django.contrib.auth import get_user_model

User = get_user_model()

def generate_unique_username(username):
    
    base_username = username.lower().replace(" ", "")

    username = base_username
    counter = 1

    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    return username

def get_client_ip(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    
    if x_forwarded_for:

        ip = x_forwarded_for.split(',')[0]

    else:

        ip = request.META.get('REMOTE_ADDR')
    
    return ip

def get_user_agent(request):

    return request.META.get('HTTP_USER_AGENT', '')

