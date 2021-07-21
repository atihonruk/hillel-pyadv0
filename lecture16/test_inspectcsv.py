import pytest
import inspectcsv as isc


def test_class_decl_success():
    inp = 'legal-entity'
    res = isc.class_decl(inp)
    assert res == 'class LegalEntity(models.Model):', f'Input is not valid: {inp}'

@pytest.mark.xfail    
def test_class_decl_subscript():
    inp = 'legal_entity.csv'
    res = isc.class_decl(inp)
    assert res == 'class LegalEntity(models.Model):'

@pytest.mark.skip
def test_class_decl_digit():
    inp = '123legal_entity.csv'
    res = isc.class_decl(inp)
    assert res == 'class LegalEntity(models.Model):'


def test_char_length():
    data = ['asdf']
    res = isc.char_field(data)
    assert res == 'CharField(max_length=10)'


def test_simple_field_int():
    fn = isc.simple_field(int, 'IntegerField()')
    res = fn([1, 2, 3])
    assert res == 'IntegerField()'


def test_simple_field_int_fail():
    fn = isc.simple_field(int, 'IntegerField()')
    with pytest.raises(ValueError):
        res = fn([1, 2, 'str'])
        # assert res == 'IntegerField()'
