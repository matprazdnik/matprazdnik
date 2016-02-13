import json
from django import template
from django.template import Node, TemplateSyntaxError, loader, Context
from django.utils.safestring import mark_safe
from flying_rows.models import Transaction
from flying_rows.table import Table
from flying_rows.utils import get_table_data


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

def create_table_config_for_client(table_config):
    return json.dumps([
        {
            "name": column_name,
            "display_name": table_config['columns'][column_name]['display_name'],
            "weight": table_config['columns'][column_name].get('weight', 1),
            "default_value": table_config['columns'][column_name].get('default_value', ''),
            "one_char_field": table_config['columns'][column_name].get('one_char_field', False),
        } for column_name in table_config['meta']['column_ordering']
    ])

class RenderTableNode(Node):
    def __init__(self, table_config_var_name):
        self.table_config_var_name = table_config_var_name

    def render(self, context):
        table_config = _update_table_config_with_default_values(context[self.table_config_var_name])
        table = Table(table_config)
        t = loader.get_template('table.html')

        transactions = list(Transaction.objects.all())
        if len(transactions) == 0:
            last_transaction_id = -1
        else:
            last_transaction_id = max(x.id for x in transactions)

        c = Context({
            'context': context,
            'table': table,
            'table_data': mark_safe(get_table_data(table_config)),
            'table_columns_config': mark_safe(create_table_config_for_client(table_config)),
            'last_transaction_id': last_transaction_id,
            'table_name': table_config['meta']['table_name'],
            'search_fields': mark_safe(json.dumps(table_config['meta']['search_by'])),
            'focus_policy_after_add': table_config['meta'].get('focus_after_add', ''),
            'focus_policy_after_change': table_config['meta'].get('focus_after_change', ''),
            'enable_add_new': json.dumps(table_config['meta']['add_new']),
            'selectable_rows': json.dumps(table_config['meta'].get('selectable_rows', False)),
            'initial_focus_after_search': table_config['meta'].get('initial_focus', '')
        })
        return t.render(c)


@register.tag('render_table')
def render_table(parser, token):
    try:
        tag_name, table_config_var_name = token.split_contents()
    except ValueError:
        msg = '{0} tag requires a single argument'.format(token.split_contents()[0])
        raise TemplateSyntaxError(msg)
    return RenderTableNode(table_config_var_name)


@register.filter
def get_range( value ):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  return range( value )


@register.filter
def index(List, i):
    """
    {{ List|index:x }} is equal to List[x]
    """
    return List[int(i)]
