from django import template

register = template.Library()


@register.filter
def get_field(instance, field_name):
    print(f"Fetching {field_name} from {instance}")
    try:
        value = getattr(instance, field_name, None)
        print(f"Value: {value}")
        return value
    except AttributeError:
        print(f"Attribute {field_name} not found in {instance}")
        return None
