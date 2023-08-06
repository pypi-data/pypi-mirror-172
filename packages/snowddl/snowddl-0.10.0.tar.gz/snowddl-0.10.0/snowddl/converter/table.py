from re import compile

from snowddl.blueprint import ObjectType
from snowddl.converter.abc_schema_object_converter import AbstractSchemaObjectConverter, ConvertResult
from snowddl.parser.table import table_json_schema


cluster_by_syntax_re = compile(r'^(\w+)?\((.*)\)$')
collate_type_syntax_re = compile(r'^(.*) COLLATE \'(.*)\'$')


class TableConverter(AbstractSchemaObjectConverter):
    def get_object_type(self) -> ObjectType:
        return ObjectType.TABLE

    def get_existing_objects_in_schema(self, schema: dict):
        existing_objects = {}

        cur = self.engine.execute_meta("SHOW TABLES IN SCHEMA {database:i}.{schema:i}", {
            "database": schema['database'],
            "schema": schema['schema'],
        })

        for r in cur:
            # Skip external tables
            if r['is_external'] == 'Y':
                continue

            full_name = f"{r['database_name']}.{r['schema_name']}.{r['name']}"
            existing_objects[full_name] = {
                "database": r['database_name'],
                "schema": r['schema_name'],
                "name": r['name'],
                "owner": r['owner'],
                "is_transient": r['kind'] == 'TRANSIENT',
                "cluster_by": r['cluster_by'] if r['cluster_by'] else None,
                "change_tracking": bool(r['change_tracking'] == 'ON'),
                "search_optimization": bool(r.get('search_optimization') == 'ON'),
                "comment": r['comment'] if r['comment'] else None,
            }

        return existing_objects

    def dump_object(self, row):
        data = {'columns': self._get_columns(row)}

        if row['is_transient']:
            data['is_transient'] = True

        if row['cluster_by']:
            data['cluster_by'] = cluster_by_syntax_re.sub(r'\2', row['cluster_by']).split(', ')

        if row['change_tracking']:
            data['change_tracking'] = True

        if row['search_optimization']:
            data['search_optimization'] = True

        data['comment'] = row['comment']

        data['primary_key'] = self._get_primary_key(row)
        data['unique_keys'] = self._get_unique_keys(row)
        data['foreign_keys'] = self._get_foreign_keys(row)

        object_path = self.base_path / self._normalise_name_with_prefix(row['database']) / self._normalise_name(row['schema']) / 'table'
        object_path.mkdir(mode=0o755, parents=True, exist_ok=True)

        if data:
            self._dump_file(object_path / f"{self._normalise_name(row['name'])}.yaml", data, table_json_schema)
            return ConvertResult.DUMP

        return ConvertResult.EMPTY

    def _get_columns(self, row):
        cols = {}

        cur = self.engine.execute_meta("DESC TABLE {database:i}.{schema:i}.{name:i}", {
            "database": row['database'],
            "schema": row['schema'],
            "name": row['name'],
        })

        for r in cur:
            m = collate_type_syntax_re.match(r['type'])

            if m:
                col = {
                    "type": m.group(1),
                    "collate": m.group(2),
                }
            else:
                col = {"type": r['type']}

            if r['null?'] == 'N':
                col['type'] = f"{col['type']} NOT NULL"

            if r['default']:
                if str(r['default']).upper().endswith('.NEXTVAL'):
                    col['default_sequence'] = self._normalise_name_with_prefix(str(r['default'])[:-8])
                else:
                    col['default'] = str(r['default'])

            if r['comment']:
                col['comment'] = r['comment']

            cols[self._normalise_name(r['name'])] = col

        return cols

    def _get_primary_key(self, row):
        constraints = {}

        cur = self.engine.execute_meta("SHOW PRIMARY KEYS IN TABLE {database:i}.{schema:i}.{name:i}", {
            "database": row['database'],
            "schema": row['schema'],
            "name": row['name'],
        })

        for r in cur:
            if r['constraint_name'] not in constraints:
                constraints[r['constraint_name']] = {}

            constraints[r['constraint_name']][r['key_sequence']] = r['column_name']

        if not constraints:
            return None

        # It is possible to have multiple PRIMARY KEYS in some cases
        # Return only the first key
        for pk in constraints.values():
            return [self._normalise_name(pk[seq]) for seq in sorted(pk)]

    def _get_unique_keys(self, row):
        constraints = {}
        unique_keys = []

        cur = self.engine.execute_meta("SHOW UNIQUE KEYS IN TABLE {database:i}.{schema:i}.{name:i}", {
            "database": row['database'],
            "schema": row['schema'],
            "name": row['name'],
        })

        for r in cur:
            if r['constraint_name'] not in constraints:
                constraints[r['constraint_name']] = {}

            constraints[r['constraint_name']][r['key_sequence']] = r['column_name']

        if not constraints:
            return None

        for uq in constraints.values():
            unique_keys.append([self._normalise_name(uq[seq]) for seq in sorted(uq)])

        return unique_keys

    def _get_foreign_keys(self, row):
        constraints = {}
        foreign_keys = []

        cur = self.engine.execute_meta("SHOW IMPORTED KEYS IN TABLE {database:i}.{schema:i}.{name:i}", {
            "database": row['database'],
            "schema": row['schema'],
            "name": row['name'],
        })

        for r in cur:
            if r['fk_name'] not in constraints:
                constraints[r['fk_name']] = {
                    "columns": {},
                    "ref_table": f"{r['pk_database_name']}.{r['pk_schema_name']}.{r['pk_table_name']}",
                    "ref_columns": {},
                }

            constraints[r['fk_name']]['columns'][r['key_sequence']] = r['fk_column_name']
            constraints[r['fk_name']]['ref_columns'][r['key_sequence']] = r['pk_column_name']

        if not constraints:
            return None

        for fk in constraints.values():
            foreign_keys.append({
                "columns": [self._normalise_name(fk['columns'][seq]) for seq in sorted(fk['columns'])],
                "ref_table": self._normalise_name_with_prefix(fk['ref_table']),
                "ref_columns": [self._normalise_name(fk['ref_columns'][seq]) for seq in sorted(fk['ref_columns'])],
            })

        return foreign_keys
