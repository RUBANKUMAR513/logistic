
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from EmailConfiguration.msg import process  # Adjust the import based on your project structure


def send_otp(request):
    if request.method == "POST":
        try:
            print("message received")
            data = json.loads(request.body)

            name = data.get("name")
            email = data.get("email")
            subject = data.get("subject")
            message = data.get("message")

            # Example: trigger process
            process(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            return JsonResponse({
                "status": "success",
                "message": "Your message has been sent successfully!"
            })

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)

    return JsonResponse({
        "status": "error",
        "message": "Only POST method allowed"
    }, status=405)