#!/bin/bash

PYTHON="/usr/bin/python3"

cd wms_api || exit
$PYTHON -m pip install -r requirements.txt
$PYTHON manage.py runserver --settings='wms_api.settings.development' &
BACKEND_PID=$!

cd ../wms_frontend || exit
$PYTHON -m pip install -r requirements.txt
$PYTHON manage.py runserver 0.0.0.0:3000 --settings='wms_frontend.settings.development' &
FRONTEND_PID=$!

trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID" SIGINT SIGTERM
wait
