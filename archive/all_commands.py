def print_all_commands():
	commands = [
		"/heehee",
		"/help",
		"/hello",
		"/hoyaa",
		"/inspire",
		"/insult [name]",
		"/join",
		"/leave",
		"/play [url]",
		"/randomreddit",
		"/rrr",
		"/Sieg",
		"/speakas [name] (if available)",
		"/stop",
	]

	res = ""
	for c in commands:
		res += c + "\n"

	return res
