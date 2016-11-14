events_json = '''{
    "device_records": {
        "board": "DB8520H",
        "brand": "samsung",
        "build_id": "JZO54K.I8190LUBAMH1",
        "device": "golden",
        "device_id": "8000000000000000000",
        "hardware": "samsunggolden",
        "manufacturer": "samsung",
        "model": "GT-I8190L",
        "product": "goldenub",
        "release": "4.1.2",
        "release_type": "user",
        "sdk": 16,
        "app_version_code": "0.0a"
    },
    "sim_records": {
        "serial_number": "8000000000000000000",
        "mcc": 730,
        "mnc": 2
    },
    "cdma_records": [],
    "gsm_records": [
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
            "id": 157,
            "mcc": 730,
            "mnc": 2,
            "network_type": 15,
            "tableName": "GSM_OBSERVATION_WRAPPER",
            "telephony_standard": 1,
            "timestamp": 1330641527625
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
            "state_type": 1,
            "timestamp": 1447019305132,
            "app_version_code": "1.1"
        }

    ],
    "telephony_records": [],
    "traffic_records":[
        {
            "event_type": 2,
            "id": 4603,
            "network_type": 1,
            "rx_bytes": 1234,
            "rx_packets": 45672,
            "tableName": "TRAFFIC_OBSERVATION_WRAPPER",
            "tcp_rx_bytes": 4687,
            "tcp_tx_bytes": 1357,
            "timestamp": 1330641500183,
            "tx_bytes": 489,
            "tx_packets": 35
        },
        {
            "event_type": 2,
            "id": 4603,
            "network_type": 1,
            "rx_bytes": 1234,
            "rx_packets": 45672,
            "tableName": "TRAFFIC_OBSERVATION_WRAPPER",
            "tcp_rx_bytes": 4687,
            "tcp_tx_bytes": 1357,
            "timestamp": 1330641500184,
            "tx_bytes": 489,
            "tx_packets": 35
        },
        {
            "event_type": 4,
            "id": 4609,
            "network_type": 6,
            "rx_bytes": 2361,
            "rx_packets": 19,
            "tableName": "TRAFFIC_OBSERVATION_WRAPPER",
            "tcp_rx_bytes": 4532,
            "tcp_tx_bytes": 1523,
            "timestamp": 1330641510326,
            "tx_bytes": 196,
            "tx_packets": 4
        },
        {
            "event_type": 4,
            "id": 4609,
            "network_type": 6,
            "rx_bytes": 2361,
            "rx_packets": 19,
            "tableName": "TRAFFIC_OBSERVATION_WRAPPER",
            "tcp_rx_bytes": 4532,
            "tcp_tx_bytes": 1523,
            "timestamp": 1330641510328,
            "tx_bytes": 196,
            "tx_packets": 4
        },
        {
            "event_type": 8,
            "id": 4604,
            "network_type": 6,
            "package_name": "cl.niclabs.adkintunmobile",
            "rx_bytes": 5143,
            "rx_packets": 1234,
            "tableName": "TRAFFIC_OBSERVATION_WRAPPER",
            "timestamp": 1330641500267,
            "tx_bytes": 5615,
            "tx_packets": 123,
            "uid": 10127
        },
        {
            "event_type": 8,
            "id": 4604,
            "network_type": 6,
            "package_name": "cl.niclabs.adkintunmobile",
            "rx_bytes": 5143,
            "rx_packets": 12345,
            "tableName": "TRAFFIC_OBSERVATION_WRAPPER",
            "timestamp": 1330641500269,
            "tx_bytes": 5615,
            "tx_packets": 123,
            "uid": 10127
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
        },
         {
            "available": true,
            "connected": true,
            "connection_type": 6,
            "detailed_state": 4,
            "event_type": 1,
            "id": 22,
            "roaming": false,
            "tableName": "CONNECTIVITY_OBSERVATION_WRAPPER",
            "timestamp": 1330641527544
        }
    ]
}
'''
