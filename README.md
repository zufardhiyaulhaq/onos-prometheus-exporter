# ONOS Prometheus Exporter
Custom Exporter for ONOS (Open Network Operating System). Show data **bytes/second** and **packets/second** via ONOS API and expose into Prometheus supported format.

## Instalation
```
git clone https://github.com/zufardhiyaulhaq/onos-prometheus-exporter
cd onos-prometheus-exporter
bash install.sh
```

## Custom ONOS configuration
You need to provide ONOS configuration to be able to get data via ONOS API. Edit ONOS configuration in **/opt/onos-prometheus-exporter/onos-config.json**. After that restart the services
```
sudo systemctl restart onos-exporter
```

