#!/bin/bash
# Start both backend servers

cd backend1
python server.py &
cd ../backend2
python server.py &
cd ..
echo "Both backends started on ports 5001 and 5002"