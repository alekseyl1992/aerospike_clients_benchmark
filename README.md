# Prepare
* Install python 3.4 or above
* Install NodeJS 6 or above
* Install Aerospike
* Fill DB with random data
  * python fill_db.py
* Create index:
  * `CREATE INDEX expiresindex ON test.sessions (expires) NUMERIC`
* Install benchmarking tool, ex: weighttp

# Tornado + sync client
* `cd torn`
* `pip install -r requirements.txt`
* `python main.py`
* `weighttp -n 10000 -t 4 -c 4 127.0.0.1:8080`

## Results
finished in 6 sec, 916 millisec and 121 microsec, 1445 req/s, 294 kbyte/s
requests: 10000 total, 10000 started, 10000 done, 10000 succeeded, 0 failed, 0 errored
status codes: 10000 2xx, 0 3xx, 0 4xx, 0 5xx
traffic: 2089108 bytes total, 1950000 bytes http, 139108 bytes data

# NodeJS + async client
* `cd node`
* `npm install`
* `nodejs main.js`
* `weighttp -n 10000 -t 4 -c 4 127.0.0.1:8081`

## Results
finished in 3 sec, 295 millisec and 444 microsec, 3034 req/s, 616 kbyte/s
requests: 10000 total, 10000 started, 10000 done, 10000 succeeded, 0 failed, 0 errored
status codes: 10000 2xx, 0 3xx, 0 4xx, 0 5xx
traffic: 2079079 bytes total, 1940000 bytes http, 139079 bytes data
