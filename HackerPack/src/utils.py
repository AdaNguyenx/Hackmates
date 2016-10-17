def convert_keys_to_string_from_unicode(dictionary):
	"""Recursively converts dictionary keys to strings."""
	if not isinstance(dictionary, dict):
		return dictionary
	return dict((str(k), convert_keys_to_string_from_unicode(v))
	            for k, v in dictionary.items())
