from django.http import JsonResponse
from .services import add_email_to_common_mailchimp_list, add_email_to_case_mailchimp_list
from django.conf import settings


def test(req):
    return JsonResponse({'success': settings.MY_API_KEY})


def add_to_common_list_view(req):
    email = req.GET.get('email')
    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    add_email_to_common_mailchimp_list(email=email)

    return JsonResponse({'success': True})


def add_to_case_list_view(req):
    email = req.GET.get('email')
    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    case_id = req.GET.get('case_id')
    if not case_id:
        return JsonResponse({'success': False, 'message': 'Передайте case_id'})

    add_email_to_case_mailchimp_list(email=email, case_id=case_id)

    return JsonResponse({'success': True})

