import os
import json
import requests
from pprint import pprint
from backend_router import cloudinary
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
import google.generativeai as genai
from PIL import Image
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from backend_router.MLModel.MLapp import predict_disease
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from PIL import Image
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



# ...................................................... Secure key ...................................................
secure = os.getenv('SECURE')
     
cloudinary.config( 
    cloud_name = "dsktyutef", 
    api_key = "264461953814364", 
    api_secret = "H6nmg4inVdwYmbE9cVKMPrT-8gM", 
    secure=True
)
# ...................................................... Secure key ...................................................

# ...................................................... For start ....................................................
def home(request):
    return JsonResponse({"status": "Backend is running 🚀"})
# ...................................................... For start ....................................................


# .......................................... DisesDetection ...................................................
@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([AllowAny])
def detect_view(request):
    """
    API endpoint: POST an image file -> get prediction.
    """
    if request.method == "POST" and request.FILES.get("file"):
        try:
            file = request.FILES["file"]

            img = Image.open(file).convert("RGB")  


            prediction = predict_disease(img)

            return JsonResponse({
                "status": "success",
                "prediction": prediction["class"],
                "confidence": round(prediction["confidence"], 4)
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "No file uploaded"}, status=400)
    
# .......................................... DisesDetection ...................................................