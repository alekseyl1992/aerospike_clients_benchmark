const Aerospike = require('aerospike');
const Key = Aerospike.Key;

const express = require('express');
const _ = require('lodash');

const config = {
    hosts: '127.0.0.1:3000',
    maxConnsPerNode: 1000000
};

const app = express();
const ns = 'test';

function connectToAerospike() {
    Aerospike.connect(config, (error, client) => {
        if (error)
            throw error;

        console.log('Connected to Aerospike');

        app.get('/', function (req, res) {
            res.send('Hello World!' + _.random(0, 100));
        });

        app.get('/user', function (req, res) {
            const query = client.query(ns, 'sessions');
            const _from = _.random(0, 100);
            const to = 100;
            query.where(Aerospike.filter.range('expires', _from, to));

            let results = [];

            const stream = query.foreach();
            stream.on('error', (error) => {
                console.error(error);
                throw error;
            });

            let done = false;
            let remaining = 0;

            stream.on('data', (session) => {
                ++remaining;
                const key = new Key(ns, 'users', session['nick']);
                client.get(key, (error, user, meta) => {
                    --remaining;
                    if (error) {
                        console.log(error);
                        throw error;
                    }

                    results.push(user['email']);

                    if (done && remaining == 0) {
                        res.json({
                            data: results,
                            version: 1,
                            date: new Date()
                        });
                    }
                });
            });

            stream.on('end', () => {
                done = true;
                if (remaining == 0) {
                    res.json({
                        data: results,
                        version: 1,
                        date: new Date()
                    });
                }
            });
        });
    });
}

const port = 8081;
app.listen(8081, function () {
    console.log(`Sever started on port ${port}`);
    connectToAerospike();
});
