def xml2dict(filename):
	import re
	import xml.etree.ElementTree as ET
	from pygeocoder import Geocoder
	expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
	        "Trail", "Parkway", "Commons"]
	street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
	street_mapping = {"St": "Street",
			            "St.": "Street",
			            "Ave" : "Avenue",
			            "Rd." : "Road",
			            "Rd" : "Road",
			            "SE" : "Southeast",
			            "S.E." : "Southeast",
			            "NE" : "Northeast",
			            "S" : "South",
			            "Dr" : "Drive",
			            "Rd/Pkwy" : "Road/Parkway",
			            "Ln" : "Lane",
			            "Dr." : "Drive",
			            "E" : "East",
			            "Pl" : "Plain",
			            "ne" : "Northeast",
			            "NW" : "Northwest",
			            "Ave." : "Avenue",
			            "N." : "North",
			            "W" : "West",
			            "Pkwy" : "Parkway",
			            "Ter" : "Terrace",
			            "Pky" : "Parkway",
			            "SW" : "Southwest",
			            "N" : "North",
			            "Blvd" : "Boulevard"}
	city_mapping = {"Minneapolis, MN" : "Minneapolis",
					"St. Anthony" : "Saint Anthony",
					"St. Paul" : "Saint Paul",
					"St Anthony" : "Saint Anthony",
					"St Paul" : "Saint Paul"}            
	CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
	address = ['addr:unit', 'addr:full','addr:housenumber', 'addr:postcode', 'addr:street', 
				'addr:city', 'addr:state', 'addr:country',
				'addr:suite', 'addr:housename']       
	def shape_element(element):
	    node = {}
	    if element.tag == "node" or element.tag == "way" :
	        node['type'] = element.tag
	        for i in element.attrib.keys():
	            if i in CREATED:
	                node['created'] = {}
	                break
	        for i in element.attrib.keys():
	            if i in CREATED:
	                node['created'][i] = element.attrib[i]
	            elif i == 'lon' or i == 'lat':
	                continue
	            else:
	                node[i] = element.attrib[i]
	        if 'lat' in element.attrib.keys():
	            node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]
	        for i in element:
	            if 'k' in i.attrib:
	                if i.attrib['k'] in address:
	                    node['address'] = {}
	                elif i.attrib['k'].startswith('metcouncil:'):
	                    node['metcouncil'] = {}
	                elif i.attrib['k'].startswith('tiger:'):
	                	node['tiger'] = {}
	                elif i.attrib['k'].startswith('metrogis:'):
	                	node['metrogis'] = {}
	                elif i.attrib['k'].startswith('umn:'):
	                	node['umn'] = {}
	                elif i.attrib['k'].startswith('gnis:'):
	                	node['gnis'] = {}
	        for i in element:
	        	if 'k' in i.attrib:
	        		if i.attrib['k'] in ['umn:BuildingCenterXYLatitude', 'umn:BuildingCenterXYLongitude']:
	        			node['pos'] = []
	        			break
	        for i in element:
        		if 'k' in i.attrib:
        			if i.attrib['k'] == 'umn:BuildingCenterXYLatitude':
        				node['pos'].append(float(i.attrib['v']))
        				break
        	for i in element:
        		if 'k' in i.attrib:
        			if i.attrib['k'] == 'umn:BuildingCenterXYLongitude':
        				node['pos'].append(float(i.attrib['v']))
        				break
	        for i in element:
	            if 'ref' in i.attrib:
	                node['node_refs'] = []
	        for i in element:
	            if 'k' in i.attrib:
	                if i.attrib['k'] in address:
	                	if i.attrib['k'] == 'addr:city':
	                		if i.attrib['v'] in city_mapping.keys():
	                			node['address'][re.sub('addr:', '', i.attrib['k'])] = city_mapping[i.attrib['v']]
	                		else:
	                			node['address'][re.sub('addr:', '', i.attrib['k'])] = i.attrib['v']
	                	else:
	                		node['address'][re.sub('addr:', '', i.attrib['k'])] = i.attrib['v']
	                elif i.attrib['k'].startswith('metcouncil:'):
	                    node['metcouncil'][re.sub('metcouncil:', '', i.attrib['k'])] = i.attrib['v']
	                elif i.attrib['k'].startswith('tiger:'):
	                	node['tiger'][re.sub('tiger:', '', i.attrib['k'])] = i.attrib['v']
	                elif i.attrib['k'].startswith('metrogis:'):
	                	node['metrogis'][re.sub('metrogis:', '', i.attrib['k'])] = i.attrib['v']
	                elif (i.attrib['k'].startswith('umn:') and
	                		i.attrib['k'] not in ['umn:BuildingCenterXYLatitude', 'umn:BuildingCenterXYLongitude']):
	                	node['umn'][re.sub('umn:', '', i.attrib['k'])] = i.attrib['v']
	                elif i.attrib['k'].startswith('gnis:'):
	                	node['gnis'][re.sub('gnis:', '', i.attrib['k'])] = i.attrib['v']
	                elif ('addr:street:' in i.attrib['k'] or
	                		i.attrib['k'] in ['umn:BuildingCenterXYLatitude', 'umn:BuildingCenterXYLongitude']):
	                    continue
	                else:
	                    node[i.attrib['k']] = i.attrib['v']
	            if 'ref' in i.attrib:
	                node['node_refs'].append(i.attrib['ref'])
	        return node
	temp = []
	data = []
	for _, element in ET.iterparse(filename):
	    temp.append(shape_element(element))
	for i in temp:
		if i != None:
			data.append(i)
	for i in data:
		if 'address' in i:
			if 'street' in i['address']:
				search = street_type_re.search(i['address']['street'])
				if search:
					if street_type_re.search(i['address']['street']).group() in street_mapping.keys():
						data[data.index(i)]['address']['street'] = re.sub(street_type_re.search(i['address']['street']).group(), 
																			street_mapping[street_type_re.search(i['address']['street']).group()], 
																			data[data.index(i)]['address']['street'])
	for i in data:
	    if 'address' in i and 'pos' in i:
	        if 'postcode' in i['address']:
	            if len(i['address']['postcode']) < 5 or re.search('[a-zA-Z]', i['address']['postcode']):
	                results = Geocoder.reverse_geocode(i['pos'][0], i['pos'][1])
	                i['address']['postcode'] = str(results.postal_code)
	    elif 'address' in i and 'pos' not in i:
	    	if 'postcode' in i['address']:
	    		if len(i['address']['postcode']) < 5 or re.search('[a-zA-Z]', i['address']['postcode']):
	    			q = ''
	    			if 'housename' in i['address']:
	    				q = i['address']['housename'] + ' MN'
	    			elif 'housenumber' in i['address'] and 'street' in i['address']:
	    				q = i['address']['housenumber'] + ' ' + i['address']['street'] + ' MN'
	    			results = Geocoder.geocode(q)
	                i['address']['postcode'] = str(results.postal_code)
	for i in data:
	    if 'address' in i:
	    	if 'postcode' in i['address']:
	    		if len(i['address']['postcode']) > 5:
	    			i['address']['postcode'] = i['address']['postcode'][0:5]
	return data

def dict2json(dict, output_file):
	import codecs
	import json
	with codecs.open(output_file, 'w') as fo:
	    for i in dict:
	        fo.write(json.dumps(i) + '\n')
	fo.close()

def audit_xml(filename, form = 'all', value = None):
	import xml.etree.ElementTree as ET
	def count_attrib(filename):
		attrib_count = {}
		for _, element in ET.iterparse(filename):
			if element.tag in ['node', 'way', 'tag', 'nd']:
			    for i in element.attrib.keys():
			        if i not in attrib_count.keys():
			            attrib_count[i] = {'count' : 1}
			        else:
			            attrib_count[i]['count'] += 1
		return attrib_count
	def count_val(x, filename):
		k = {}
		for _, element in ET.iterparse(filename):
			if element.tag in ['node', 'way', 'tag', 'nd']:
			    if x in element.attrib:
			        if element.attrib[x] not in k:
			            k[element.attrib[x]] = 1
			        else:
			            k[element.attrib[x]] += 1
		return k
	def tag_count(filename):
		tags = {}
		for _, element in ET.iterparse(filename):
			if element.tag in ['node', 'way', 'tag', 'nd']:
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