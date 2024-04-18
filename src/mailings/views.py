from django.http import JsonResponse
from mailchimp3 import MailChimp
from django.conf import settings
from .models import CommonMailingList, CaseMailingList
from ..cases.models import Case


def add_to_common_list_view(req):
    email = req.GET.get('email')
    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    mailchimp_client = MailChimp(mc_api=settings.MAILCHIMP_API_KEY, mc_user=settings.MAILCHIMP_USERNAME)

    mailchimp_client.lists.members.create(settings.MAILCHIMP_COMMON_LIST_ID, {
        'email_address': email,
        'status': 'subscribed'
    })
    subscriber_hash = ''

    members = mailchimp_client \
        .search_members \
        .get(query=email,
             fields='exact_matches.members.id') \
        .get('exact_matches').get('members')[0].get('id')

    mailchimp_client.lists.tags.update(list_id='', subscriber_hash='', data={})
    mailchimp_client.lists.members.tags.update(
        list_id=settings.MAILCHIMP_COMMON_LIST_ID,
        subscriber_hash=subscriber_hash,
        data={'tags': [{'name': 'COMMON_TAG', 'status': 'active'}]}
    )

    CommonMailingList.objects.get_or_create(email=email)

    return JsonResponse({'success': True})


def add_to_case_list_view(req):
    email = req.GET.get('email')
    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    case_id = req.GET.get('case_id')
    if not case_id:
        return JsonResponse({'success': False, 'message': 'Передайте case_id'})

    mailchimp_client = MailChimp(mc_api=settings.MAILCHIMP_API_KEY, mc_user=settings.MAILCHIMP_USERNAME)

    mailchimp_client.lists.members.create(settings.MAILCHIMP_CASE_LIST_ID, {
        'email_address': email,
        'status': 'subscribed'
    })
    subscriber_hash = ''

    members = mailchimp_client \
        .search_members \
        .get(query=email,
             fields='exact_matches.members.id') \
        .get('exact_matches').get('members')[0].get('id')

    mailchimp_client.lists.tags.update(list_id='', subscriber_hash='', data={})

    case = Case.objects.get(pk=case_id)
    case_tag=f"Case {case.name}"

    mailchimp_client.lists.members.tags.update(
        list_id=settings.MAILCHIMP_CASE_LIST_ID,
        subscriber_hash=subscriber_hash,
        data={'tags': [{'name': case_tag, 'status': 'active'}]}
    )

    CommonMailingList.objects.get_or_create(email=email, case=case)

    return JsonResponse({'success': True})
