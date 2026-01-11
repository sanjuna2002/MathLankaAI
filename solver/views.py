from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .gemini import extract_math_from_image

from .gemini import (
    solve_math_explain,
    solve_math_direct,
    extract_math_from_image
)

def home(request):
    question = ""
    answer = None

    if request.method == "POST":
        question = request.POST.get("question", "")

        if "explain" in request.POST:
            answer = solve_math_explain(question)
        elif "direct" in request.POST:
            answer = solve_math_direct(question)

    return render(request, "solver/home.html", {
        "question": question,
        "answer": answer
    })


@csrf_exempt
def extract_math(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            image_data = data.get("image")

            # Remove base64 header
            header, encoded = image_data.split(",", 1)
            image_bytes = base64.b64decode(encoded)

            question = extract_math_from_image(image_bytes)

            return JsonResponse({"question": question})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
