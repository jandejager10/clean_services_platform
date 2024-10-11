import json
from django.core.serializers.json import DjangoJSONEncoder
from decimal import Decimal

class DecimalEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)

class DecimalSerializer:
    def dumps(self, obj):
        return json.dumps(obj, cls=DecimalEncoder).encode('utf-8')

    def loads(self, data):
        return json.loads(data.decode('utf-8'))
