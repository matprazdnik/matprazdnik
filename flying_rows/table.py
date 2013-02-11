class Field(object):
    def __init__(self, name, value, editable=False):
        self.name = name
        self.value = value
        self.editable = editable

    def id(self):
        return 'cell' + self.row_id + self.name

class Table(object):
    def __init__(self, config):
        self.__config__ = config
        if not 'meta' in config:
            raise Exception("No meta specified in config") # TODO: update with correct exception
        if not 'model' in config['meta']:
            raise Exception("No model specified in config['meta']") # TODO: update with correct exception
        if not 'columns' in config:
            raise Exception("No columns specified in config") # TODO: update with correct exception
        self.model = config['meta']['model']
        self.columns = []
        # creating dict for field names
        field_names = {}
        for field in self.model._meta.fields:
            field_names[field.name] = field
        if 'column_ordering' in config['meta']:
            column_ordering = config['meta']['column_ordering']
            for column_name in config['columns']:
                if column_name not in column_ordering:
                    raise Exception("No column " + column_name + " in ordering") # TODO: update with correct exception
        else:
            column_ordering = list(config['columns'])
        # creating columns classes for rendering
        for column_name in column_ordering:
            if column_name in config['columns']:
                if not column_name in field_names:
                    raise Exception("No field for " + column_name + " column") # TODO: update with correct exception
                class Column:
                    def __init__(self, column_name):
                        self.column_name = column_name
                    def name(self):
                        if 'verbose_name' in config['columns'][self.column_name]:
                            return config['columns'][self.column_name]['verbose_name']
                        return field_names[self.column_name].verbose_name

                self.columns.append(Column(column_name))
        # creating data
        objects = self.model.objects.all() # get objects
        if 'sort_by' in config['meta']:
            objects = objects.order_by(*config['meta']['sort_by']) # sort if need
        is_editable_getter = lambda config: config['editable'] if 'editable' in config else False
        class Row:
            def __init__(self, object):
                self.id = object.id
                self.fields = [ Field(column_name, object.__getattribute__(column_name), is_editable_getter(config['columns'][column_name])) for column_name in column_ordering]
                for field in self.fields:
                    field.row_id = str(self.id)

        self.data = [ Row(object) for object in objects ]

    def update_url(self):
        return self.__config__['meta']['update-url']