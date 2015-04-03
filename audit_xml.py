def audit_xml(filename, form = 'all', value = None):
	import xml.etree.ElementTree as ET
	def count_attrib(filename):
		attrib_count = {}
		for _, element in ET.iterparse(filename):
		    for i in element.attrib.keys():
		        if i not in attrib_count.keys():
		            attrib_count[i] = {'count' : 1}
		        else:
		            attrib_count[i]['count'] += 1
		return attrib_count
	def count_val(x, filename):
		k = {}
		for _, element in ET.iterparse(filename):
		    if x in element.attrib:
		        if element.attrib[x] not in k:
		            k[element.attrib[x]] = 1
		        else:
		            k[element.attrib[x]] += 1
		return k
	def tag_count(filename):
		tags = {}
		for _, element in ET.iterparse(filename):
			for i in element:
				if i.tag not in tags:
					tags[i.tag] = 1
				else:
					tags[i.tag] += 1
		return tags
	if form.lower() == 'all':
		data = {}
		attrib = count_attrib(filename)
		for i in attrib:
			data[i] = count_val(i, filename)
		for i in data:
			data[i]['TOTAL'] = attrib[i]['count']
		data['TAGS'] = tag_count(filename)
		return data
	elif form.lower() == 'tags':
		return tag_count(filename)
	elif form.lower() == 'attributes':
		return count_attrib(filename)
	elif form.lower() == 'values':
		return count_val(v, filename)
	else:
		if not form or form not in ['all', 'tags', 'attributes', 'values']:
			print "Invalid Audit Type"



