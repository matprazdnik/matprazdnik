from django.db.models.fields.related import ForeignKey


class Column:
    def __init__(self, name, django_field, config, frontend_validation):
        self.name = name
        self.django_field = django_field
        self.config = config
        self.is_foreign_key = isinstance(self.django_field, ForeignKey)
        if frontend_validation is not None:
            self.frontend_validation = frontend_validation

    def verbose_name(self):
        return self.config.get('verbose_name', self.django_field.verbose_name)


def _update_column_config_with_default_values(column_config):
    default_column = {
        'autocomplete': True,
        'editable': True,
        'weight': 1,
        }

    default_column.update(column_config)
    return default_column


class Table(object):
    def __init__(self, config):
        self.config = config
        if not 'meta' in config:
            raise KeyError("No meta specified in config")
        if not 'model' in config['meta']:
            raise KeyError("No model specified in config['meta']")
        if not 'columns' in config:
            raise KeyError("No columns specified in config")

        self.model = config['meta']['model']
        self.module_name = self.model.__module__
        self.model_name = self.model.__name__
        self.columns = []

        class Config:
            pass

        self.config = Config();
        self.config.enable_add_new = config['meta'].get('add_new', False)
        self.config.enable_search = config['meta'].get('search', False)
        self.config.initial_focus = config['meta']['initial_focus']
        self.config.autoupdate = config['meta'].get('autoupdate', False)
        try:
            self.config.search_by = config['meta']['search_by']
        except:
            pass

        if 'column_ordering' in config['meta']:
            column_ordering = config['meta']['column_ordering']
            for column_name in config['columns']:
                if column_name not in column_ordering:
                    raise Exception("No column " + column_name + " in ordering") # TODO: update with correct exception
        else:
            column_ordering = list(config['columns'].keys())

        self.columns_space_delimited = ' '.join(column_ordering)

        # creating columns classes for rendering
        django_fields = {field.name: field for field in self.model._meta.fields}
        for column_name in column_ordering:
            self.columns.append(Column(name=column_name,
                    django_field=django_fields[column_name],
                    config=_update_column_config_with_default_values(config['columns'].get(column_name, {})),
                    frontend_validation=config['columns'].get(column_name, {}).get('frontend_validation', None)))

        # setting width for columns
        total_weight = sum(column.config['weight'] for column in self.columns)
        for column in self.columns:
            column.width = '%.10f' % (float(column.config['weight']) / total_weight * 100) + '%'