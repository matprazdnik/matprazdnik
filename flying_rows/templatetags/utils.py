from django import template

register = template.Library()


class SetVariableNode(template.Node):
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        value = template.Variable(self.var_value).resolve(context)
        context[self.var_name] = value
        return ""


@register.tag('set_variable')
def set_variable(parser, token):
    """
        {% set <var_name> = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form: {% set <var_name> = <var_value> %}")
    return SetVariableNode(parts[1], parts[3])
