import traceback, re, os, sys, json

MIN_PACKET_VERSION = 20000000
CLIENTS = {
	're': True, # Renewal
	'main': True, # Main
	'zero': True, # Zero
	'ad': True,
	'sak': True
}

len_files = [
	'packets2003_len_main.h',
	'packets2003_len_sak.h',
	'packets2004_len_ad.h',
	'packets2004_len_main.h',
	'packets2004_len_sak.h',
	'packets2005_len_ad.h',
	'packets2005_len_main.h',
	'packets2005_len_sak.h',
	'packets2006_len_ad.h',
	'packets2006_len_main.h',
	'packets2006_len_sak.h',
	'packets2007_len_ad.h',
	'packets2007_len_main.h',
	'packets2007_len_sak.h',
	'packets2008_len_ad.h',
	'packets2008_len_main.h',
	'packets2008_len_re.h',
	'packets2008_len_sak.h',
	'packets2009_len_main.h',
	'packets2009_len_re.h',
	'packets2009_len_sak.h',
	'packets2010_len_main.h',
	'packets2010_len_re.h',
	'packets2011_len_main.h',
	'packets2011_len_re.h',
	'packets2012_len_main.h',
	'packets2012_len_re.h',
	'packets2013_len_main.h',
	'packets2013_len_re.h',
	'packets2014_len_main.h',
	'packets2014_len_re.h',
	'packets2015_len_main.h',
	'packets2015_len_re.h',
	'packets2016_len_main.h',
	'packets2016_len_re.h',
	'packets2017_len_main.h',
	'packets2017_len_re.h',
	'packets2017_len_zero.h',
	'packets2018_len_main.h',
	'packets2018_len_re.h',
	'packets2018_len_zero.h',
	'packets2019_len_main.h',
	'packets2019_len_re.h',
	# 'packets2020_len_main.h',
	# 'packets2020_len_re.h',
	# 'packets2020_len_zero.h'
]

shuffle_files = [
	'packets_shuffle_re.h',
	'packets_shuffle_main.h',
	'packets_shuffle_zero.h',
]

def get_client_type(name):
		if re.search(r"_re", file):
			return "re"
		elif re.search(r"_ad", file):
			return "ad"
		elif re.search(r"_main", file):
			return "main"
		elif re.search(r"_zero", file):
			return "zero"
		elif re.search(r"_sak", file):
			return "sak"

def get_client_type_enum(type):
	if not cmp(type, 're'):
		return 'CLIENT_RE'
	if not cmp(type, 'zero'):
		return 'CLIENT_ZERO'
	if not cmp(type, 'ad'):
		return 'CLIENT_AD'
	if not cmp(type, 'sak'):
		return 'CLIENT_SAKRAY'
	return 'CLIENT_RAGEXE'

def get_legal():
	hpp = '-----------------------------------------------------\n'
	hpp += '--       _   _            _                        --\n'
	hpp += '--      | | | |          (_)                       --\n'
	hpp += '--      | |_| | ___  _ __ _ _______  _ __          --\n'
	hpp += '--      |  _  |/ _ \| \'__| |_  / _ \| \'_  \        --\n'
	hpp += '--      | | | | (_) | |  | |/ / (_) | | | |        --\n'
	hpp += '--      \_| |_/\___/|_|  |_/___\___/|_| |_|        --\n'
	hpp += '-----------------------------------------------------\n'
	hpp += '-- This file is part of Horizon (c).\n'
	hpp += '-- Copyright (c) 2019 Horizon Dev Team.\n'
	hpp += '--\n'
	hpp += '-- Base Author - Sagun Khosla. (sagunxp@gmail.com)\n'
	hpp += '--\n'
	hpp += '-- This library is free software; you can redistribute it and/or modify\n'
	hpp += '-- it under the terms of the GNU General Public License as published by\n'
	hpp += '-- the Free Software Foundation, either version 3 of the License, or\n'
	hpp += '-- (at your option) any later version.\n'
	hpp += '--\n'
	hpp += '-- This library is distributed in the hope that it will be useful,\n'
	hpp += '-- but WITHOUT ANY WARRANTY; without even the implied warranty of\n'
	hpp += '-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n'
	hpp += '-- GNU General Public License for more details.\n'
	hpp += '--\n'
	hpp += '-- You should have received a copy of the GNU General Public License\n'
	hpp += '-- along with this library.  If not, see <http://www.gnu.org/licenses/>.\n'
	hpp += '-----------------------------------------------------\n\n'
	return hpp

def get_server_name(server):
	if not cmp(server, 'z'):
		return "Zone"
	elif not cmp(server, 'a'):
		return 'Auth'
	elif not cmp(server, 'c'):
		return 'Char'
	elif not cmp(server, 'cs'):
		return 'Common'
	return ''

def status(status):
	print(status)
	sys.stdout.write('\x1b[1A\x1b[2K')
	return

def get_client_folder(client_type):
	if not cmp(client_type, "re"):
		return "RE"

	if not cmp(client_type, "ad"):
		return "AD"

	if not cmp(client_type, "zero"):
		return "Zero"

	if not cmp(client_type, "sak"):
		return "Sakray"

	return 'Ragexe'

def find_packet_name(pvls, packet_name, client_type, packet_id):
	for pi, packet_name in enumerate(pvls[client_type]):
		for vi, version in enumerate(pvls[client_type][packet_name]):
			if pvls[client_type][packet_name][version]['id'] == packet_id:
				return packet_name
	return ""

##
# Entry Point
##
print "Welcome to the Hercules2Horizon packet classes generator!"
print "All credits to -"
print "\tAuthor: Smokexyz"
print "\t4144 for Hercules packet generation."
print "Initiating the generation of packet version length table..."

pvl = dict()
pvl['z'] = dict()
try:
	for file in shuffle_files:
		f = open("../src/map/" + file, "r")

		lines = f.readlines()

		client_type = get_client_type(file)

		if CLIENTS[client_type] == False:
			continue

		ignore = False
		packet_version = 0
		back_index = 0
		found_if = False
		idx = 0
		status("Reading for zone shuffle packets in '{}'".format(file) + "")
		for idx in range(0, len(lines)):
			line = lines[idx]
			if re.match(r"^\/\/", line):
				continue
			rec = re.compile("(.*)/\*.*\*/(.*)")
			found = rec.search(line)
			if found:
				line = found.group(1) + found.group(2)
			if re.match(r"^\/\*\*", line):
				ignore = True
			if re.match(r"^\s\*\/", line):
				ignore = False
				continue
			if ignore:
				continue

			rec = re.compile(r"PACKETVER[<>= ]+([0-9]+)")
			found = rec.search(line)
			if found:
				packet_version = found.group(1)
			else:
				continue

			if int(packet_version) < MIN_PACKET_VERSION:
				continue

			rec = re.compile("packet\(([x0-9A-Za-z]+),[A-Za-z->0-9,\/*]+\)[;\s\/]+([A-Za-z0-9_]+)[;\s\/]+([-\d]+)")

			sub_line_idx = idx + 1
			while not re.match(r"^#endif", lines[sub_line_idx]):
				search = rec.search(lines[sub_line_idx])
				sub_line_idx += 1
				if search:
					packet_name = search.group(2)
					packet_len = search.group(3)
					packet_id = search.group(1)
					if client_type not in pvl['z']:
						pvl['z'][client_type] = dict()
					if packet_version not in pvl['z'][client_type]:
						pvl['z'][client_type][packet_version] = dict()

					pvl['z'][client_type][packet_version][packet_name] = { 'id': packet_id, 'len': packet_len }
					status("{}: {} size {} found".format(packet_version, packet_id, packet_len))
except Exception:
	traceback.print_exc()

#
# Packet Version Length List
#
#
pvl_unknown = dict()
search_unknown = False
try:
	for file in len_files:
		f = open("../src/common/packets/" + file, "r")
		client_type = get_client_type(file)
		if CLIENTS[client_type] == False:
			continue
		ignore = False
		status("Searching for packet lengths in '{}'...".format(file))
		packet_version = 0
		for line in f:
			if line:
				if re.match(r"^\/\/", line):
					continue
				rec = re.compile("(.*)/\*.*\*/(.*)")
				found = rec.search(line)
				if found:
					line = found.group(1) + found.group(2)
				if re.match(r"^\/\*\*", line):
					ignore = True
				if re.match(r"^\s\*\/", line):
					ignore = False
					continue
				if ignore:
					continue

				rec = re.compile("^#(?:elif|if) PACKETVER[<>= ]+([0-9]+)$")
				ver = rec.search(line)

				if ver:
					packet_version = int(ver.group(1))

				if packet_version > 0 and packet_version < MIN_PACKET_VERSION:
					continue

				# Reset packet version to 0 (default) at the end of an if/else chain
				if re.match("^#endif$", line):
					packet_version = 0

				rec = re.compile("packetLen\(([x0-9A-Za-z]+), ([0-9-]+)\)[\s\/]+([A-Za-z0-9_]+)")

				found = rec.search(line)

				if found:
					packet_id = found.group(1)
					packet_len = found.group(2)
					packet_name = found.group(3) # "0{}".format(found.group(1)[3:].upper())
					server = 'z'

					if re.match(r"^AC_", packet_name) or re.match(r"^CA_", packet_name):
						server = 'a'
					elif re.match(r"^CH_", packet_name) or re.match(r"^HC_", packet_name):
						server = 'c'
					elif re.match(r"^CZ_", packet_name) or re.match(r"^ZC_", packet_name):
						server = 'z'
					elif re.match(r"^CS_", packet_name) or re.match(r"^SC_", packet_name) or re.match(r"^AHC_", packet_name) or re.match(r"^CAH_", packet_name):
						server = 'cs'

					if re.search(r"REASSEMBLY_AUTH", packet_name):
						continue # skip these packets as we're taking it from shuffle packets.

					if not server in pvl:
						pvl[server] = dict()
					if not client_type in pvl[server]:
						pvl[server][client_type] = dict()
					if not packet_version in pvl[server][client_type]:
						pvl[server][client_type][packet_version] = dict()

					# Ignore for incorrect packet names or duplicates
					real_name = find_packet_name(pvl[server], packet_name, client_type, packet_id)
					if cmp(real_name, "") != 0:
						if cmp(real_name, packet_name) == 0:
							status("Found duplicate {} {} as {}".format(packet_version, packet_name, real_name))
							continue
						elif real_name is not 0:
							status("In client `{}` packet-ver `{}`: Found different packet names (new: `{}`, existing: `{}`) for same packet id {}".format(client_type, (packet_version, "Default")[packet_version == 0], packet_name, real_name, packet_id))

					try:
						pvl[server][client_type][packet_version][packet_name] = { 'id': packet_id, 'len': packet_len }
					except:
						print("error: {} {} {} {}".format(server, packet_name, client_type, packet_version))

				elif search_unknown == True:
					rec = re.compile("packetLen\(([x0-9A-Za-z]+), ([0-9-]+)\)$")
					found = rec.search(line)
					if found:
						packet_id = format(found.group(1))
						rootdir = "../src"
						regex = re.compile(packet_id)

						packet_id2 = "0x" + packet_id[3:]
						regex2 = re.compile(packet_id2 + "[,);]")

					  	if packet_id in pvl_unknown:
					  		continue

						for root, dirs, files in os.walk(rootdir):
							for file in files:
								if re.search("../src/map/packets", root) or re.search("../src/common/packets", root) or re.search("packet", file) or re.search("messages", file):
						  			continue
						  		f = open(root + "/" + file, "r")
						  		print("Searching for unknown packet {} in file {}".format(packet_id, root + "/" + file))
						  		sys.stdout.write('\x1b[1A\x1b[2K')
						  		for num, line in enumerate(f, 1):
						  			if regex.search(line) or regex2.search(line):
										print("{}".format(packet_id) + " or " + "{}".format(packet_id2) + " in " + root + "/" + file + " line {} ".format(num) + line.strip())

				  				if packet_id not in pvl_unknown:
				  					pvl_unknown[packet_id] = True
	print("Done.")
except Exception:
	traceback.print_exc()

f = open("packets.out", "w+")
f.write(json.dumps(pvl))
f.close()

print("Packet tables have been dumped in json format to file 'packets.out'")

def write_packet_table_file(server_name, packets, version_list):
	strings = []

	strings.append(get_legal())
	strings.append((
		"local default_packets = {{\n"
	).format(server_name=server_name))

	s = ""
	for pi, pn in enumerate(sorted(packets.keys())):
		s += "\t['{}'] = {{ ['length'] = {}, ['module'] = require('{}') }},\n".format(packets[pn]['id'], packets[pn]['len'], pn)

	strings.append(s)

	strings.append((
		"}}\n\n"

		"function default_packets:new(o)\n"
		"\to = o or default_packets\n"
		"\tsetmetatable(o, self)\n"
		"\tself.__index = self\n"
		"\treturn o\n"
		"end\n\n"

		"function default_packets:add(id, len, module)\n"
		"\tself[id] = {{ [\"length\"] = len, [\"module\"] = module }}\n"
		"end\n\n"

		"return default_packets\n"
	).format(server_namec=server_name.upper(), server_name=server_name))

	return "".join(strings)

def write_packet_shuffle_table_file(server_name, packets, client, version):
	client_folder = get_client_folder(client).lower()
	strings = []

	strings.append(get_legal())

	strings.append((
		"local d = require('default_packets_{client}')\n\n"
	).format(client=client_folder))

	s = ""
	for pi, pn in enumerate(sorted(packets.keys())):
		s += "d:add({}, {}, require('{}'))\n".format(packets[pn]['id'], packets[pn]['len'], pn)

	strings.append(s);

	strings.append("\n")

	strings.append("return d\n")

	return "".join(strings)

def create_packet_length_files(pvl, server):
	server_name = get_server_name(server).lower()

	for client in pvl[server].keys():
		client_folder = get_client_folder(client).lower()
		if not os.path.isdir("src/" + server_name + "/modules/packets/" + client_folder):
			os.mkdir("src/" + server_name + "/modules/packets/" + client_folder, 0o777)

		for vi, version in enumerate(sorted(pvl[server][client].keys())):
			client_folder = get_client_folder(client).lower()
			pvll = pvl[server][client][version]
			
			f = open("src/{}/modules/packets/{}/{}_packets_{}.lua".format(server_name, client_folder, (version, "default")[version == 0], client_folder), "w+")

			if version == 0:
				f.write(write_packet_table_file(server_name, pvll, pvl[server][client].keys()))
			else:
				f.write(write_packet_shuffle_table_file(server_name, pvll, client, version))
			f.close()


	finit = open("src/{}/init.lua".format(server_name), "w")

	finit.write(get_legal())
	finit.write("-- Package paths (defined relative to the root directory of server execution)\n")

	for client in pvl[server].keys():
		client_folder = get_client_folder(client).lower()
		finit.write("package.path = package.path .. \";./scripts/{}/modules/packets/{}/?.lua\"\n".format(server_name, client_folder))
	
	finit.write("package.path = package.path .. \";./scripts/{}/modules/packets/structs/?.lua\"\n\n".format(server_name))
	finit.write("package.path = package.path .. \";./scripts/{}/modules/libs/?.lua\"\n\n".format(server_name))
	finit.write("package.path = package.path .. \";./config/?.lua\"\n\n")

	finit.write("-- Initializing global variable\n-- Ensures that modules are running within project directory and not standalone.\n")
	finit.write("RAGNA_ROOT = true\n\n")
	finit.write("auth_config = require('auth-server')\n")
	finit.write("char_config = require('char-server')\n")
	finit.write("zone_config = require('zone-server')\n\n")

	finit.write("\nlocal packet_tables = {\n")

	for client in pvl[server].keys():
		client_folder = get_client_folder(client).lower()
		finit.write("\t['{}'] = {{\n".format(client_folder))
		for vi, version in enumerate(sorted(pvl[server][client].keys())):
			if version == 0: continue
			finit.write("\t\t[\"{}\"] = require(\"{}_packets_{}\"),\n".format(version, version, client_folder))
		finit.write("\t},\n")

	finit.write("}\n\n")

	finit.write("print('Ragnarok LUA scripts have been initialized.')\n\n")

	finit.write("\nreturn packet_tables\n")
	finit.close()

def update_packet_file(file_path, server_name, packet, pid, client, version):
	f = open(file_path, "r")
	linesa = f.readlines()
	liness = "".join(linesa)
	f.close()

	start = 29

	pkt_arr = []
	once = False

	while once is False:
		if re.compile("^end\n").search(linesa[start]):
			linesa.pop(start)
			break

		found = re.compile("(else)?if packet_version >= ([0-9]+) then\n").search(linesa[start])
		if found:
			prev_version = found.group(2)
			found = re.compile("\tlocal pid = ([0-9a-z-A-Z]+)\n").search(linesa[start + 1])
			if found:
				linesa.pop(start)
				linesa.pop(start)
				pkt_arr.append([ int(prev_version), found.group(1) ])
		else:
			found = re.compile("local pid = ([0-9a-z-A-Z]+)\n").search(linesa[start])
			if found:
				once = True
				linesa.pop(start)
				pkt_arr.append([ 0, found.group(1) ])

	# delete previous entries or skip if version exists.
	duplicate_versions = []
	for i, v in enumerate(pkt_arr):
		if version == v[0]:
			return
		if v[0] in duplicate_versions:
			pkt_arr.pop(i)
		else:
			duplicate_versions.append(v[0])

	# append new version pid
	pkt_arr.append([ version, pid ])

	arr_len = len(pkt_arr)

	newlines = []

	if arr_len > 1:
		conditional = True
		# re-iterate to sort in descending
		pkt_arr = sorted(pkt_arr, None, reverse=True)
	else:
		conditional = False

	for i in range(0, arr_len):
		pkt = pkt_arr[i]
		if not conditional:
			newlines.insert(len(newlines), "local pid = {}\n".format(pkt[1]))
		else:
			newlines.insert(len(newlines), "{} packet_version >= {} then\n".format(("elseif", "if")[i == 0], pkt[0]))
			newlines.insert(len(newlines), "\tlocal pid = {}\n".format(pkt[1]))

		if i == arr_len - 1:
			if conditional:
				newlines.insert(len(newlines), "end\n")

	newarr = linesa[:start] + newlines + linesa[start:]

	f = open(file_path, "w")
	f.write("".join(newarr))
	f.close()

	status("Updated {}".format(file_path))

def create_packet_file(struct_dirpath, pvl, server, client):
	server_name = get_server_name(server)
	client_folder = get_client_folder(client)

	if not os.path.isdir("src/" + server_name.lower() + "/modules/packets/structs"):
		os.mkdir("src/" + server_name.lower() + "/modules/packets/structs", 0o777)

	for vi, version in enumerate(pvl[server][client]):
		for pi, packet in enumerate(pvl[server][client][version]):
			pid = pvl[server][client][version][packet]['id']

			file_path_l = "src/{}/modules/packets/structs/{}.lua".format(server_name.lower(), packet)

			if os.path.exists(file_path_l):
				update_packet_file(file_path_l, server_name, packet, pid, client, version)
				continue

			f = open(file_path_l, "w")
		
			f.write(get_legal())

			strings = []
			strings.append((
				#"local {server_namel}_config = require('{server_namel}-server')\n\n"
				"if RAGNA_ROOT == nil then print('Error: Running outside of project directory') os.exit() end\n\n"
				"local pid = {packet_id}\n\n"
				"local {packet} = {{\n"
				"\t_id = pid,\n"
				"\t_len = 0,\n"
				"\tbuffer = nil\n"
				"}}\n\n"
				"function {packet}:new(o)\n"
				"\to = o or {packet}\n"
				"\tsetmetatable(o, self)\n"
				"\tself.__index = self\n"
				"\treturn o\n"
				"end\n\n"
				"\n"
			).format(server_namec=server_name.upper(), server_name=server_name, server_namel=server_name.lower(), packet=packet, packet_id=pid))

			if "AC" in packet or "HC" in packet or "ZC" in packet:
				strings.append((
					"function {packet}:serialize()\n"
					"\n"
					"end\n\n").format(packet=packet))
			else:
				strings.append((
					"function {packet}:deserialize()\n"
					"\n"
					"end\n\n").format(packet=packet))
			
			strings.append("return {packet}\n\n".format(packet=packet))

			f.write("".join(strings))
			f.close()
			status ("Written {}".format(file_path_l))


if not os.path.isdir("src"):
	os.mkdir("src", 0o777)

for server in sorted(pvl.iterkeys()):
	status("Writing packet handlers for " + get_server_name(server) + " server...")

	server_name = get_server_name(server)

	if not os.path.isdir("src/" + server_name.lower()):
		os.mkdir("src/" + server_name.lower(), 0o777)

	if not os.path.isdir("src/" + server_name.lower()):
		os.mkdir("src/" + server_name.lower(), 0o777)
	
	if not os.path.isdir("src/" + server_name.lower() + "/modules"):
		os.mkdir("src/" + server_name.lower() + "/modules", 0o777)

	if not os.path.isdir("src/" + server_name.lower() + "/modules/packets"):
		os.mkdir("src/" + server_name.lower() + "/modules/packets", 0o777)

	for ci, client in enumerate(sorted(pvl[server])):
		client_folder = get_client_folder(client)
		struct_dirpath = "src/" + server_name.lower() + "/modules/packets"

		if not os.path.isdir(struct_dirpath):
			os.mkdir(struct_dirpath, 0o777)

		create_packet_file(struct_dirpath, pvl, server, client)

	create_packet_length_files(pvl, server)

	