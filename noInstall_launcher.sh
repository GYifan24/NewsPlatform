#!/bin/bash
# pip install -r requirements.txt

# Launch UI Server
cd web_server
cd server
npm start &

# Launch backend server
cd ../../backend_server
python3 service.py &

# Launch recommendation server
cd ../recommendation_service
python3 service.py &
python3 click_log_processor.py &

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)
