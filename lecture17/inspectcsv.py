
import csv
from os.path import splitext, basename
from uuid import UUID
from collections import defaultdict
from datetime import datetime
from math import ceil

DATE_INPUT_FORMATS = ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%b %d %Y', '%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y', '%B %d, %Y', '%d %B %Y', '%d %B, %Y']

def class_decl(name):
    name, _ = splitext(basename(name))
    class_name = ''.join(map(str.capitalize, name.split('-')))
    return f'class {class_name}(models.Model):'


def simple_field(type_, field):
    def _inner(data):
        for val in data:
            type_(val)
        return field
    return _inner
    

def char_field(data):
    max_length = ceil(max(map(len, data)) * 1.25 / 10) * 10
    return f'CharField(max_length={max_length})'


def date_field(data):
    it = iter(data)
    first = next(it)
    for fmt in DATE_INPUT_FORMATS:
        try:
            datetime.strptime(first, fmt)
            break
        except:
            pass
    for val in it:
        datetime.strptime(val, fmt)
    return 'DateField()'


def gen_field(name, data):
    validators = [
        simple_field(int, 'IntegerField()'),
        simple_field(float, 'FloatField()'),
        simple_field(UUID, 'UUIDField()'),
        char_field,
    ]
    for v in validators:
        try:
            field = v(data)
            break
        except:
            pass
    indent = ' ' * 4
    print(f'{indent}{name} = model.{field}')


def gen_model(fname, col_data):
    print(f'class {fname}(model.Model):')
    for k, v in col_data.items():
        gen_field(k, v)


def process_file(fname):
    with open(fname) as csvfile:
        reader = csv.DictReader(csvfile)
        col_data = defaultdict(set)
        for row in reader:
            for k, v in row.items():
                col_data[k].add(v)
        return col_data   # {'a': set(1, 2, 3), 'b':  }


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    print(args)
    if args:
        gen_model(args[0], process_file(args[0]))
    else:
        print('Usage: inspectcsv ..')
