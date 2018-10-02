#!/bin/bash
sudo service mongod restart
pip install -r requirements.txt

# Launch UI Server
cd web_server
cd client
npm install
npm run build
cd ../server
npm install
npm start &

# Launch backend server
cd ../../backend_server
python3 service.py &

# Launch recommendation server
cd ../recommendation_service
python3 service.py &
python3 click_log_processor.py &

cd ../news_pipeline
python3 news_monitor.py &
python3 news_deduper.py &

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)
