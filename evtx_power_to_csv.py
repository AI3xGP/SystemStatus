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
    "1074": "APAGADO"
}

if len(sys.argv) != 2:
    print("Uso: python3 evtx_power_to_csv.py <directorio_system_evtx>")
    sys.exit(1)

evtx_dir = sys.argv[1]
evtx_path = os.path.join(evtx_dir, "System.evtx")

if not os.path.isfile(evtx_path):
    print(f"Error: no se encontró System.evtx en {evtx_dir}")
    sys.exit(1)

with Evtx(evtx_path) as log, open("power_events.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["fecha", "estado"])

    for record in log.records():
        xml = ET.fromstring(record.xml())
        event_id = xml.find(".//EventID").text

        if event_id in EVENT_MAP:
            time = xml.find(".//TimeCreated").attrib["SystemTime"]
            estado = EVENT_MAP[event_id]
            writer.writerow([time, estado])

print("CSV generado: power_events.csv")

