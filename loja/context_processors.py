'''
Módulo para utilitários de contexto.
'''


def site_title(request):  # pylint: disable=W0613
    '''
    Contexto Processor para definir o nome do site
    '''
    return {
        'site_title': 'LinkBuy'
    }
