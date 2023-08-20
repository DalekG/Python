import os
import sqlite3
import secrets
import string
import xml.etree.ElementTree as ET
from typing import Iterator

class NmapDB:
    """
    A simple wrapper for db operations.
    """
    def __init__(self) -> None:
        self.db_file = '/tmp/' + ''.join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(5)) + '.db'
        self.con = sqlite3.connect(self.db_file)
        self.cur = self.con.cursor()
        self.cur.execute('''
            CREATE TABLE open_ports(
                o1 INT, o2 INT, o3 INT, o4 INT, port INT, hostname, os,
                proto, service, product,
                PRIMARY KEY (o1, o2, o3, o4, port))
        ''')

    def __del__(self) -> None:
        os.remove(self.db_file)

    def populate(self, data: dict) -> None:
        """
        Inserts a given port information into the database.
        The IP is split into four columns for easy sorting.
        """
        octet = data['ip'].split('.')
        for x in range(4):
            data[f'o{x+1}'] = octet[x]
        
        self.cur.execute('''
            INSERT OR IGNORE INTO open_ports VALUES(
                :o1, :o2, :o3, :o4, :port, :hostname, :os,
                :proto, :service, :product)
        ''', data)
        self.con.commit()

    def dump_to_csv(self, output_file) -> None:
        """
        Sorts, appends a sort integer column, and saves results to the
        given csv file.
        """
        select = '''
            SELECT
                ROW_NUMBER() OVER (
                    ORDER BY o1, o2, o3, o4, port
                ) AS Sort,
                o1 || '.' || o2 || '.' || o3 || '.' || o4 AS IP,
                '' AS Technology,
                '' AS Findings,
                '' AS Notes,
                port AS Port,
                service AS Service,
                hostname AS Host,
                os AS OS,
                proto AS Proto,
                product AS Product
            FROM open_ports
        '''
        os.system(f'sqlite3 -header -csv {self.db_file} "{select}" \
                  > {output_file}')

def get_ports(xml_path: str) -> Iterator[dict]:
    """
    Retrieves port data from an nmap xml.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for host in root.findall('host/status[@state="up"]/..'):
        ip = host.find('address[@addrtype="ipv4"]').get('addr')
        el_host = host.find('hostnames/hostname[@name]')
        hostname = el_host.get('name') if el_host else ''
        el_os = host.find('os/osmatch')
        osname = el_os.get('name') if el_os else ''

        for port in host.findall('ports/port/state[@state="open"]/..'):
            el_srv = port.find('service')
            
            yield {
                'ip': ip,
                'hostname': hostname,
                'os': osname,
                'port': port.get('portid'),
                'proto': port.get('protocol'),
                'service': el_srv.get('name') if el_srv else '',
                'product': el_srv.get('product') if el_srv else ''
            }

def list_files(file_path: str) -> set[str]:
    """
    Retrieves absolute path(s) for a given file or directory of xml files.
    """
    if os.path.isfile(file_path):
        return {os.path.abspath(file_path)}
    else:
        return set([
            os.path.abspath(os.path.join(file_path, f))
            for f in os.listdir(file_path)
            if f.lower().endswith('.xml')
        ])

if __name__ == '__main__':
    file_paths = set()
    while True:
        file_path = input("Enter the path of the XML file or directory to combine (or 'done' to finish): ")
        if file_path.lower() == 'done':
            break
        if not os.path.exists(file_path):
            print("File/dir not found. Please enter a valid file path.")
            continue
        file_paths |= list_files(file_path)

    output_filename = input("Enter the filename for the combined CSV file: ")

    db = NmapDB()
    for xml_file in file_paths:
        for port in get_ports(xml_file):
            db.populate(port)
    db.dump_to_csv(output_filename)
