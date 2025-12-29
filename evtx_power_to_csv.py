import sys
import os
import csv
from Evtx.Evtx import Evtx
import xml.etree.ElementTree as ET

EVENT_MAP = {
    "6005": "ENCENDIDO",
    "6006": "APAGADO",
    "6008": "APAGADO",
    "41":   "APAGADO",
    "1074": "APAGADO",
    "42":   "SUSPENDIDO",
    "1":    "REANUDADO"
}

if len(sys.argv) != 2:
    print("Uso: python3 evtx_power_to_csv.py <directorio_system_evtx>")
    sys.exit(1)

evtx_dir = sys.argv[1]
evtx_path = os.path.join(evtx_dir, "System.evtx")

if not os.path.isfile(evtx_path):
    print(f"Error: no se encontró System.evtx en {evtx_dir}")
    sys.exit(1)

def find_event_id(xml_root):
    for elem in xml_root.iter():
        if elem.tag.endswith("EventID"):
            return elem.text
    return None

def find_time(xml_root):
    for elem in xml_root.iter():
        if elem.tag.endswith("TimeCreated"):
            return elem.attrib.get("SystemTime")
    return None

with Evtx(evtx_path) as log, open("power_events.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["fecha", "estado"])

    for record in log.records():
        try:
            xml = ET.fromstring(record.xml())
        except ET.ParseError:
            continue

        event_id = find_event_id(xml)
        if event_id not in EVENT_MAP:
            continue

        time = find_time(xml)
        if not time:
            continue

        writer.writerow([time, EVENT_MAP[event_id]])

print("CSV generado correctamente con encendido, apagado y suspensión: power_events.csv")

