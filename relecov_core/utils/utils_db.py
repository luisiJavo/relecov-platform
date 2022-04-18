from ..models import *

def get_variant_records():
    variants = Variant.objects.all()
    for variant in variants:
        print(variant.pos)