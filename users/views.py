from rest_framework import generics
from .models import User
from .serializers import UserSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Ограничить доступ к профилю только для текущего пользователя
    def get_object(self):
        return self.request.user
