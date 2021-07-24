from django import template
import json

register = template.Library()

@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]

@register.filter(name='dict2obj')
def dict2obj(value, arg):
    return obj.dict2obj(value)

class obj(object):
        def __init__(self, dict_):
            self.__dict__.update(dict_)
        def dict2obj(d):
            return json.loads(json.dumps(d), object_hook=obj)
            
class IncrementVarNode(template.Node):

    def __init__(self, var_name):
        self.var_name = var_name

    def render(self,context):
        value = context[self.var_name]
        context[self.var_name] = value + 1
        return u""

def increment_var(parser, token):

    parts = token.split_contents()
    if len(parts) < 2:
        raise template.TemplateSyntaxError("'increment' tag must be of the form:  {% increment <var_name> %}")
    return IncrementVarNode(parts[1])

register.tag('increment', increment_var)