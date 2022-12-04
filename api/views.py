from django.db import IntegrityError
from django.conf import settings
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseNotFound, HttpResponseServerError
from .utils import generate_key
from .validations import NewUrlValidation
from .models import Url
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create_url(req):
    if req.method != 'POST':
        return HttpResponseNotFound()

    if not req.body:
        return HttpResponseBadRequest('missing data')

    data = json.loads(req.body.decode())

    data_validations = NewUrlValidation(data)
    if not data_validations.is_valid():
        return HttpResponseBadRequest('missing or invalid data')

    url = data['url']

    for _ in range(settings.KEY_CREATION_MAX_RETRIES):
        try:
            key = generate_key(settings.URL_KEY_LENGTH)

            # we can not have empty string as key, but it not an error
            # can happend if url key length is 0
            if not key:
                continue

            new_url = Url(url=url, key=key)
            new_url.save()
            dict_obj = model_to_dict(new_url)
            res = JsonResponse(dict_obj)
            res.status_code = 201
            return res
        except IntegrityError:
            pass

    return HttpResponseServerError("couldn't creat unique key")


def redirect_url(req, key):
    if req.method != 'GET':
        return HttpResponseNotFound()

    try:
        target_url = Url.objects.get(key=key)
        target_url.redirects_count += 1
        target_url.save()
        return HttpResponseRedirect(target_url.url)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest('key not exist')


def get_key_data(req, key):
    if req.method != 'GET':
        return HttpResponseNotFound()

    try:
        url = Url.objects.get(key=key)
        return JsonResponse(model_to_dict(url))
    except Exception as e:
        print(e)
        return HttpResponseBadRequest('key not exist')
