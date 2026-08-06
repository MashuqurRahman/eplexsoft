import requests
from django.conf import settings

def create_support_ticket(cleaned_data,request):

    headers = {
        "X-API-KEY": settings.SUPPORT_API_KEY
    }

    data = {
        "name":  request.user.name,
        "enlisted_email": request.user.email,
        "contact_no": request.user.phone,
        "business_name": request.user.user_company,
        "problem_statement": cleaned_data["problem_statement"],
    }

    files = {}

    attachment = cleaned_data.get("attachment")

    if attachment:
        files["attachment"] = (
            attachment.name,
            attachment.file,
            attachment.content_type
        )

    response = requests.post(
        settings.SUPPORT_SERVER,
        headers=headers,
        data=data,
        files=files if files else None,
        timeout=30
    )

    return response


def get_my_supports(email):

    headers = {
        "X-API-KEY": settings.SUPPORT_API_KEY
    }

    response = requests.get(
        settings.SUPPORT_LIST_API,
        headers=headers,
        params={
            "email": email
        }
    )

    return response

def get_support_details(support_id):

    headers = {
        "X-API-KEY": settings.SUPPORT_API_KEY
    }

    response = requests.get(
        f"{settings.SUPPORT_DETAIL_API}{support_id}/",
        headers=headers
    )

    return response


def create_support_reply(support_id, data, files=None):

    headers = {
        "X-API-KEY": settings.SUPPORT_API_KEY
    }

    response = requests.post(
        f"{settings.SUPPORT_REPLY_API}{support_id}/",
        headers=headers,
        data=data,
        files=files
    )

    return response