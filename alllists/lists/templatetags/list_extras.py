from django import template

register = template.Library()

@register.filter(name='order_children')
def order_children(qset):
	return qset.order_by('order_number')