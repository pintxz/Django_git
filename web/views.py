from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json, logging

logger = logging.getLogger('log')


# Create your views here.

@require_http_methods(["GET"])
def testhtml(request):
    logger.info('info的测试！')
    logger.error('error的测试！')
    logger.debug('debug的测试！')
    return render(request, 'test.html')


@require_http_methods(["GET"])
def add_book(request):
    response = {}
    try:
        book = Book(book_name=request.GET.get('book_name'))
        book.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
