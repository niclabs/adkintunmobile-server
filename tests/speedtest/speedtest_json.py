reports_json = '''{
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
   "connectivitytest_records":[
      {
         "sites_results":[
            {
               "downloaded_bytes":4062383,
               "loaded":true,
               "loading_time":7027,
               "url":"http://www.lun.com",
               "id":1,
               "tableName":"SITE_RESULT"
            },
            {
               "downloaded_bytes":1684937,
               "loaded":true,
               "loading_time":9736,
               "url":"http://www.niclabs.cl",
               "id":2,
               "tableName":"SITE_RESULT"
            }
         ],
         "dispatched":false,
         "network_interface":{
            "active_interface":2,
            "bssid":"00:17:5a:1e:70:80",
            "gsm_cid":0,
            "gsm_lac":0,
            "network_type":0,
            "ssid":"'niclabs'",
            "id":5,
            "tableName":"NETWORK_INTERFACE"
         },
         "timestamp":1482341840760,
         "id":1,
         "tableName":"CONNECTIVITY_TEST_REPORT"
      }
   ],
   "mediatest_records":[
      {
         "video_id":"gPmbH8eCUj4",
         "video_results":[
            {
               "buffering_time":786,
               "downloaded_bytes":738322,
               "loaded_fraction":1.0,
               "quality":"144p",
               "id":1,
               "tableName":"VIDEO_RESULT"
            },
            {
               "buffering_time":667,
               "downloaded_bytes":606468,
               "loaded_fraction":1.0,
               "quality":"240p",
               "id":2,
               "tableName":"VIDEO_RESULT"
            },
            {
               "buffering_time":1016,
               "downloaded_bytes":1149602,
               "loaded_fraction":1.0,
               "quality":"480p",
               "id":3,
               "tableName":"VIDEO_RESULT"
            }
         ],
         "dispatched":false,
         "network_interface":{
            "active_interface":2,
            "bssid":"00:17:5a:1e:70:80",
            "gsm_cid":0,
            "gsm_lac":0,
            "network_type":0,
            "ssid":"'niclabs'",
            "id":3,
            "tableName":"NETWORK_INTERFACE"
         },
         "timestamp":1482341724349,
         "id":1,
         "tableName":"MEDIA_TEST_REPORT"
      }
   ],
   "speedtest_records":[
      {
         "download_size":1000000,
         "download_speed":9965900.0,
         "elapsed_download_time":838,
         "elapsed_upload_time":798,
         "host":"http://blasco.duckdns.org",
         "upload_size":1000000,
         "upload_speed":9854887.0,
         "dispatched":false,
         "network_interface":{
            "active_interface":2,
            "bssid":"00:17:5a:1e:70:80",
            "gsm_cid":0,
            "gsm_lac":0,
            "network_type":0,
            "ssid":"'niclabs'",
            "id":1,
            "tableName":"NETWORK_INTERFACE"
         },
         "timestamp":1482341701645,
         "id":1,
         "tableName":"SPEED_TEST_REPORT"
      }
   ]
}'''
