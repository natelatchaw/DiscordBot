class WhereClause():
    
    def __init__(self, column_name: str, value: object):
        self._column_name: str = column_name
        self._value: object = value