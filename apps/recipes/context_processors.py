def tags_filter(request):
    tags = {
        'Завтрак': {
            'status': 'active',
            'link': 'Завтрак=off',
            'color': 'orange',
            'slug': 'breakfast',
        },
        'Обед': {
            'status': 'active',
            'link': 'Обед=off',
            'color': 'green',
            'slug': 'lunch',
        },
        'Ужин': {
            'status': 'active',
            'link': 'Ужин=off',
            'color': 'purple',
            'slug': 'dinner',
        }
    }
    request_get_params = request.GET.copy()
    for tag, value in tags.items():
        param = request_get_params.get(tag)
        if param == 'on':
            value['status'] = 'active'
            value['link'] = f'{tag}=off'
            request_get_params.pop(f'{tag}')
        if param == 'off':
            value['status'] = 'disable'
            value['link'] = f'{tag}=on'
    if request_get_params.__contains__('page'):
        request_get_params.pop('page')
    query_params = request_get_params.urlencode()
    return {
        'query_params': query_params,
        'tags': tags,
    }
