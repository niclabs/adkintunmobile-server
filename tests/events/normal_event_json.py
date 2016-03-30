events_json = '''{
    "device_records": {
        "board": "DB8520H",
        "brand": "samsung",
        "build_id": "JZO54K.I8190LUBAMH1",
        "device": "golden",
        "device_id": "355258057810793",
        "hardware": "samsunggolden",
        "manufacturer": "samsung",
        "model": "GT-I8190L",
        "product": "goldenub",
        "release": "4.1.2",
        "release_type": "user",
        "sdk": 16
    },
    "sim_records": {
        "carrier_id": "73008",
        "serial_number": "8956080124002959472"
    },
    "cdma_records": [],
    "gsm_records": [
        {
            "event_type": 16,
            "gsm_cid": 1277982,
            "gsm_lac": 55700,
            "gsm_psc": -1,
            "id": 523,
            "mcc": 730,
            "mnc": 2,
            "network_type": 16,
            "signal_strength": {
                "id": 490,
                "mean": -79.0,
                "size": 1,
                "tableName": "SAMPLE_WRAPPER",
                "variance": 0.0
            },
            "tableName": "GSM_OBSERVATION_WRAPPER",
            "telephony_standard": 1,
            "timestamp": 1447019305848
        },
        {
            "event_type": 16,
            "gsm_cid": 1259355,
            "gsm_lac": 55700,
            "gsm_psc": -1,
            "id": 157,
            "mcc": 730,
            "mnc": 2,
            "network_type": 15,
            "tableName": "GSM_OBSERVATION_WRAPPER",
            "telephony_standard": 1,
            "timestamp": 1330641527620
        },
        {
            "event_type": 16,
            "gsm_cid": 1259355,
            "gsm_lac": 55700,
            "gsm_psc": -1,
            "id": 158,
            "mcc": 730,
            "mnc": 2,
            "network_type": 15,
            "tableName": "GSM_OBSERVATION_WRAPPER",
            "telephony_standard": 1,
            "timestamp": 1330641527661
        }
    ],
    "state_records": [
        {
            "event_type": 16,
            "state": 1,
            "state_type": 1,
            "timestamp": 1447019305131,
            "app_version_code": "1.1"
        },
        {
            "event_type": 16,
            "state": 1,
            "state_type": 2,
            "timestamp": 1447019305832,
            "app_version_code": "1.1"
        }
    ],
    "telephony_records": [],
    "traffic_records":[
        {
            "event_type": 2,
            "id": 4603,
            "network_type": 1,
            "rx_bytes": 0,
            "rx_packets": 0,
            "tableName": "TRAFFIC_OBSERVATION_WRAPPER",
            "tcp_rx_bytes": 0,
            "tcp_tx_bytes": 0,
            "timestamp": 1330641500183,
            "tx_bytes": 0,
            "tx_packets": 0
        },
        {
            "event_type": 8,
            "id": 4604,
            "network_type": 6,
            "package_name": "cl.niclabs.adkintunmobile",
            "rx_bytes": 0,
            "rx_packets": 0,
            "tableName": "TRAFFIC_OBSERVATION_WRAPPER",
            "timestamp": 1330641500267,
            "tx_bytes": 5615,
            "tx_packets": 0,
            "uid": 10127
        },
        {
            "event_type": 8,
            "id": 4605,
            "network_type": 6,
            "package_name": "com.google.uid.shared:10016",
            "rx_bytes": 15252,
            "rx_packets": 0,
            "tableName": "TRAFFIC_OBSERVATION_WRAPPER",
            "timestamp": 1330641500297,
            "tx_bytes": 928,
            "tx_packets": 0,
            "uid": 10016
        },
        {
            "event_type": 8,
            "id": 4606,
            "network_type": 6,
            "package_name": "com.google.android.talk",
            "rx_bytes": 15140,
            "rx_packets": 0,
            "tableName": "TRAFFIC_OBSERVATION_WRAPPER",
            "timestamp": 1330641500334,
            "tx_bytes": 916,
            "tx_packets": 0,
            "uid": 10098
        },
        {
            "event_type": 4,
            "id": 4607,
            "network_type": 6,
            "rx_bytes": 43966,
            "rx_packets": 67,
            "tableName": "TRAFFIC_OBSERVATION_WRAPPER",
            "tcp_rx_bytes": 30392,
            "tcp_tx_bytes": 7459,
            "timestamp": 1330641500384,
            "tx_bytes": 10400,
            "tx_packets": 80
        },
        {
            "event_type": 2,
            "id": 4608,
            "network_type": 1,
            "rx_bytes": 0,
            "rx_packets": 0,
            "tableName": "TRAFFIC_OBSERVATION_WRAPPER",
            "tcp_rx_bytes": 0,
            "tcp_tx_bytes": 0,
            "timestamp": 1330641510184,
            "tx_bytes": 0,
            "tx_packets": 0
        },
        {
            "event_type": 4,
            "id": 4609,
            "network_type": 6,
            "rx_bytes": 2361,
            "rx_packets": 19,
            "tableName": "TRAFFIC_OBSERVATION_WRAPPER",
            "tcp_rx_bytes": 0,
            "tcp_tx_bytes": 0,
            "timestamp": 1330641510326,
            "tx_bytes": 196,
            "tx_packets": 4
        },
        {
            "event_type": 2,
            "id": 4610,
            "network_type": 1,
            "rx_bytes": 0,
            "rx_packets": 0,
            "tableName": "TRAFFIC_OBSERVATION_WRAPPER",
            "tcp_rx_bytes": 0,
            "tcp_tx_bytes": 0,
            "timestamp": 1330641527513,
            "tx_bytes": 0,
            "tx_packets": 0
        },
        {
            "event_type": 4,
            "id": 4611,
            "network_type": 6,
            "rx_bytes": 576,
            "rx_packets": 1,
            "tableName": "TRAFFIC_OBSERVATION_WRAPPER",
            "tcp_rx_bytes": 0,
            "tcp_tx_bytes": 0,
            "timestamp": 1330641527636,
            "tx_bytes": 0,
            "tx_packets": 0
        }
    ],
    "connectivity_records": [
        {
            "available": true,
            "connected": true,
            "connection_type": 6,
            "detailed_state": 4,
            "event_type": 1,
            "id": 22,
            "roaming": false,
            "tableName": "CONNECTIVITY_OBSERVATION_WRAPPER",
            "timestamp": 1330641527540
        }
    ]
}
'''
