# breadcrumbs/context_processors.py
def breadcrumb(request):
    breadcrumb = []

    if hasattr(request, 'breadcrumb'):
        breadcrumb = request.breadcrumb

    return {'breadcrumb': breadcrumb}
