
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from EmailConfiguration.msg import process  # Adjust the import based on your project structure



def send_otp(request):
    if request.method == "POST":
        try:
            print("📩 Contact message received")

            data = json.loads(request.body)

            name = data.get("name")
            email = data.get("email")
            company = data.get("company")
            contact_number = data.get("contact_number")
            service_type = data.get("service_type")
            message = data.get("message")

            # Optional validation
            if not all([name, email, company, contact_number, service_type, message]):
                return JsonResponse({
                    "status": "error",
                    "message": "All fields are required"
                }, status=400)

            # Trigger your process (email / save DB / automation)
            process(
                name=name,
                email=email,
                company=company,
                contact_number=contact_number,
                service_type=service_type,
                message=message
            )

            return JsonResponse({
                "status": "success",
                "message": "Your message has been sent successfully!"
            })

        except json.JSONDecodeError:
            return JsonResponse({
                "status": "error",
                "message": "Invalid JSON data"
            }, status=400)

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)

    return JsonResponse({
        "status": "error",
        "message": "Only POST method allowed"
    }, status=405)
