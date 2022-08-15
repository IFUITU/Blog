from django.shortcuts import render
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token


from .serializers import RegisterSerializer, UserSerializer
from .tasks import send_confirmation_email
from .token import account_activation_token


@api_view(["POST"])
@permission_classes([~IsAuthenticated])
def signup(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['is_active'] = False
        user = serializer.save()
        send_confirmation_email.delay(UserSerializer(user, many=False).data)
        return Response({"data":serializer.data, "message":_('Please confirm your email address to complete the registration')}, status=status.HTTP_200_OK)
    return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class SignInOutView(APIView):
    @permission_classes([~IsAuthenticated])
    def post(self, request):
        user = authenticate(username=request.data.get("email"), password=request.data.get("password"))
        
        if user is None:
            return Response({'error':_("User or password is not valid! or Check your email for confirmation!")}, status=status.HTTP_400_BAD_REQUEST)
        token, create = Token.objects.get_or_create(user=user)
        return Response({"token":token.key, "user":{'phone':user.email,'id':user.id}}, status=status.HTTP_200_OK)
    
    @permission_classes([IsAuthenticated])
    def delete(self, request):
        if request.user.is_authenticated:
            request.auth.delete()
            return Response({"data":"Come back soon!"}, status=status.HTTP_200_OK)
        return Response({"data":"Something wrong!"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
def activate(request, uid, token):  
    User = get_user_model()  
    try:  
        user = User.objects.get(pk=uid)
        serialized_user = UserSerializer(user, many=False).data

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None
        serialized_user = None

    if user is not None and account_activation_token.check_token(serialized_user, token):  
        user.is_active = True  
        user.save()  
        return Response({'data':_('Thank you for your email confirmation. Now you can login your account.')}, status=status.HTTP_200_OK) 
    else:
        return Response({'data':_('Activation link is invalid!')}, status=status.HTTP_400_BAD_REQUEST)  