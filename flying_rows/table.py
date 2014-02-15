from django.db.models.fields.related import ForeignKey


class Column:
    def __init__(self, name, django_field, config, frontend_validation, default_value, quick_focus):
        self.name = name
        self.django_field = django_field
        self.config = config
        self.is_foreign_key = isinstance(self.django_field, ForeignKey)
        if frontend_validation is not None:
            self.frontend_validation = frontend_validation
        if default_value is not None:
            self.default_value = default_value
        self.quick_focus = quick_focus

    def verbose_name(self):
        return self.config.get('verbose_name', self.django_field.verbose_name)


def _update_column_config_with_default_values(column_config):
    default_column = {
        'autocomplete': True,
        'editable': True,
        'weight': 1,
        'max_length': -1,
    }

    default_column.update(column_config)
    return default_column


class Config:
    pass


class Table(object):
    def __init__(self, config):
        self.config = config

        if not 'meta' in config:
            raise KeyError("No meta specified in config")
        meta = config['meta']

        if not 'model' in meta:
            raise KeyError("No model specified in config['meta']")
        if not 'table_name' in meta:
            raise KeyError("No table name specified in config['meta']")
        if not 'columns' in config:
            raise KeyError("No columns specified in config")

        self.model = meta['model']
        self.name = meta['table_name']
        self.module_name = self.model.__module__
        self.model_name = self.model.__name__

        self.config = Config()
        self.config.enable_add_new = meta.get('add_new', False)
        self.config.enable_search = meta.get('search', False)
        self.config.initial_focus = meta['initial_focus']
        self.config.autoupdate = meta.get('autoupdate', False)

        if 'search_by' in meta:
            self.config.search_by = meta['search_by']

        if 'column_ordering' in meta:
            column_ordering = meta['column_ordering']
            for column_name in config['columns']:
                if column_name not in column_ordering:
                    raise ValueError("No column " + column_name + " in config['meta']['ordering']")
        else:
            column_ordering = list(config['columns'].keys())

        self.columns_space_delimited = ' '.join(column_ordering)

        # creating columns classes for rendering
        django_fields = {field.name: field for field in self.model._meta.fields}
        self.columns = []
        for column_name in column_ordering:
            self.columns.append(Column(
                name=column_name,
                django_field=django_fields[column_name],
                config=_update_column_config_with_default_values(config['columns'].get(column_name, {})),
                frontend_validation=config['columns'].get(column_name, {}).get('frontend_validation', None),
                default_value=config['columns'].get(column_name, {}).get('default_value', None),
                quick_focus=config['columns'].get(column_name, {}).get('quick_focus', True)
            ))

        # setting width for columns
        total_weight = sum(column.config['weight'] for column in self.columns)
        for column in self.columns:
            column.width = '%.10f' % (float(column.config['weight']) / total_weight * 100) + '%'
