import os
import json
import requests
from pprint import pprint
from backend_router import cloudinary
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings
from PIL import Image

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
from .models import DiseaseDetection
import time


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

# ....................................................... Frontend run task ...........................................
@api_view(['POST'])
def run_task(request):
    print("Frontend triggered API received!")

    
    time.sleep(5)  
    print("Backend sleep done!")

    return Response({"status": "success", "message": "Task finished after sleep"})
# ..................................................... Frontend run task ............................................


# .......................................... DisesDetection ...................................................
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([AllowAny])
def detect_view(request):

    if "image" not in request.FILES:
        return JsonResponse({"error": "No image uploaded"}, status=400)

    try:
        image_file = request.FILES["image"]
        image_file.seek(0)

        img = Image.open(image_file).convert("RGB")

        prediction = predict_disease(img)
        print("PREDICTION:", prediction)

        image_file.seek(0)

        record = DiseaseDetection.objects.create(
    image=image_file,
    predicted_disease=prediction["class"], 
    confidence=float(prediction["confidence"])
)


        image_url = request.build_absolute_uri(record.image.url)

        return JsonResponse({
    "status": "success",
    "id": record.id,
    "disease": record.predicted_disease,   
    "confidence": round(record.confidence, 4),
    "image_name": record.image_name,
    "image_link": record.image_link,
    "import_time": record.import_time
})


    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)

# .......................................... DisesDetection ...................................................