from apps.recipes.models import Tag


def tags_filter(request):
    tag_list = Tag.objects.all()
    request_copy = request.GET.copy()
    tags_off = request_copy.getlist('tags_off')
    tags_on = request_copy.getlist('tags_on')
    for item in tags_on:
        tags_off.remove(item)
    request_copy.setlist('tags_off', tags_off)
    if len(tags_on) != 0:
        request_copy.pop('tags_on')
    query = request_copy.urlencode()
    return {'tag_list': tag_list,
            'tags_off' : tags_off,
            'query' : query
            }
