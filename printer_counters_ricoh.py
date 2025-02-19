####
# Script de relève des compteurs d'impression Ricoh
####
# Copyright (C) 2025 Noël MARTINON
# License GPL v2
#
# Requis : apt install python3-easysnmp
####
#
# Usage : python3 printer_counters_ricoh.py > `date +%Y%m%d_%H%M%S`.csv
#
####

from easysnmp import Session
import array as arr
import sys

printers = ['192.168.1.30', '192.168.1.31', '192.168.1.32']

def query(ip):
    session = Session(hostname=ip, community='public', version=2, use_sprint_value=False, timeout=5)
    #system_items = session.walk() #SNMPv2-MIB::system
    #for item in system_items:
    #    print('{oid}.{oid_index} {snmp_type} = {value}'.format(
    #        oid=item.oid,
    #        oid_index=item.oid_index,
    #        snmp_type=item.snmp_type,
    #        value=item.value
    #    ))

    ret = [ip, 'ERROR']
    name = session.get('.1.3.6.1.2.1.1.5.0').value
    serial = session.get('.1.3.6.1.2.1.43.5.1.1.17.1').value
    hostname = session.get('.1.3.6.1.4.1.367.3.2.1.6.1.1.7.1').value

    if name != 'SP C352DN':
        # Copieur
        counterColorCopier = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.62').value
        counterColorCopierTxt = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.6.62').value

        counterBWCopier = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.63').value
        counterBWCopierTxt = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.6.63').value

        counterMonoCopier = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.64').value
        counterMonoCopierTxt = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.6.64').value

        counterBiCopier = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.65').value
        counterBiCopierTxt = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.6.65').value

        counterColorPrinter = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.66').value
        counterColorPrinterTxt = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.6.66').value

        counterBWPrinter = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.67').value
        counterBWPrinterTxt = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.6.67').value

        counterMonoPrinter = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.68').value
        counterMonoPrinterTxt = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.6.68').value

        counterBiPrinter = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.69').value
        counterBiPrinterTxt = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.6.69').value

        counterBWFax = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.36').value
        counterBWFaxTxt = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.6.36').value

        ret = [hostname, name, serial, ip,
            counterBWPrinter,
            counterColorPrinter,
            counterMonoPrinter,
            counterBiPrinter,
            counterBWCopier,
            counterColorCopier,
            counterMonoCopier,
            counterBiCopier,
            counterBWFax,
            int(counterBWPrinter) + int(counterBWCopier) + int(counterBWFax),
            int(counterColorPrinter) + int(counterMonoPrinter) + int(counterBiPrinter) + int(counterColorCopier) + int(counterMonoCopier) + int(counterBiCopier)
            ]
    else:
        # Imprimante
        counterColorPrinter = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.17').value
        counterColorPrinterTxt = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.6.17').value

        counterBWPrinter = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.29').value
        counterBWPrinterTxt = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.6.29').value

        counterMonoPrinter = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.47').value
        counterMonoPrinterTxt = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.6.47').value

        counterBiPrinter = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.9.48').value
        counterBiPrinterTxt = session.get('.1.3.6.1.4.1.367.3.2.1.2.19.5.1.6.48').value

        ret = [hostname, name, serial, ip,
            counterBWPrinter,
            counterColorPrinter,
            counterMonoPrinter,
            counterBiPrinter
            ]

    return ret


def main():
    headers = ['Nom', 'Modele', 'Num. serie', 'Adresse IP',
            'Imprimante : Noir & Blanc',
            'Imprimante : Pleine couleur',
            'Imprimante : Monochromie',
            'Imprimante : Bichromie',
            'Copieur : Noir & Blanc',
            'Copieur : Pleine couleur',
            'Copieur : Monochromie',
            'Copieur : Bichromie',
            'Fax : Noir & Blanc',
            'Total noir',
            'Total couleur'
            ]

    headers_len = len(headers) - 1
    for index, item in enumerate(headers):
        print(item, end='\n' if index == headers_len else '\t')

    for printer in printers:
        try:
            data = query(printer)
            data_len = len(data) - 1
            for index, item in enumerate(data):
                print(item, end='\n' if index == data_len else '\t')
        except KeyboardInterrupt:
            sys.exit()
        except:
            continue

if __name__ == "__main__":
    main()

