from django.core.management import execute_from_command_line
from django.db import connection
from django.shortcuts import render
from django.urls import path

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

DEBUG = True
ROOT_URLCONF = __name__
SECRET_KEY = 'secret'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [''],
    }
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'immunization.sqlite3'
    }
}


def index(request):
    default_region = 'М.КИЇВ'
    region = request.GET.get('region', default_region)

    query_all_regions = '''
    select registration_area, count(*)
    from legal_entities_info
    group by registration_area;
    '''
    with connection.cursor() as cur:
        cur.execute(query_all_regions)
        reg_counts = cur.fetchall()
    
    query_region = '''
    select legal_entity_id, legal_entity_name
    from legal_entities_info
    where registration_area=%s;
    '''
    with connection.cursor() as cur:
        cur.execute(query_region, [region])
        reg_data = cur.fetchall()

    return render(request, 'index.html', {'reg_data': reg_data,
                                          'reg_counts': reg_counts,
                                          'region': region})


def entity_by_id(request, id_):
    query = 'select * from legal_entities_info where legal_entity_id=%s'
    with connection.cursor() as cur:
        cur.execute(query, [id_])
        print(cur.description)
        data = dict(zip((col[0] for col in cur.description), cur.fetchone()))
    return render(request, 'entity.html', {'data': data})


urlpatterns = [
    path('', index, name='index'),
    path('entity/<id_>', entity_by_id, name='entity-by-id'),
]


if __name__ == '__main__':
    execute_from_command_line()
