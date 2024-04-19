from src.mailings.mailchimp_services import add_email_with_tag


def webhook(req):
    add_email_with_tag(email=req.POST.get('email'),
                       audience_name='DONATES',
                       tag='DONATES')
