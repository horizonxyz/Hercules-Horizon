import traceback, re, os, sys, json, subprocess

LAST_NAMED_COMMIT_VER = '26457909e94c910489077ce2643beb08cab33807'
LAST_NAMED_COMMIT_YEAR=2019
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
	'packets2019_len_zero.h',
	'packets2020_len_main.h',
	'packets2020_len_re.h',
	'packets2020_len_zero.h',
	'packets2021_len_main.h',
	'packets2021_len_re.h',
	'packets2021_len_zero.h',
	'packets2022_len_main.h',
	'packets2022_len_zero.h'
]

shuffle_files = [
	'packets_shuffle_re.h',
	'packets_shuffle_main.h',
	'packets_shuffle_zero.h',
]

def cmp(a, b):
	a = str(a)
	b = str(b)
	return (a > b) - (a < b)

def get_client_type(file):
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

def get_client_year(file):
	found = re.search(r"([0-9]+)", file)
	if found:
		return int(found.group(1))
	else:
		return 0000

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
	hpp += ' * Copyright (c) 2023 Horizon Dev Team.\n'
	hpp += ' *\n'
	hpp += ' * Base Author - Sephus. (sagunxp@gmail.com)\n'
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

def client_type_macro(c):
	if c == "re":
		return "R"
	elif c == "ad":
		return "A"
	elif c == "main":
		return "M"
	elif c == "zero":
		return "Z"
	elif c == "sak":
		return "S"

def find_packet_name(pvls, client_type, packet_id):
	for pi, version in enumerate(pvls[client_type]):
		for vi, packet_name in enumerate(pvls[client_type][version]):
			if pvls[client_type][version][packet_name]['id'] == packet_id:
				return packet_name
	return ""

def find_packet_length(pvls, client_type, packet_id):
	for pi, version in enumerate(pvls[client_type]):
		for vi, packet_name in enumerate(pvls[client_type][version]):
			if pvls[client_type][version][packet_name]['id'] == packet_id:
				return pvls[client_type][version][packet_name]['len']
	return ""

def is_handled_packet(packet_name):
	found = re.search(r"^CZ_|^CA_|^CH_|^CS_", packet_name)
	return True if found else False

def is_base_version(version):
	return str(version)[-4:] == "0000"

def create_base_version(year):
	return int("{}0000".format(year))

def write_packet_table_file(server_name, packets, client_folder):
	strings = []
	strings.append((
		"#ifndef HORIZON_{server_namec}_{c}_PACKET_LENGTH_TABLE\n"
		"#define HORIZON_{server_namec}_{c}_PACKET_LENGTH_TABLE\n"
		"\n"
		"#include \"Core/Multithreading/LockedLookupTable.hpp\"\n"
		"#include \"Server/{server_name}/Packets/HandledPackets.hpp\"\n"
		"#include \"Server/{server_name}/Packets/TransmittedPackets.hpp\"\n"
		"\n"
		"namespace Horizon\n"
		"{{\n"
		"namespace {server_name}\n"
		"{{\n"
		"	typedef std::shared_ptr<Base::NetworkPacketHandler<{server_name}Session>> HPacketStructPtrType;\n"
		"	typedef std::shared_ptr<Base::NetworkPacketTransmitter<{server_name}Session>> TPacketStructPtrType;\n"
		"	typedef std::pair<int16_t, HPacketStructPtrType> HPacketTablePairType;\n"
		"	typedef std::pair<int16_t, TPacketStructPtrType> TPacketTablePairType;\n"
	).format(server_name=server_name, server_namec=server_name.upper(), c=client_folder.upper()))

	strings.append((
		"/**\n"
		" * @brief Auto-generated with a python generator tool authored by Sephus (sagunxp@gmail.com).\n"
		" */\n"
		"class PacketLengthTable\n"
		"{{\n"
		"public:\n"
		"	PacketLengthTable(std::shared_ptr<{server_name}Session> s)\n"
		"	: _session(s)\n"
		"	{{\n"
		"#define ADD_HPKT(i, j, k) _hpacket_length_table.insert(i, std::make_pair(j, std::make_shared<k>(s)))\n"
		"#define ADD_TPKT(i, j, k) _tpacket_length_table.insert(i, std::make_pair(j, std::make_shared<k>(s)))\n"
	).format(server_name=server_name))

	s = ""
	for pi, pn in enumerate(sorted(packets.keys())):
		if is_handled_packet(pn):
			s += "\t\tADD_HPKT({}, {}, {});\n".format(packets[pn]['id'], packets[pn]['len'], pn)
		else:
			s += "\t\tADD_TPKT({}, {}, {});\n".format(packets[pn]['id'], packets[pn]['len'], pn)

	strings.append(s)

	strings.append((
		"#undef ADD_HPKT\n"
		"#undef ADD_TPKT\n"
		"	}}\n"
		"\n"
		"	~PacketLengthTable() {{ }}\n"
		"\n"
		"	std::shared_ptr<{server_name}Session> get_session() {{ return _session.lock(); }}\n"
		"\n"
		"	HPacketTablePairType get_hpacket_info(uint16_t packet_id) {{ return _hpacket_length_table.at(packet_id); }}\n"
		"	TPacketTablePairType get_tpacket_info(uint16_t packet_id) {{ return _tpacket_length_table.at(packet_id); }}\n"
		"\n"
		"protected:\n"
		"	LockedLookupTable<uint16_t, HPacketTablePairType> _hpacket_length_table;\n"
		"	LockedLookupTable<uint16_t, TPacketTablePairType> _tpacket_length_table;\n"
		"	std::weak_ptr<{server_name}Session> _session;\n"
		"\n"
		"}};\n"
		"}}\n"
		"}}\n"
		"#endif /* HORIZON_{server_namec}_{c}_PACKET_LENGTH_TABLE */\n"
	).format(server_name=server_name, server_namec=server_name.upper(), c=client_folder.upper()))

	return "".join(strings)

def write_packet_shuffle_table_file(server_name, pvll, client_folder):
	strings = []
	strings.append((
		"#ifndef HORIZON_{server_namec}_CLIENT_PACKET_LENGTH_TABLE\n"
		"#define HORIZON_{server_namec}_CLIENT_PACKET_LENGTH_TABLE\n"
		"\n"
		"#include \"PacketLengthTable.hpp\"\n"
		"\n"
		"namespace Horizon\n"
		"{{\n"
		"namespace {server_name}\n"
		"{{\n"
	).format(server_name=server_name, server_namec=server_name.upper()))

	strings.append((
		"/**\n"
		" * @brief Auto-generated with a python generator tool authored by Sephus (sagunxp@gmail.com).\n"
		" */\n"
		"class ClientPacketLengthTable : public PacketLengthTable\n"
		"{{\n"
		"public:\n"
		"	ClientPacketLengthTable(std::shared_ptr<{server_name}Session> s)\n"
		"	: PacketLengthTable(s)\n"
		"	{{\n"
		"#define ADD_HPKT(i, j, k) _hpacket_length_table.insert(i, std::make_pair(j, std::make_shared<k>(s)))\n"
		"#define ADD_TPKT(i, j, k) _tpacket_length_table.insert(i, std::make_pair(j, std::make_shared<k>(s)))\n"
	).format(server_name=server_name))

	total = len(pvll.keys())
	for vi, version in enumerate(sorted(pvll.keys(), key=lambda x:str(x))):
		packets = pvll[version]

		if is_base_version(version):
			continue # handled separately in parent caller.
		elif len(packets) == 0:
			continue

		strings.append((
			"// Packet Version {version}: {n} Packets\n"
		).format(version=version, n=len(packets)))
		
		strings.append((
			"#if PACKET_VERSION >= {version}\n"
		).format(version=version))

		s = ""
		for pi, pn in enumerate(sorted(packets.keys())):
			if is_handled_packet(pn):
				s += "\t\tADD_HPKT(" + packets[pn]['id'] + ", " + packets[pn]['len'] +", " + pn + ");\n";
			else:
				s += "\t\tADD_TPKT(" + packets[pn]['id'] + ", " + packets[pn]['len'] +", " + pn + ");\n";
		strings.append(s)
		strings.append((
			"#endif\n"
		))
	
	strings.append((
		"#undef ADD_TPKT\n"
		"#undef ADD_HPKT\n"
		"	}}\n"
		"\n"
		"	~ClientPacketLengthTable() {{ }}\n"
		"\n"
		"}};\n"
		"}}\n"
		"}}\n"
		"#endif /* HORIZON_{server_namec}_CLIENT_PACKET_LENGTH_TABLE */\n"
	).format(server_namec=server_name.upper()))

	return "".join(strings)

def create_packet_length_files(pvl, server):
	server_name = get_server_name(server)

	for client in pvl[server].keys():
		client_folder = get_client_folder(client)
		if not os.path.isdir("Server/" + server_name + "/Packets/" + client_folder):
			os.mkdir("Server/" + server_name + "/Packets/" + client_folder, 0o777)

			client_folder = get_client_folder(client)
			server_name = get_server_name(server)
			
			f = open("Server/{}/Packets/{}/PacketLengthTable.hpp".format(server_name, client_folder), "w+")
			f.write(get_legal())
			f.write(write_packet_table_file(server_name, pvl[server][client][sorted(pvl[server][client].keys(), key=lambda x:str(x))[0]], client_folder))
			f.close()
			
			f = open("Server/{}/Packets/{}/ClientPacketLengthTable.hpp".format(server_name, client_folder), "w+")
			f.write(get_legal())
			f.write(write_packet_shuffle_table_file(server_name, pvl[server][client], client_folder))
			f.close()

def order_and_summarize_packet_definitions_header(pvls, server_name, handled=True):
	strings = []

	packets = dict()
	for ci, client_type in enumerate(sorted(pvls.keys())):
		for vi, version in enumerate(pvls[client_type].keys()):
			for pi, packet_name in enumerate(sorted(pvls[client_type][version].keys())):
				if handled and not is_handled_packet(packet_name):
					continue
				elif not handled and is_handled_packet(packet_name):
					continue
				if not packet_name in packets:
					packets[packet_name] = dict()
				if not client_type in packets[packet_name]:
					packets[packet_name][client_type] = dict()
				_id = pvls[client_type][version][packet_name]["id"]
				if not _id in packets[packet_name][client_type]:
					packets[packet_name][client_type][_id] = list()
				if version not in packets[packet_name][client_type][_id]:
					packets[packet_name][client_type][_id].append(int(version))
		
	for pi, packet_name in enumerate(sorted(packets.keys())):
		strings.append((
			"enum {\n"
		))
		count = 0
		total = len(packets[packet_name].keys())
		for ci, client_type in enumerate(sorted(packets[packet_name].keys())):
			if count == 0:	
				strings.append((
					"#if CLIENT_TYPE == '{}'"
				).format(client_type_macro(client_type).upper()))
			else:
				strings.append((
					"#elif CLIENT_TYPE == '{}'"
				).format(client_type_macro(client_type).upper()))
			count2 = 0
			total2 = len(packets[packet_name][client_type].keys())
			for vi, _id in enumerate(sorted(packets[packet_name][client_type].keys(), key=lambda x: packets[packet_name][client_type][x][0], reverse=False)):
				total3 = len(packets[packet_name][client_type][_id])
				if count2 >= 1:	
					strings.append((
						"#elif CLIENT_TYPE == '{}'"
					).format(client_type_macro(client_type).upper()))
				if total3 > 0:
					strings.append(( " && "))
					if total3 > 1:
						strings.append(( "( \\\n"))
					elif total3 == 1:
						strings.append(( " \\\n"))
					else:
						strings.append(( "\n"))
				else:
					strings.append("\n")
				count3 = 0
				for version in sorted(packets[packet_name][client_type][_id], key=lambda x:int(x), reverse=True):
					#version operator is equal if the version is not a base version, because we provide both specific and minimum verisons.
					# every statement is important here for the entire functioning of packet versioning in horizon.
					base_version = is_base_version(version)
					if base_version: 
						has_prev_version = count3 != 0 # // for the 1st instance of PACKET_VERSION >= 20220000
						if has_prev_version:
							prev_version = sorted(packets[packet_name][client_type][_id], key=lambda x:int(x), reverse=True)[count3 - 1]
							if count3 == 0:	# start of the list.
								# if PACKET_VERSION >= 20060000 && PACKET_VERSION <= 20070000
								strings.append((
									"\tPACKET_VERSION >= {} && PACKET_VERSION < {}"
								).format(int(version), int(prev_version)))
							elif count3 < total3 - 1: # before the end of the list
								strings.append((
									"\t|| (PACKET_VERSION >= {} && PACKET_VERSION < {})"
								).format(int(version), int(prev_version)))
							else: # when count3 is equal to total3 (end of list)
								strings.append((
									"\t|| (PACKET_VERSION >= {} && PACKET_VERSION < {})"
								).format(int(version), int(prev_version)))
						elif has_prev_version and total3 > 1: # when there is no previous version and there are more versions
							strings.append((
								"\t|| PACKET_VERSION >= {} &&" # Base Version
							).format(int(version)))
						elif not has_prev_version and total3 >= 1: # count3 == 0 therefore not has_prev_version only required here. Other cases are not required.
							strings.append((
								"\tPACKET_VERSION >= {}"
							).format(int(version)))
						else:
							strings.append(("{} - {}".format(has_prev_version, total3)))
					elif not base_version and total3 == 1: # Keep as base if only one specific client has been found.
						# count3 will be 0 in this step.
						strings.append((
							"\tPACKET_VERSION >= {}"
						).format(int(version)))
					elif not base_version and int(sorted(packets[packet_name][client_type][_id], key=lambda x:int(x), reverse=True)[0]) - int(version) >= 10000:
						if  total3 > 1:
							strings.append((
								"\t|| PACKET_VERSION >= {}"
							).format(int(version)))
						else:
							strings.append((
								"\tPACKET_VERSION >= {}"
							).format(int(version)))
					else: 
						if count3 == 0:	
							strings.append((
								"\tPACKET_VERSION == {}"
							).format(int(version)))
						elif count3 < total3 - 1:
							strings.append((
								"\t|| PACKET_VERSION == {}"
							).format(int(version)))
						else:
							strings.append((
								"\t|| PACKET_VERSION == {}"
							).format(int(version)))
					# When iteration over total3 (version list) has finished and pending the closing of 2 sections -
					# 1) version list 2) client type list. 
					if count3 == total3 - 1 and total3 > 1:
						if base_version: # if iteration is over base_version (using >= to compare) (avoid extra closing brace)
							strings.append(( ")\n"))
						else:
							strings.append(( ")\n"))
					# else if iteration is not completed and version list is more than one in length.
					elif total3 > 1:
						strings.append(( " \\\n" ))
					# else if iteration is not completed or total3 is (greater than 1 - because we're inside loop) in length
					else:
						strings.append(( "\n" ))
					count3+=1
				strings.append((
					"ID_{} = {}\n"
				).format(packet_name, _id))
				count2+=1
			if count == total - 1:
				strings.append((
					"#else\n"
					"ID_{} = 0x0000 // Disabled\n"
					"#endif\n"
				).format(packet_name, _id))
			count+=1
		strings.append((
			"};\n"
		))

		if handled:
			strings.append((
				"/**\n"
				" * @brief Main object for the aegis packet: {pn}\n"
				" *\n"
				" */ \n"
				"class {pn} : public Base::NetworkPacketHandler<{server_name}Session>\n"
				"{{\n"
				"public:\n"
				"	{pn}(std::shared_ptr<{server_name}Session> s)\n"
				"	: NetworkPacketHandler<{server_name}Session>(ID_{pn}, s)\n"
				"	{{}}\n"
				"	virtual ~{pn}() {{}}\n"
				"\n"
				"	void handle(ByteBuffer &&buf);\n"
				"	void deserialize(ByteBuffer &buf);\n"
				"\n"
				"/* Structure */\n"
				"}};\n\n"
			).format(pn=packet_name,server_name=server_name))
		else:
			strings.append((
				"/**\n"
				" * @brief Main object for the aegis packet: {pn}\n"
				" *\n"
				" */ \n"
				"class {pn} : public Base::NetworkPacketTransmitter<{server_name}Session>\n"
				"{{\n"
				"public:\n"
				"	{pn}(std::shared_ptr<{server_name}Session> s)\n"
				"	: NetworkPacketTransmitter<{server_name}Session>(ID_{pn}, s)\n"
				"	{{}}\n"
				"	virtual ~{pn}() {{}}\n"
				"\n"
				"	void deliver();\n"
				"	ByteBuffer &serialize();\n"
				"\n"
				"/* Structure */\n"
				"}};\n\n"
			).format(pn=packet_name,server_name=server_name))

	return "".join(strings)

def order_and_summarize_packet_definitions_source(pvls, handled=True):
	strings = []

	packets = list()
	for ci, client_type in enumerate(sorted(pvls.keys())):
		for vi, version in enumerate(pvls[client_type].keys()):
			for pi, packet_name in enumerate(sorted(pvls[client_type][version].keys())):
				if handled and not is_handled_packet(packet_name):
					continue
				elif not handled and is_handled_packet(packet_name):
					continue
				if len(packet_name.strip()) and not packet_name in packets:
					packets.append(packet_name)

	for packet_name in packets:
		if handled:
			strings.append((
				"/**\n"
				" * {pn}\n"
				" */\n"
				"void {pn}::handle(ByteBuffer &&buf) {{}}\n"
				"void {pn}::deserialize(ByteBuffer &buf) {{}}\n"
			).format(pn=packet_name))
		else:
			strings.append((
			"/**\n"
			" * {pn}\n"
			" */\n"
			"void {pn}::deliver() {{}}\n"
			"ByteBuffer &{pn}::serialize()\n"
			"{{\n"
			"	return buf();\n"
			"}}\n"
		).format(pn=packet_name))

	return "".join(strings)

def write_packet_handled_file_header(server_name, pvls, client_folder):
	strings = []
	strings.append((
		"#ifndef HORIZON_{server_namec}_HANDLED_PACKETS_HPP\n"
		"#define HORIZON_{server_namec}_HANDLED_PACKETS_HPP\n"
		"\n"
		"#include \"Server/Common/Base/NetworkPacket.hpp\"\n"
		"#include \"Server/Common/Configuration/Horizon.hpp\"\n"
		"\n"
		"namespace Horizon\n"
		"{{\n"
		"namespace {server_name}\n"
		"{{\n"
		"class {server_name}Session;\n"
	).format(server_name=server_name, server_namec=server_name.upper()))

	strings.append(order_and_summarize_packet_definitions_header(pvls, server_name))

	strings.append((
		"}} /* namespace {server_name} */\n"
		"}} /* namespace Horizon */\n"
		"#endif /* HORIZON_{server_namec}_TRANSMITTED_PACKETS_HPP */\n"
		).format(server_name=server_name, server_namec=server_name.upper()))

	return "".join(strings)

def write_packet_handled_file_source(server_name, pvls, client_folder):
	strings = []
	strings.append((
		"#include \"HandledPackets.hpp\"\n"
		"#include \"Server/{server_name}/Session/{server_name}Session.hpp\"\n"
		"\n"
		"using namespace Horizon::{server_name};\n\n"
	).format(server_name=server_name, server_namec=server_name.upper()))

	strings.append(order_and_summarize_packet_definitions_source(pvls))

	return "".join(strings)
	
def write_packet_transmitted_file_header(server_name, pvls, client_folder):
	strings = []
	strings.append((
		"#ifndef HORIZON_{server_namec}_TRANSMITTED_PACKETS_HPP\n"
		"#define HORIZON_{server_namec}_TRANSMITTED_PACKETS_HPP\n"
		"\n"
		"#include \"Server/Common/Base/NetworkPacket.hpp\"\n"
		"#include \"Server/Common/Configuration/Horizon.hpp\"\n"
		"\n"
		"namespace Horizon\n"
		"{{\n"
		"namespace {server_name}\n"
		"{{\n"
		"class {server_name}Session;\n"
	).format(server_name=server_name, server_namec=server_name.upper()))

	strings.append(order_and_summarize_packet_definitions_header(pvls, server_name, handled=False))

	strings.append((
		"}} /* namespace {server_name}\n */"
		"}} /* namespace Horizon */\n"
		"#endif /* HORIZON_{server_namec}_TRANSMITTED_PACKETS_HPP */\n"
		).format(server_name=server_name, server_namec=server_name.upper()))

	return "".join(strings)

def write_packet_transmitted_file_source(server_name, pvls, client_folder):
	strings = []
	strings.append((
		"#include \"TransmittedPackets.hpp\"\n"
		"#include \"Server/{server_name}/Session/{server_name}Session.hpp\"\n"
		"#include \"Utility/Utility.hpp\"\n"
		"\n"
		"using namespace Horizon::{server_name};\n\n"
	).format(server_name=server_name, server_namec=server_name.upper()))

	strings.append(order_and_summarize_packet_definitions_source(pvls, handled=False))

	return "".join(strings)

def create_packet_definition_files(pvl, server):
	server_name = get_server_name(server)
	print("Writing packet definition files")
	for ci, client_type in enumerate(sorted(pvl[server].keys())):
		client_folder = get_client_folder(client_type)
		server_name = get_server_name(server)
		
		print("Writing Server/{}/Packets/HandledPackets.hpp".format(server_name))
		f = open("Server/{}/Packets/HandledPackets.hpp".format(server_name), "w+")
		f.write(get_legal())
		f.write(write_packet_handled_file_header(server_name, pvl[server], client_folder))
		f.close()

		
		print("Writing Server/{}/Packets/HandledPackets.cpp".format(server_name))
		f = open("Server/{}/Packets/HandledPackets.cpp".format(server_name), "w+")
		f.write(get_legal())
		f.write(write_packet_handled_file_source(server_name, pvl[server], client_folder))
		f.close()
		
		print("Writing Server/{}/Packets/TransmittedPackets.hpp".format(server_name))
		f = open("Server/{}/Packets/TransmittedPackets.hpp".format(server_name), "w+")
		f.write(get_legal())
		f.write(write_packet_transmitted_file_header(server_name, pvl[server], client_folder))
		f.close()

		print("Writing Server/{}/Packets/TransmittedPackets.cpp".format(server_name))
		f = open("Server/{}/Packets/TransmittedPackets.cpp".format(server_name), "w+")
		f.write(get_legal())
		f.write(write_packet_transmitted_file_source(server_name, pvl[server], client_folder))
		f.close()

def name_generator(CLIENTS, MIN_PACKET_VERSION, LAST_NAMED_COMMIT_VER, LAST_NAMED_COMMIT_YEAR, shuffle_files, len_files):
	print("Checking out revision '" + LAST_NAMED_COMMIT_VER + "' for name generator!")
	if not os.path.isdir("Hercules"):
		print(subprocess.check_output(['git', 'clone', "https://www.github.com/HerculesWS/Hercules.git"]).decode('ascii'))
	wd = os.getcwd()
	os.chdir("Hercules")
	print(subprocess.check_output(['git', 'checkout', LAST_NAMED_COMMIT_VER]).decode('ascii'))
	os.chdir(wd)

	if os.path.isfile('names.out') == True:
		print("'names.out' was already generated... nothing to do.")
		return

	pvl = dict()
	pvl['z'] = dict()
	try:
		for file in shuffle_files:
			f = open("Hercules/src/map/" + file, "r")
	
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
			year = get_client_year(file)

			if year > LAST_NAMED_COMMIT_YEAR:
				continue

			f = open("Hercules/src/common/packets/" + file, "r")
			client_type = get_client_type(file)
			if CLIENTS[client_type] == False:
				continue

			ignore = False
			status("Searching for packet lengths in '{}'...".format(file))
			packet_version = create_base_version(get_client_year(file))
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
						packet_version = create_base_version(get_client_year(file))
	
					rec = re.compile("packetLen\(([x0-9A-Za-z]+), ([0-9-]+)\)[\s\/]+([A-Za-z0-9_]+)")
	
					found = rec.search(line)
	
					if found:
						packet_id = found.group(1)
						packet_len = found.group(2)
						packet_name = found.group(3) # "0{}".format(found.group(1)[3:].upper())
						server = 'z'
	
						status("{} {} {}".format(packet_id, packet_len, packet_name))
	
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
						real_name = find_packet_name(pvl[server], client_type, packet_id)
						if cmp(real_name, "") != 0:
							if cmp(real_name, packet_name) == 0:
								print("Found duplicate {} {} as {}".format(packet_version, packet_name, real_name))
								continue
							elif real_name != 0:
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
							rootdir = "Hercules/src"
							regex = re.compile(packet_id)
	
							packet_id2 = "0x" + packet_id[3:]
							regex2 = re.compile(packet_id2 + "[,);]")
	
							if packet_id in pvl_unknown:
						  		continue
	
							for root, dirs, files in os.walk(rootdir):
								for file in files:
									if re.search("Hercules/src/map/packets", root) or re.search("Hercules/src/common/packets", root) or re.search("packet", file) or re.search("messages", file):
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
	
	f = open("names.out", "w+")
	f.write(json.dumps(pvl))
	f.close()
	print("Packet names have been dumped to 'names.out'...")

def search_structs_file_for_packet(packet_id):
	f = open("Hercules/src/map/packets_struct.h", "r")
	lines = f.readlines()
	status("Reading for packet structs for packets in '{}'".format("packet_structs.h") + "")
	for idx in range(0, len(lines)):
		line = lines[idx]
		found = re.search(r"^DEFINE_PACKET_HEADER\(([A-Za-z0-9_]+), ([A-Za-z0-9]+)\);", line)
		if found:
			if found.group(2).upper() == packet_id.upper():
				return found.group(1)

	return ""

def packets_generator(CLIENTS, MIN_PACKET_VERSION, LAST_NAMED_COMMIT_YEAR, shuffle_files, len_files):
	print("Checking out revision 'HEAD' for packets generator!")
	wd = os.getcwd()
	os.chdir("Hercules")
	subprocess.check_output(['git', 'checkout', 'stable']).decode('ascii')
	os.chdir(wd)

	if os.path.isfile('names.out') == False:
		print("Error: names.out was not generated.")
		return

	with open('names.out') as names_json:
		pvl = json.load(names_json)
		#
		# Packet Version Length List
		#
		#
		pvl_unknown = dict()
		search_unknown = False
		try:
			for file in len_files:
				
				year = get_client_year(file)
	
				if LAST_NAMED_COMMIT_YEAR >= year:
					print("Last commit year " + str(LAST_NAMED_COMMIT_YEAR) + " is greater than " + str(year) + ", skipping...")
					continue
	
				print("opening file " + file);
				print(os.getcwd())
				f = open("Hercules/src/common/packets/" + file, "r")
				client_type = get_client_type(file)
				if CLIENTS[client_type] == False:
					continue
	
				ignore = False
				status("Searching for packet lengths in '{}'...".format(file))
				packet_version = create_base_version(get_client_year(file)) # this is the minimum client year that was captured, not 0. We dont default to zero.
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
							packet_version = create_base_version(get_client_year(file))
		
						rec = re.compile("packetLen\(([x0-9A-Za-z]+), ([0-9-]+)\)")
		
						found = rec.search(line)
		
						if found:
							packet_id = found.group(1)
							packet_len = found.group(2)
							packet_name = find_packet_name(pvl['z'], client_type, packet_id) # "0{}".format(found.group(1)[3:].upper())
							server = 'z'

							if re.search(r"clif", found.group(2)):
								packet_len = find_packet_length(pvl['z'], client_type, packet_id)
								if packet_len == "":
									packet_len = "unknown_length_placeholder"
							if packet_name == "":
								packet_name = search_structs_file_for_packet(packet_id)
								if packet_name == "":
									packet_name = "UNKNOWN_PACKET_PLACEHOLDER_{}".format(packet_id[-4:].upper())

		
							status("{} {} {}".format(packet_id, packet_len, packet_name))
		
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
							try:
								pvl[server][client_type][packet_version][packet_name] = { 'id': packet_id, 'len': packet_len }
							except:
								print("error: {} {} {} {}".format(server, packet_name, client_type, packet_version))
			print("Done.")
		except Exception:
			traceback.print_exc()
		
		f = open("packets.out", "w+")
		f.write(json.dumps(pvl))
		f.close()
		print("Packet tables have been dumped in json format to file 'packets.out'")

		if not os.path.isdir("Server"):
			os.mkdir("Server", 0o777)
		
		for server in sorted(iter(pvl.keys())):
			status("Writing packet handlers for " + get_server_name(server) + " server...")
		
			server_name = get_server_name(server)
		
			if not os.path.isdir("Server/" + server_name):
				os.mkdir("Server/" + server_name, 0o777)
		
			if not os.path.isdir("Server/" + server_name + "/Packets"):
				os.mkdir("Server/" + server_name + "/Packets", 0o777)
		
			create_packet_length_files(pvl, server)
			create_packet_definition_files(pvl, server)

##
# Unofficial Entry Point
##
print("Welcome to the Hercules2Horizon packet classes generator!")
print("All credits to -")
print("\tAuthor: Sephus")

name_generator(CLIENTS, MIN_PACKET_VERSION, LAST_NAMED_COMMIT_VER, LAST_NAMED_COMMIT_YEAR, shuffle_files, len_files)

packets_generator(CLIENTS, MIN_PACKET_VERSION, LAST_NAMED_COMMIT_YEAR, shuffle_files, len_files)
