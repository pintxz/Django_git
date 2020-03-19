from django.shortcuts import render
import logging
logger = logging.getLogger('log')
# Create your views here.

def testhtml(request):
    logger.info('info的测试！')
    logger.error('error的测试！')
    logger.debug('debug的测试！')
    return render(request, 'test.html')
