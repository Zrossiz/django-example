from mailings.mailchimp_services import add_email_with_tag
from mailings.models import CommonMailingList, CaseMailingList
from cases.models import Case
from typing import Union


def add_email_to_common_mailchimp_list(email: str):
    add_email_with_tag(audience_name='COMMON',
                       email=email,
                       tag='COMMON_TAG')

    CommonMailingList.objects.get_or_create(email=email)


def add_email_to_case_mailchimp_list(email: str, case_id: Union[int, str]):
    case = Case.objects.get(pk=case_id)
    add_email_with_tag(audience_name='CASES',
                       email=email,
                       tag=f"Case {case.name}")

    CaseMailingList.objects.get_or_create(email=email, case=case)