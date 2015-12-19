#!/usr/bin/env python2

import subprocess
import re
import time
import sys


def get_state():
    output = subprocess.Popen(["aconnect", "-l"], stdout=subprocess.PIPE).communicate()[0]
    output += "\n"

    connections = []
    clients = {}

    client = {}

    last_port = None

    lines = output.split("\n")
    for line in lines:
        m = re.match(r"client (\d+): '(.*)' ", line)
        if m or (line == ""):
            if len(client.keys()) > 0:
                id = client['id']
                del client['id']
                clients[id] = client
            
            client = {}
            if m:
                client['id'] = int(m.group(1))
                client['name'] = m.group(2)
                client['ports'] = {}
                last_port = None

        m = re.match(r"\ *(\d+) '(.*)'", line)
        if m:
            port_id = int(m.group(1))
            port_name = m.group(2).strip()
            client['ports'][port_id] = port_name

            last_port = "%d:%d" % (client['id'], port_id)

        m = re.match(r".*Connecting To: (\d+):(\d+)", line)
        if m:
            other_port = "%s:%s" % (m.group(1), m.group(2))
            connections.append((last_port, other_port))

    return (clients, connections)


def connect(p_from, p_to):
    subprocess.call(["aconnect", p_from, p_to])


def find_port(clients, port_name):
    client_name = None
    if "/" in port_name:
        a = port_name.split("/")
        client_name = a[0]
        port_name = a[1]

    for id in clients.keys():
        if client_name is not None:
            if not re.match(client_name, clients[id]['name']):
                continue

        ports = clients[id]['ports']
        for id2 in ports.keys():
            if re.match(port_name, ports[id2]):
                return "%d:%d" % (id, id2)

def main():
    if len(sys.argv) != 3:
        print "Usage: %s <port_from> <port_to>" % sys.argv[0]
        return

    port_from = sys.argv[1]
    port_to = sys.argv[2]
    while True:
        time.sleep(2)

        (clients, connections) = get_state()

        p_from = find_port(clients, port_from)
        p_to = find_port(clients, port_to)
        
        if (p_from is None) or (p_to is None):
            continue

        t = (p_from, p_to)
        if t in connections:
            continue

        print "Connecting %s and %s..." % (p_from, p_to)
        connect(p_from, p_to)

 
if __name__=="__main__":
    main()
