class ForeignKey(Field):
    def __init__(self, to, **kwargs):
        super().__init__("INTEGER", **kwargs)
        self.to = to

class ManyToManyField(Field):
    def __init__(self, to, **kwargs):
        super().__init__("MANYTOMANY", **kwargs)
        self.to = to

class Model(metaclass=ModelMeta):
    # ... previous code ...
    @classmethod
    def create_table(cls, conn):
        cols = []
        for name, field in cls._fields.items():
            col = f"{name} {field.column_type}"
            if field.primary_key:
                col += " PRIMARY KEY"
            elif isinstance(field, ForeignKey):
                col += f" REFERENCES {field.to.__name__.lower()}(id)"
            cols.append(col)
        q = f"CREATE TABLE IF NOT EXISTS {cls.__name__.lower()} ({', '.join(cols)});"
        cur = conn.cursor()
        cur.execute(q)
        conn.commit()
        # ManyToMany: create join tables
        for name, field in cls._fields.items():
            if isinstance(field, ManyToManyField):
                join_table = f"{cls.__name__.lower()}_{field.to.__name__.lower()}"
                qj = f"CREATE TABLE IF NOT EXISTS {join_table} ({cls.__name__.lower()}_id INTEGER, {field.to.__name__.lower()}_id INTEGER)"
                cur.execute(qj)
        conn.commit()