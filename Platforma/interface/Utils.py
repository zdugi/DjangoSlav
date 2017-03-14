def formatYTUrl(url):
	# ovo je samo proba
	start = url.find("v=")
	end = url.find("&", start)

	videoId = "SuR3LeAUYA4"

	if end != -1:
		videoId= url[start+2:end]
	elif start != -1:
		videoId = url[start+2:]

	return "https://www.youtube.com/embed/" + videoId