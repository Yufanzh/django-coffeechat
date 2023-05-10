class HBaseField:
    field_type = None

    def __init__(self, reverse=False, column_family=None):
        self.reverse = reverse
        self.column_family = column_family

class IntegerField(HBaseField):
    field_type = 'int'

    def __init__(self, *args, **kwargs):
        super(IntegerField, self).__init__(*args, **kwargs)

class TimestampField(HBaseField):
    field_type = 'timestamp'

    def __init__(self, *args, auto_now_add=False, **kwargs):
        super(TimestampField, self).__init__( *args, **kwargs)