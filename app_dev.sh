#!/bin/bash

VENV_NAME="wms_venv"
PYTHON_VERSION="python3"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Starting WMS Development Environment...${NC}"

create_venv_if_missing() {
    if [ ! -d "$VENV_NAME" ]; then
        echo -e "${YELLOW}Virtual environment not found. Creating '$VENV_NAME'...${NC}"
        $PYTHON_VERSION -m venv $VENV_NAME
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to create virtual environment. Make sure python3-venv is installed.${NC}"
            echo -e "${YELLOW}Try: sudo apt install python3-venv (Ubuntu/Debian) or equivalent${NC}"
            exit 1
        fi
        echo -e "${GREEN}Virtual environment created successfully.${NC}"
    fi
}

activate_venv() {
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source $VENV_NAME/bin/activate
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to activate virtual environment${NC}"
        exit 1
    fi
    echo -e "${GREEN}Virtual environment activated. Using Python: $(which python)${NC}"
}

create_venv_if_missing
activate_venv

echo -e "${YELLOW}Upgrading pip...${NC}"
python -m pip install --upgrade pip

echo -e "${YELLOW}Starting backend API...${NC}"
if [ -d "wms_api" ]; then
    cd wms_api || exit
    if [ -f "requirements.txt" ]; then
        echo -e "${YELLOW}Installing backend dependencies...${NC}"
        python -m pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to install backend dependencies${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}No requirements.txt found in wms_api directory${NC}"
    fi
    
    echo -e "${GREEN}Starting Django backend server...${NC}"
    python manage.py runserver --settings='wms_api.settings.development' &
    BACKEND_PID=$!
    cd ..
else
    echo -e "${RED}wms_api directory not found${NC}"
    exit 1
fi

echo -e "${YELLOW}Starting frontend...${NC}"
if [ -d "wms_frontend" ]; then
    cd wms_frontend || exit
    if [ -f "requirements.txt" ]; then
        echo -e "${YELLOW}Installing frontend dependencies...${NC}"
        python -m pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to install frontend dependencies${NC}"
            kill $BACKEND_PID
            exit 1
        fi
    else
        echo -e "${YELLOW}No requirements.txt found in wms_frontend directory${NC}"
    fi
    
    echo -e "${GREEN}Starting Django frontend server...${NC}"
    python manage.py runserver 0.0.0.0:3000 --settings='wms_frontend.settings.development' &
    FRONTEND_PID=$!
    cd ..
else
    echo -e "${RED}wms_frontend directory not found${NC}"
    kill $BACKEND_PID
    exit 1
fi

echo -e "${GREEN}Both servers started successfully!${NC}"
echo -e "${GREEN}Backend API: http://localhost:8000${NC}"
echo -e "${GREEN}Frontend: http://localhost:3000${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"

trap "echo -e '${YELLOW}Stopping servers...${NC}'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo -e '${GREEN}Servers stopped.${NC}'; exit 0" SIGINT SIGTERM

wait