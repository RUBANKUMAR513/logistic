
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from EmailConfiguration.msg import process  # Adjust the import based on your project structure


@csrf_exempt  # Use this only if CSRF protection is not needed (not recommended for production)
def send_otp(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data
            data = json.loads(request.body)
            message = data.get('message', '')

            # Check for the specific message to trigger the OTP process
            if message == 'admin trigger otp':
                process()  # Call your process function to send the OTP
                return JsonResponse({'status': 'success', 'message': 'OTP sent successfully.'})

            return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)