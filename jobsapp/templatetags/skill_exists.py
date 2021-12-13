from django import template

register = template.Library()


@register.simple_tag(name="skill_exists")
def skill_exists(id, skills):
    return True if skills is not None and len(skills) > 0 and str(id) in skills else False


@register.filter
def get_item(dictionary, key):
    return dict(dictionary).get(key)