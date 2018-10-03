import time
import json
import requests

from requests.auth import HTTPBasicAuth
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

class onos():
    def __init__(self,ip,username,password):
        self.ip = ip
        self.username = username
        self.password = password
    
    def get_data(self,path):
        url = 'http://'+self.ip+':8181/onos/v1'+path
        data = requests.get(url, auth=HTTPBasicAuth(self.username,self.password)).text
        return json.loads(data)
    
    def get_devices(self):
        data = []
        tmp = self.get_data('/devices')
        for device in tmp['devices']:
            data.append(device['id'])
        return data

    class devices():
        def __init__(self,id, outer_instance):
            self.id = id
            self.outer_instance = outer_instance
        
        def get_statistic(self):
            data = self.outer_instance.get_data('/statistics/ports/'+self.id)
            return data

class prometheusCollector():
    
    def calculation(self,data_0,data_1):
        data = data_1
        port_length = len(data['ports'])
        for number in range(0,port_length):
            data["ports"][number]["packetsReceived"] = data_1["ports"][number]["packetsReceived"] - data_0["ports"][number]["packetsReceived"]
            data["ports"][number]["packetsSent"] = data_1["ports"][number]["packetsSent"] - data_0["ports"][number]["packetsSent"]
            data["ports"][number]["bytesReceived"] = data_1["ports"][number]["bytesReceived"] - data_0["ports"][number]["bytesReceived"]
            data["ports"][number]["bytesSent"] = data_1["ports"][number]["bytesSent"] - data_0["ports"][number]["bytesSent"]
        return data

    def collect(self):

        self.metric = {}
        self.metric = {
        'packetsReceived': GaugeMetricFamily('onos_device_packets_received','packet received per seconds', labels=["node","port"]),
        'packetsSent': GaugeMetricFamily('onos_device_packets_sent','packet sends per seconds', labels=["node","port"]),
        'bytesReceived': GaugeMetricFamily('onos_device_bytes_received','bytes received per seconds', labels=["node","port"]),
        'bytesSent': GaugeMetricFamily('onos_device_bytes_sent','bytes sends per seconds', labels=["node","port"])
        }

        onos_config = json.loads(open("onos-config.json","r").read())
        onos_instance = onos(onos_config["ipaddress"],onos_config["username"],onos_config["password"])
        device_data = onos_instance.get_devices()
        
        for line in device_data:
            device = onos_instance.devices(line,onos_instance)
            data_0 = device.get_statistic()["statistics"][0]
            time.sleep(5)
            data_1 = device.get_statistic()["statistics"][0]
            data = self.calculation(data_0,data_1)
        
            port_length = len(data['ports'])
            for number in range(0,port_length):
                self.metric['packetsReceived'].add_metric([data["device"],str(data["ports"][number]['port'])], data["ports"][number]["packetsReceived"])
                self.metric['packetsSent'].add_metric([data["device"],str(data["ports"][number]['port'])], data["ports"][number]["packetsSent"])
                self.metric['bytesReceived'].add_metric([data["device"],str(data["ports"][number]['port'])], data["ports"][number]["bytesReceived"])
                self.metric['bytesSent'].add_metric([data["device"],str(data["ports"][number]['port'])], data["ports"][number]["bytesSent"])

        for metric in self.metric.values():
            yield metric

if __name__ == "__main__":

    REGISTRY.register(prometheusCollector())
    start_http_server(9090)
    
    while True:
        time.sleep(1)
    

