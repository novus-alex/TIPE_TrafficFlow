import xml.etree.ElementTree as ET
import requests

class BF:
    xml_url = "http://tipi.bison-fute.gouv.fr/bison-fute-ouvert/publicationsDIR/QTV-DIR/qtvDir.xml"

class XML:
    def __init__(self, url):
        self.xml_file = requests.get(url)
        with open('tmp.xml', 'w+') as _f:
            _f.write(self.xml_file.content.decode())
        self.xml_cont = ET.parse('tmp.xml')
        self.data = {}

    def parse_xml(self):
        '''

        Data type:
            data[id_of_station] = [time, cars_nbr, flowrate, speed]
        
        '''

        for elem in self.xml_cont.getroot():
            for sub in elem:
                if "siteMeasurements" in sub.tag:
                    id = "N/A"; time = "N/A"; flowrate = "N/A"; speed = "N/A"
                    for mes in sub:
                        if "measurementSiteReference" in mes.tag:
                            id = mes.attrib.get('id')
                        elif "measurementTimeDefault" in mes.tag:
                            time = mes.text
                        elif "measuredValue" in mes.tag:
                            for val in mes:
                                for basic in val:
                                    if "TrafficFlow" in list(basic.attrib.items())[0]:
                                        for tab in basic:
                                            cars_nbr = tab.attrib.get('numberOfInputValuesUsed')
                                            for flow in tab:
                                                flowrate = flow.text
                                    else:
                                        for tab in basic:
                                            for sp in tab:
                                                speed = sp.text
                    self.data[id] = [time, cars_nbr, flowrate, speed]

    def to_csv(self, filename):
        with open(filename, 'w+') as _f:
            _f.write("")
        with open(filename, "a") as _f:
            _f.write("ID;Time;Nbr_Voitures;Flowrate;Speed\n")
            for id in self.data.keys():
                data = self.data.get(id)
                _f.write(f"{id};{data[0]};{data[1]};{data[2]};{data[3]}\n")



