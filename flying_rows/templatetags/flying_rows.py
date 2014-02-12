from django import template
from django.template import Node, TemplateSyntaxError, loader, Context
from flying_rows.table import Table


register = template.Library()


def _update_table_config_with_default_values(table_config):
    default_meta = {
        'sort_by': ('-id',),
        'after_save_focus': 'search',  # choices: add_new, search
        'enable_search': True,
        'enable_add_new': True,
    }
    default_meta.update(table_config['meta'])
    table_config['meta'] = default_meta
    return table_config


class RenderTableNode(Node):
    def __init__(self, table_config_var_name):
        self.table_config_var_name = table_config_var_name

    def render(self, context):
        table_config = _update_table_config_with_default_values(context[self.table_config_var_name])
        table = Table(table_config)
        t = loader.get_template('main.html')
        c = Context({'context': context, 'table': table})
        return t.render(c)


@register.tag('render_table')
def render_table(parser, token):
    try:
        tag_name, table_config_var_name = token.split_contents()
    except ValueError:
        msg = '{0} tag requires a single argument'.format(token.split_contents()[0])
        raise TemplateSyntaxError(msg)
    return RenderTableNode(table_config_var_name)
