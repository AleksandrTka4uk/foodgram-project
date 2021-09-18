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
    for tag, value in tags.items():
        param = request_params.get(value['slug'], 'active')
        if param != 'active':
            value['status'] = 'disable'
            value['link'] = f"{value['slug']}=active"
    if request_params.get('page'):
        request_params.pop('page')
    query_params = request_params.urlencode()
    return {
        'query_params': query_params,
        'tags': tags,
    }
