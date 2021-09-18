from apps.recipes.models import Tag


def tags_filter(request):
    tags = {}
    for tag in Tag.objects.all():
        tags[tag.title] = {
            'status': 'active',
            'link': f'{tag.slug}=disable',
            'color': tag.color,
            'slug': tag.slug
        }
    request_params = request.GET.copy()
    count_of_disabled_tags = 0
    for tag, value in tags.items():
        if count_of_disabled_tags < 2:
            param = request_params.get(value['slug'])
            if param == 'disable':
                value['status'] = 'disable'
                value['link'] = f"{value['slug']}=active"
                count_of_disabled_tags += 1
    if request_params.get('page'):
        request_params.pop('page')
    query_params = request_params.urlencode()
    return {
        'query_params': query_params,
        'tags': tags,
        'count_of_disabled_tags': count_of_disabled_tags,
    }
