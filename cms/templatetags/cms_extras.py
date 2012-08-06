from django import template

register = template.Library()

@register.filter
def get_range( value ):
    return range( 1, value + 1 )

@register.filter(name="get_precise_range")
def get_precise_range(start, end):
    return range(start, end+1)

@register.filter(name="get_country_pref")
def get_country_pref(form, num):
    return form.get_country_pref(num)