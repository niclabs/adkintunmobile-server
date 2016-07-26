events_json = '''{
    "device_records": {
        "board": "DB8520H",
        "brand": "samsung",
        "build_id": "JZO54K.I8190LUBAMH1",
        "device": "golden",
        "hardware": "samsunggolden",
        "manufacturer": "samsung",
        "model": "GT-I8190L",
        "product": "goldenub",
        "release": "4.1.2",
        "release_type": "user",
        "sdk": 16,
        "device_id": "800000000000000000000",
        "app_version_code": "0.0a"
    },
    "sim_records": {
        "carrier_id": 1209,
        "serial_number": "800000000000000000000",
        "mcc": 120,
        "mnc": 9
    },
    "cdma_records": [],
    "gsm_records": [
        {
            "event_type": 16,
            "gsm_cid": 1259355,
            "gsm_lac": 55700,
            "gsm_psc": -1,
            "id": 523,
            "mcc": 120,
            "mnc": 9,
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
        }
    ],
    "state_records": [],
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
        }
        ],
    "connectivity_records": []
}
'''
