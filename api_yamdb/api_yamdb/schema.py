from django.shortcuts import render
from rest_framework.schemas.openapi import SchemaGenerator


def schema(request):
    """Этот код вам не пригодится, но и удалять его не стоит."""
    generator = SchemaGenerator(title='Yandex Praktikum')
    getted_schema = generator.get_schema() or {
        'info': {'title': 'Yandex Praktikum'}, 'paths': {}
    }

    getted_schema['paths']['api/v1/posts/{id}/'] = {
        'get': {'description': '',
                'operationId': 'retrieveapi_posts_detail',
                'parameters': [],
                'responses': {
                    '200': {
                        'content': {'application/json': {
                            'schema': {'items': {}, 'type': 'array'}
                        }},
                        'description': ''
                    }
                },
                'tags': ['api']
                }
    }
    schema = {
        'title': getted_schema['info']['title'],
        'endpoints': []
    }
    for path in getted_schema['paths']:
        for method in getted_schema['paths'][path].keys():
            operationId = getted_schema['paths'][path][method]['operationId']
            schema['endpoints'].append(
                {'path': path, 'method': method, 'operationId': operationId}
            )

    return render(request, 'index.html', {'schema': schema})
