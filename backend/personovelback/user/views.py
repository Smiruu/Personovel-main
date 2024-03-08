from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserPasswordResetSerializer, UserRegistrationSerializers, UserLoginSerializer, UserProfileSerializer
from django.contrib.auth import authenticate
from user.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken, Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.decorators import api_view

# Generate token Manually
def get_tokens_for_user(user):
    # Generate refresh token
    refresh = RefreshToken.for_user(user)

    # Include user's name and email in the token payload
    access_token_payload = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user_id': user.id,
        'name': user.name,  # Assuming 'name' is a field in your user model
        'email': user.email  # Assuming 'email' is a field in your user model
    }

    return access_token_payload

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg':'Register Succcess'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token,'msg':'Login Succcess'}, status=status.HTTP_200_OK)
            else: 
                return Response({'errors':{'non_field_errors':['Email or Password is not valid']}}, status=status.HTTP_400_BAD_REQUEST)

# class UserProfileView(APIView):
#     renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         serializer= UserProfileSerializer(request.user)
#         return Response(serializer.data, status=status.HTTP_200_OK)

from .models import User
@api_view(['GET'])
def get_user_profile(request, pk):
    print(pk)
    user = User.objects.get(id=pk)
    print(user)
    user_profile = UserProfile.objects.get(user=user)
    serializer = UserProfileSerializer(user_profile, many=False)
    print(serializer.data)
    return Response(serializer.data)
    

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        context = {'user': request.user}
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Change Password Succcessfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request, uid, token , format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context = {'uid':uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':"Password Reset Succesfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    