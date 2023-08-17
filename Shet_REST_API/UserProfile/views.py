from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
import io 
from rest_framework.parsers import JSONParser
from .models import UserProfile
from .serializers import UserProfileSer, SignUpSer
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from django.views.decorators.http import require_POST
# Create your views here.
def GetCSRF(request):
    response = JsonResponse({"Info": "Set CSRFToken"})
    response["X-CSRFToken"] = get_token(request)
    return response

class UserProfileVS(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSer

@require_POST 
def SignUp(request):
    if request.method == 'POST':
        FormData = request.body
        stream = io.BytesIO(FormData)
        PythonData = JSONParser().parse(stream)
        serializer = SignUpSer(data=PythonData)
        if serializer.is_valid():
            serializer.save()
            email = PythonData.get('email')
            User = UserProfile.objects.get(email=email)
            login(request, User)
            serializer = UserProfileSer(User, context={"request": request})
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors)

@require_POST           
def LogIn(request):
    FormData = request.body
    stream = io.BytesIO(FormData)
    PythonData = JSONParser().parse(stream)
    Email = PythonData.get('email') 
    PassWord = PythonData.get('password')
    print(Email, PassWord)
    try:
        user = authenticate(username=Email, password=PassWord)
    except UserProfile.DoesNotExist:
        return HttpResponse('Account Does Not Exist!')    
    if user is not None:
        login(request, user)
        serializer = UserProfileSer(user, context={"request": request})
        return JsonResponse(serializer.data)
    else:
        return HttpResponse("Invalid Credentials!")

@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])    
def LogOut(request):
    logout(request)
    return JsonResponse({"Msg":"Logged Out!"})
