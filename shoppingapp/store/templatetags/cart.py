from django import template

register=template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(pid,cart):
	keys=cart.keys()
	"""
	for ids in keys:
		#print('sample',ids)
		if type(ids)== str:
			if ids==pid.id:
				print('working')
				return True
	print('not working')
	"""

	for i in keys:
		#print('cart',cart.get(pid))
		if cart.get(pid)==int(pid):
			return True
		else:
			#print("not working")
			return False


	#if pid.id in keys:
		#print("working")
		#return True
