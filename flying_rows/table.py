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
        self.add_new_enabled = config['meta']['add-new-enabled'] if 'add-new-enabled' in config['meta'] else True
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
                    def __init__(self, name):
                        self.name = name
                        self.weight = config['columns'][name]['weight'] if 'weight' in config['columns'][name] else 1
                        self.editable = config['columns'][name]['editable'] if 'editable' in config['columns'][name] else False
                    def verbose_name(self):
                        if 'verbose_name' in config['columns'][self.name]:
                            return config['columns'][self.name]['verbose_name']
                        return field_names[self.name].verbose_name
                    def input_id(self):
                        return 'input_field_' + self.name


                self.columns.append(Column(column_name))
        self.reversed_columns = list(reversed(self.columns))
        # setting next for columns
        for i in range(1, len(self.columns)):
            self.columns[i-1].next = self.columns[i]
        # setting width for columns
        total_weight = sum([ column.weight for column in self.columns ])
        for column in self.columns:
            column.width = '%.10f' % (float(column.weight) / total_weight * 100) + '%'
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
                last_editable = None
                for i in reversed(range(len(self.fields))):
                    if last_editable is not None:
                        self.fields[i].next = last_editable
                    if self.fields[i].editable:
                        last_editable = self.fields[i]

        self.data = [ Row(object) for object in objects ]

    def update_url(self):
        return self.__config__['meta']['update-url']

    def add_url(self):
        return self.__config__['meta']['add-url']

    def get_new_url(self):
        return self.__config__['meta']['get-new-url']

    def initial_focus(self):
        return self.__config__['meta']['initial_focus']
