from django_redis import get_redis_connection
from unidecode import unidecode



KBD_LAYOUT = {
    'en': 'abcdefghijklmnopqrstuvwxyz[];\',.ABCDEFGHIJKLMNOPQRSTUVWXYZ{}:"<>`~@#$^&',
    'ru': 'фисвуапршолдьтщзйкыегмцчняхъжэбюФИСВУАПРШОЛДЬТЩЗЙКЫЕГМЦЧНЯХЪЖЭБЮёЁ"№;:?',
    'uk': 'фисвуапршолдьтщзйкіегмцчняхїжєбюФИСВУАПРШОЛДЬТЩЗЙКІЕГМЦЧНЯХЇЖЄБЮ\'₴"№;:?'
}

# {'en': [...]
#  ''}

TRANS_LANGS = KBD_LAYOUT.keys()

TRANSLATIONS = {lang1: [''.maketrans(KBD_LAYOUT[lang1], KBD_LAYOUT[lang2])
                        for lang2 in TRANS_LANGS if lang1 != lang2]
                for lang1 in TRANS_LANGS}

SEPARATOR = ':'


def make_completion_key(cls, field_name):
    full_name = '.'.join([cls.__module__, cls.__name__, field_name])
    return f'autocomplete:{full_name}'


def make_field_completions(obj, field_name):
    values = set()
    val = obj.__dict__[field_name]
    if val:
        val = val.lower()
        values.add(val)  # original value
        values.add(unidecode(val)) # transliterated
        for lang in TRANSLATIONS:
            values.update([val.translate(t) for t in TRANSLATIONS[lang]])
    return values
        

def model_completions(cls, field_name):
    """ Make all possible completions of the model data """

    key = make_completion_key(cls, field_name)
    completions = []
    for obj in cls.objects.all():  # Book.objects.all()
        for compl in make_field_completions(obj, field_name):
            # completions.append(0.0)
            completions.append(SEPARATOR.join((compl, str(obj.id))))
    con = get_redis_connection()
    con.zremrangebyrank(key, 0, -1) # remove all old data
    con.zadd(key, {k:0.0 for k in completions})
    return completions


def get_completion(cls, field_name, term, min_length=1):
    key = make_completion_key(cls, field_name)
    if term and len(term) > min_length:
        con = get_redis_connection()
        term = '[' + term
        term = term.encode('utf-8')
        str_id_list = con.zrangebylex(key, term, term + b'\xff')
        return set([val.decode('utf-8').split(':', 1)[1] for val in str_id_list])
    return set()
