import peewee
from peewee import Model, EXCLUDED


class BaseModel(Model):
    def bulk_save(self, rows: list, transaction_count=10000):

        if not rows:
            return

        update_fields = self.get_excluded_fields()

        # Delete duplicates
        if self.conflict_fields:
            rows = list({''.join([str(x.get(field)) for field in self.conflict_fields]): self.match_schema(x) for x in rows}.values())

        counters = {field: 0 for field in update_fields.keys()}
        for field in update_fields:
            for row in rows:
                if field in row.keys():
                    counters[field] += 1

        for key, counter in counters.items():
            if counter == 0:
                del update_fields[key]

        if not transaction_count:
            transaction_count = len(rows)

        for index in range(0, len(rows), transaction_count):
            if self.conflict_fields and update_fields:
                self.insert_many(rows[index:index + transaction_count]).on_conflict(
                    action=None,
                    conflict_target=self.conflict_fields,
                    update=update_fields,
                ).execute()
            else:
                self.insert_many(rows[index:index + transaction_count]).on_conflict_ignore().execute()

    def save_or_update(self, row):
        row = self.match_schema(row)
        update_data = self.get_update_data(dict(row))

        if self.conflict_fields:
            self.insert(**row).on_conflict(
                action=None if update_data else 'IGNORE',
                conflict_target=self.conflict_fields,
                update=update_data,
            ).execute()
        else:
            self.insert(**row).execute()

    def match_schema(self, row: dict):
        result = {}
        schema = self.get_schema()

        for key in schema:
            if key in row:
                result[key] = row[key]

        for key in self.conflict_fields:
            if result.get(key, True) is None:
                del result[key]

        return result

    def get_update_data(self, row):
        for val in self.conflict_fields:
            if row.get(val):
                del row[val]

        return row

    def get_excluded_fields(self):
        fields = self.get_model_fields()
        indexes = self.conflict_fields
        result = {}

        fields_set = set(fields.keys())
        indexes_set = set(indexes)

        fields_without_indexes = list(fields_set - indexes_set)

        for field in fields_without_indexes:
            if isinstance(fields[field], peewee.ForeignKeyField):
                field = fields[field].object_id_name

            result[field] = getattr(EXCLUDED, field)

        return result

    # Get model fields list
    def get_schema(self):
        schema = list(self._meta.fields)

        return schema

    def get_model_fields(self):
        fields = self._meta.fields

        return fields

    @property
    def conflict_fields(self):
        # Init vars
        indexes = []

        # Get model primary key if exist
        _primary_key_field = getattr(getattr(self._meta, 'primary_key'), 'name', None)

        if self._meta.indexes:
            if self._meta.indexes[0]:
                indexes = list(self._meta.indexes[0][0])

        if not indexes:
            indexes = [_primary_key_field]

        return tuple(indexes)