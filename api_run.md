Run the API Server APP : python iperf3_api.py &

curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/server/create -d '{"name":"server1"}'
curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/server/server1/run -d '{}'
curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/client/create -d '{"name":"client1"}'
curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/client/client1/run -d '{}'
