from django.http import JsonResponse

def handler404(request, exception):
    message = ('Path not found')
    response = JsonResponse(date = {'error':message})
    response.status_code = 404
    return response

    