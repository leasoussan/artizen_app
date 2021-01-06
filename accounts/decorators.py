# this function is to make sure that if there is no Proflie >.send to make one
# all decorator return True /False 
from artists.models import Profile

def check_profile(user):
    return Profile.objects.filter(user=user).exists()
