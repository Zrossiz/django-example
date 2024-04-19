from django.http import JsonResponse
from mailchimp3 import MailChimp
from django.conf import settings
from .models import CommonMailingList, CaseMailingList
from ..cases.models import Case
from typing import Optional


def add_to_common_list_view(req):
    email = req.GET.get('email')
    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    _add_email_with_tag(audience_id=settings.MAILCHIMP_COMMON_LIST_ID,
                        email=email,
                        tag='COMMON_TAG')

    CommonMailingList.objects.get_or_create(email=email)

    return JsonResponse({'success': True})


def add_to_case_list_view(req):
    email = req.GET.get('email')
    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    case_id = req.GET.get('case_id')
    if not case_id:
        return JsonResponse({'success': False, 'message': 'Передайте case_id'})

    case = Case.objects.get(pk=case_id)
    case_tag = f"Case {case.name}"

    _add_email_with_tag(audience_id=settings.MAILCHIMP_CASE_LIST_ID,
                        email=email,
                        tag=case_tag)

    CommonMailingList.objects.get_or_create(email=email, case=case)

    return JsonResponse({'success': True})


def _get_mailchimp_client() -> MailChimp:
    return MailChimp(mc_api=settings.MAILCHIMP_API_KEY, mc_user=settings.MAILCHIMP_USERNAME)


def _add_email_to_mailchimp_audience(audience_id: str, email=str) -> None:
    _get_mailchimp_client().lists.members.create(audience_id, {
        'email_address': email,
        'status': 'subscribed'
    })


def _get_mailchimp_subscriber_hash(email: str) -> Optional[str]:
    members = _get_mailchimp_client() \
        .search_members \
        .get(query=email,
             fields='exact_matches.members.id') \
        .get('exact_matches').get('members')

    if not members:
        return None
    else:
        return members[0].get('id')


def _add_mailchimp_tag(audience_id: str, subscriber_hash: str, tag: str) -> None:
    _get_mailchimp_client().lists.members.tags.update(
        list_id=audience_id,
        subscriber_hash=subscriber_hash,
        data={'tags': [{'name': tag, 'status': 'active'}]}
    )


def _add_email_with_tag(audience_id: str, email: str, tag: str) -> None:
    _add_email_to_mailchimp_audience(audience_id=settings.audience_id, email=email)

    _add_mailchimp_tag(audience_id=audience_id,
                       subscriber_hash=_get_mailchimp_subscriber_hash(email),
                       tag=tag)
