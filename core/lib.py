import random

def get_html_color_code():
	r = lambda: random.randint(0,255)
	return '#%02X%02X%02X' % (r(),r(),r())


def colour_replies(replies):

	#Generate colours for replies.


	html_color_obj = [
		
		{'color':"#FDB45C",'highlight':"#FFC870"},
		{'color':"#949FB1",'highlight':"#A8B3C5"},
		{'color':"#4D5360",'highlight':"#616774"},
		{'color':"#F7464A",'highlight':"#FF5A5E"},
		{'color':"#46BFBD",'highlight':"#5AD3D1"},
		{'color':"#4DA519",'highlight':"#5AD3D1"},
		{'color':"#7393E7",'highlight':"#5AD3D1"},
		{'color':"#7537CC",'highlight':"#5AD3D1"},
		{'color':"#A0A42A",'highlight':"#5AD3D1"},
		{'color':"#ACD287",'highlight':"#5AD3D1"},
		{'color':"#275055",'highlight':"#5AD3D1"},
		{'color':"#AF7210",'highlight':"#5AD3D1"},
	]

	# IF remain equal 0, ratings doesn't show.
	total_hits = 0
	for idx, reply in enumerate(replies):
		
		color = None
		total_hits += reply.hits
		try:
			color = html_color_obj[idx]['color']
		except Exception:

			color = get_html_color_code()
		reply.color = color

	return replies
