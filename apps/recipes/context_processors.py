from apps.recipes.models import Tag


def tags_filter(request):
    tag_list = Tag.objects.all()
    request_get_params = request.GET.copy()
    tags_off = request_get_params.getlist('tags_off')
    tags_off_count = len(tags_off)
    if tags_off_count == 3:
        tags_off = tags_off[:2]
    tags_on = request_get_params.getlist('tags_on')
    for item in tags_on:
        tags_off.remove(item)
    request_get_params.setlist('tags_off', tags_off)
    if tags_on:
        request_get_params.pop('tags_on')
    if request_get_params.__contains__('page'):
        request_get_params.pop('page')
    query_params = request_get_params.urlencode()
    return {'tag_list': tag_list,
            'tags_off': tags_off,
            'query_params': query_params,
            'tags_off_count': tags_off_count
            }
