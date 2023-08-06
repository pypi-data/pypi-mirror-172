import pytest
from metagen import PTRMetagen
from metagen import LayerTemplate


def test_gen_get_types():
    gen = PTRMetagen()
    lt1 = LayerTemplate(applicationKey='app', nameInternal=f'lt', nameDisplay='lt')
    lt2 = LayerTemplate(applicationKey='app', nameInternal=f'lt', nameDisplay='lt')
    lts = gen.get_elements_by_type(LayerTemplate)