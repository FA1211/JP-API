from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class LoginVerifyView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        authenticated_user = request.user.first_name
        response_data = {"authenticated_user":authenticated_user}
        return Response(data=response_data, status=200)
