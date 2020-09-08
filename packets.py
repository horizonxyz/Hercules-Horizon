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
	hpp = '/***************************************************\n'
	hpp += ' *       _   _            _                        *\n'
	hpp += ' *      | | | |          (_)                       *\n'
	hpp += ' *      | |_| | ___  _ __ _ _______  _ __          *\n'
	hpp += ' *      |  _  |/ _ \| \'__| |_  / _ \| \'_  \        *\n'
	hpp += ' *      | | | | (_) | |  | |/ / (_) | | | |        *\n'
	hpp += ' *      \_| |_/\___/|_|  |_/___\___/|_| |_|        *\n'
	hpp += ' ***************************************************\n'
	hpp += ' * This file is part of Horizon (c).\n'
	hpp += ' * Copyright (c) 2019 Horizon Dev Team.\n'
	hpp += ' *\n'
	hpp += ' * Base Author - Sagun Khosla. (sagunxp@gmail.com)\n'
	hpp += ' *\n'
	hpp += ' * This library is free software; you can redistribute it and/or modify\n'
	hpp += ' * it under the terms of the GNU General Public License as published by\n'
	hpp += ' * the Free Software Foundation, either version 3 of the License, or\n'
	hpp += ' * (at your option) any later version.\n'
	hpp += ' *\n'
	hpp += ' * This library is distributed in the hope that it will be useful,\n'
	hpp += ' * but WITHOUT ANY WARRANTY; without even the implied warranty of\n'
	hpp += ' * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n'
	hpp += ' * GNU General Public License for more details.\n'
	hpp += ' *\n'
	hpp += ' * You should have received a copy of the GNU General Public License\n'
	hpp += ' * along with this library.  If not, see <http://www.gnu.org/licenses/>.\n'
	hpp += ' **************************************************/\n\n'
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
							print("In client `{}` packet-ver `{}`: Found different packet names (new: `{}`, existing: `{}`) for same packet id {}".format(client_type, (packet_version, "Default")[packet_version == 0], packet_name, real_name, packet_id))

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
	strings.append((
		"#ifndef HORIZON_{server_namec}_PACKET_LENGTH_TABLE\n"
		"#define HORIZON_{server_namec}_PACKET_LENGTH_TABLE\n"
		"\n"
		"#include \"Core/Multithreading/LockedLookupTable.hpp\"\n\n"
		"#include \"Default.hpp\"\n\n"
	).format(server_namec=server_name.upper()))

	for vi, vl in enumerate(sorted(version_list, reverse=True)):
		s = ""
		if vi == 0:
			s += "#if "
		elif vi != len(version_list) - 1:
			s += "#elif "

		if vi != len(version_list) - 1:
			s += "CLIENT_VERSION >= {}\n".format(vl)
			s += "#include \"{}.hpp\"\n".format(vl)
		else:
			s += "#endif\n"

		strings.append(s)

	strings.append((
		"\n"
		"namespace Horizon\n"
		"{{\n"
		"namespace {}\n"
		"{{\n"
		"/**\n"
		" * @brief Packet Length Table object that stores\n"
		" * the packet length of each packet of this client version.\n"
		" * The data is stored in a thread-safe lookup table.\n"
		" * RAII techinque ensures that the table is populated on instantiation.\n"
		" */\n"
		"class PacketLengthTable\n"
		"{{\n"
		"public:\n"
		"	PacketLengthTable()\n"
		"	{{\n"
	).format(server_name))

	s = ""
	for pi, pn in enumerate(sorted(packets.keys())):
		s += "\t\t_packet_length_table.insert({}, {});\n".format(packets[pn]['id'], packets[pn]['len'])

	strings.append(s)

	strings.append((
		"	}}\n"
		"\n"
		"	~PacketLengthTable() {{ }}\n"
		"\n"
		"	ShufflePacketLengthTable *instance()\n"
		"	{{\n"
		"		static ShufflePacketLengthTable p;\n"
		"		return &p;\n"
		"	}}\n"
		"\n"
		"protected:\n"
		"	LockedLookupTable<uint16_t, int> _packet_length_table;\n\n"
		"}};\n"
		"}}\n"
		"}}\n"
		"#endif /* HORIZON_{server_namec}_PACKET_LENGTH_TABLE */"
	).format(server_namec=server_name.upper()))

	return "".join(strings)

def write_packet_shuffle_table_file(server_name, packets, version):
	strings = []

	strings.append((
		"#ifndef HORIZON_{server_namec}_SHUFFLE_PACKET_LENGTH_TABLE_{version}\n"
		"#define HORIZON_{server_namec}_SHUFFLE_PACKET_LENGTH_TABLE_{version}\n"
		"\n"
		"#include \"Core/Multithreading/LockedLookupTable.hpp\"\n\n"
		"#include \"Default.hpp\"\n\n"
		"namespace Horizon\n"
		"{{\n"
		"namespace {server_name}\n"
		"{{\n"
		"namespace ShufflePackets\n"
		"{{\n"
	).format(server_name=server_name, server_namec=server_name.upper(), version=version))

	strings.append((
		"/**\n"
		" * @brief Shuffle Packet Length Table object that stores\n"
		" * the packet length of each packet of this client version.\n"
		" * Packets with IDs already existent in the database are over-written.\n"
		" * The data is stored in a thread-safe lookup table.\n"
		" * RAII techinque ensures that the table is populated on instantiation.\n"
		" */\n"
		"class ShufflePacketLengthTable : public PacketLengthTable\n"
		"{{\n"
		"public:\n"
		"	ShufflePacketLengthTable()\n"
		"	{{\n"
	).format(server_name))

	s = ""
	for pi, pn in enumerate(sorted(packets.keys())):
		s += "\t\t_packet_length_table.insert({}, {});\n".format(packets[pn]['id'], packets[pn]['len'])

	strings.append(s)

	strings.append((
		"	}}\n"
		"\n"
		"	~ShufflePacketLengthTable() {{ }}\n"
		"\n"
		"}};\n"
		"}}\n"
		"}}\n"
		"}}\n"
		"#endif /* HORIZON_{server_namec}_SHUFFLE_PACKET_LENGTH_TABLE_{version} */"
	).format(server_namec=server_name.upper(), version=version))

	return "".join(strings)

def create_packet_length_files(pvl, server):
	server_name = get_server_name(server)

	for client in pvl[server].keys():
		client_folder = get_client_folder(client)
		if not os.path.isdir("Server/" + server_name + "/Packets/" + client_folder):
			os.mkdir("Server/" + server_name + "/Packets/" + client_folder, 0o777)

		if not os.path.isdir("Server/" + server_name + "/Packets/" + client_folder + "/Tables"):
			os.mkdir("Server/" + server_name + "/Packets/" + client_folder + "/Tables", 0o777)

		for vi, version in enumerate(sorted(pvl[server][client].keys())):
			client_folder = get_client_folder(client)
			server_name = get_server_name(server)
			pvll = pvl[server][client][version]
			
			f = open("Server/{}/Packets/{}/Tables/{}.hpp".format(server_name, client_folder, (version, "Default")[version == 0]), "w+")
			f.write(get_legal())
			if version == 0:
				f.write(write_packet_table_file(server_name, pvll, pvl[server][client].keys()))
			else:
				f.write(write_packet_shuffle_table_file(server_name, pvll, version))
			f.close()

def update_packet_file(file_path, packet, pid, client, version):
	f = open(file_path, "r")
	linesa = f.readlines()
	liness = "".join(linesa)
	f.close()

	start = linesa.index("enum {\n")

	pkt_arr = []
	while True:
		rec = re.compile("#(el)?if PACKETVER >= ([0-9]+)\n")
		found = rec.search(linesa[start])
		if found:
			rec = re.compile("\tID_([A-Za-z0-9_]+) = ([0-9a-zA-Z]+)\n")
			found = rec.search(linesa[start + 1])
			if found:
				pkt_arr.append([ found.group(2), found.group(3), found.group(4) ])
		else:
			rec = re.compile("\tID_([A-Za-z0-9_]+) = ([0-9a-zA-Z]+)\n")
			found = rec.search(linesa[start])
			if found:
				pkt_arr.append([ 0, found.group(1), found.group(2) ])

		if "};\n" in linesa.pop(start):
			break

	# append new version pid
	pkt_arr.append([ version, packet, pid ])

	arr_len = len(pkt_arr)

	# delete previous entries or skip if version exists.
	for i in range(0, arr_len):
		if version == pkt_arr[i - 1][0]:
			return

	newlines = []

	# append new entries
	newlines.insert(len(newlines), "enum {\n")

	if arr_len > 1:
		conditional = True
		print("Conditional: {} {}".format(version, client))
		print(pkt_arr)
		exit()
	else:
		conditional = False

	for i in range(0, arr_len):
		pkt = pkt_arr[i]
		if not conditional:
			newlines.insert(len(newlines), "\tID_{} = {}\n".format(pkt[1], pkt[2]))
		else:
			newlines.insert(len(newlines), "#{} PACKETVER >= {}\n".format(("elif", "if")[i == 1], pkt[0]))
			newlines.insert(len(newlines), "\tID_{} = {}\n".format(pkt[1], pkt[2]))

		if i == arr_len - 1:
			if conditional:
				newlines.insert(len(newlines), "#endif\n")
			newlines.insert(len(newlines), "};\n")

	newarr = linesa[:start] + newlines + linesa[start:]
	f = open(file_path, "w")
	f.write("".join(newarr))
	f.close()
	status("Updated {}".format(file_path))

def create_packet_file(struct_dirpath, pvl, server, client):
	server_name = get_server_name(server)
	client_folder = get_client_folder(client)

	for vi, version in enumerate(pvl[server][client]):
		for pi, packet in enumerate(pvl[server][client][version]):
			pid = pvl[server][client][version][packet]['id']
			file_path = "Server/" + server_name + "/Packets/Structures/{}.hpp".format(packet)

			if os.path.exists(file_path):
				update_packet_file(file_path, packet, pid, client, version)
				continue

			f = open(file_path, "w")
		
			f.write(get_legal())

			strings = []
			strings.append((
			"#ifndef HORIZON_{server_namec}_{packet}_HPP\n"
			"#define HORIZON_{server_namec}_{packet}_HPP\n"
			"\n"
			"#include \"Server/Common/PacketBuffer.hpp\"\n"
			"\n"
			"namespace Horizon\n"
			"{{\n"
			"namespace {server_name}\n"
			"{{\n"
			"namespace Packet\n"
			"{{\n\n"
			"enum {{\n"
			"	ID_{packet} = {packet_id}\n"
			"}};\n"
			"/**\n"
			" * @brief Main object for the aegis packet: {packet}\n"
			).format(server_namec=server_name.upper(), server_name=server_name, packet=packet, packet_id=pid))

			# dirty re-loop for this little thing.
			strings.append((
				" * Size : {bytes} @ {version}\n"
			).format(version=version, bytes=pvl[server][client][version][packet]['len']))

			strings.append((
			" *\n"
			" */ \n"
			"class {packet} : public PacketBuffer\n"
			"{{\n"
			"public:\n"
			"	{packet}() : Packet(ID_{packet}) {{ }}\n"
			"	~{packet}() {{ }}\n"
			"\n"
			"	virtual {packet} *serialize()\n"
			"	{{\n"
			"		return this;\n"
			"	}}\n"
			"\n"
			"	virtual void deserialize(PacketBuffer &/*buf*/) {{ }}\n"
			"\n"
			"	virtual {packet} *operator << (PacketBuffer &right)\n"
			"	{{\n"
			"		deserialize(right);\n"
			"		return this;\n"
			"	}}\n"
			"\n"
			"	virtual {packet} *operator >> (PacketBuffer &right)\n"
			"	{{\n"
			"		return right = serialize();\n"
			"	}}\n"
			"\n"
			"protected:\n"
			"	/* Structure Goes Here */\n"
			"}};\n"
			"}}\n"
			"}}\n"
			"}}\n"
			).format(server_namec=server_name.upper(), packet=packet, bytes=pvl[server][client][version][packet]['len']))

			strings.append((
			"#endif /* HORIZON_{server_namec}_{packet}_HPP */"
			).format(server_namec=server_name.upper(), packet=packet))

			f.write("".join(strings))
			f.close()

if not os.path.isdir("Server"):
	os.mkdir("Server", 0o777)

for server in sorted(pvl.iterkeys()):
	status("Writing packet handlers for " + get_server_name(server) + " server...")

	server_name = get_server_name(server)

	if not os.path.isdir("Server/" + server_name):
		os.mkdir("Server/" + server_name, 0o777)

	if not os.path.isdir("Server/" + server_name + "/Packets"):
		os.mkdir("Server/" + server_name + "/Packets", 0o777)

	create_packet_length_files(pvl, server)

	for ci, client in enumerate(sorted(pvl[server])):
		client_folder = get_client_folder(client)
		struct_dirpath = "Server/" + server_name + "/Packets/Structures"

		if not os.path.isdir(struct_dirpath):
			os.mkdir(struct_dirpath, 0o777)

		create_packet_file(struct_dirpath, pvl, server, client)
	