echo ""
echo ""
echo ""
# request 1
echo "Request 1: "
echo "curl http://localhost:5000/car/1"
echo ""
echo "Response 1: "
curl -I -s -L http://localhost:5000/car/1 | grep "HTTP/1"
curl http://localhost:5000/car/1
echo ""
echo ""

# request 2
echo "Request 2: "
echo "curl http://localhost:5000/car/"
echo ""
echo "Response 2: "
curl -I -s -L http://localhost:5000/car/ | grep "HTTP/1"
curl http://localhost:5000/car/
echo ""
echo ""


# request 3
echo "Request 3: "
echo "curl -d '{\"make\":\"Nissan\", \"model\":\"Micra\"}' -H \"Content-Type: application/json\" -X POST http://localhost:5000/avgprice/"
echo ""
echo "Response 3: "
curl -d '{"make":"Nissan", "model":"Micra"}' -H "Content-Type: application/json" -X POST http://localhost:5000/avgprice/ 
echo ""
echo ""

# request 4
echo "Request 4: "
echo "curl -d '{\"make\":\"Seat\", \"model\":\"Cordoba\", \"year\":\"2003\", \"chassis_id\":\"12345F\"}' -H \"Content-Type: application/json\" -X POST http://localhost:5000/car/ "
echo ""
echo "Response 4: "
curl -d '{"make":"Seat", "model":"Cordoba", "year":"2003", "chassis_id":"12345F"}' -H "Content-Type: application/json" -X POST http://localhost:5000/car/
echo ""
echo ""

