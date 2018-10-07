#!/bin/bash
sudo service mongod restart
pip install -r requirements.txt

# Launch backend server
cd backend_server
python3 service.py &

# Launch news modeling Server
cd ../news_topic_modeling_service
cd trainer
python3 news_trainer.py
cd ../server
python3 service.py &


# Launch recommendation server
cd ../../recommendation_service
python3 service.py &
python3 click_log_processor.py &

cd ../news_pipeline
python3 news_monitor.py &
python3 news_deduper.py &

# Launch UI Server
cd ../web_server
cd client
npm install
npm run build
cd ../server
npm install
npm start &

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)
