
# IP Address Reputation Scanning App

This is a Django Rest Framework project for scanning IP addresses using a background task queue (Celery) and sending real-time scan results to the frontend using WebSockets (Django Channels). 

## Project Overview

This project allows users to input multiple IP addresses, and for each IP address, the application fetches reputation data from an external API (`ipinfo.io`). The task of scanning each IP is handled asynchronously by Celery, while the results are sent back to the user in real-time using Django Channels.

## Features

- **Validate IP Addresses**: The app validates that only valid IP addresses are submitted.
- **Background Task Queue**: Each IP address is processed asynchronously using Celery.
- **Real-Time Updates**: As each IP address is scanned, the result is sent to the frontend using WebSockets.
- **REST API**: The API accepts a list of IP addresses and starts the scanning process.

## Tech Stack

- **Django**: The main framework for the backend.
- **Django Rest Framework (DRF)**: Used to create the API endpoints.
- **Celery**: A task queue to handle IP address scanning asynchronously.
- **Redis**: The message broker for Celery.
- **Django Channels**: Used to implement WebSockets for real-time communication.
- **ipinfo.io**: External API to retrieve IP address reputation data.

## Installation

### Prerequisites

Ensure that you have the following installed:

- Python 3.x
- Redis (for Celery)
- Virtualenv (recommended)

### Steps

1. **Clone the repository**:
   ```bash
   https://github.com/MahmoudBayoumi58/ip-address-reputation.git
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the requirements**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Redis (for Celery)**:
   Ensure that Redis is installed and running on `localhost:6379`. 

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

## Celery Configuration

Celery is used to run the background tasks for scanning each IP address asynchronously. To start the Celery worker:

```bash
celery -A ip_scanner worker --loglevel=info # linux
celery -A ip_scanner worker --loglevel=info --pool=solo # win
```


## Usage

1. **Submit IP addresses**: 
   Send a POST request with a list of IP addresses to the `/reputation/ips-scan/` endpoint.

   Example request:
   ```json
   {
     "ips": [
       "8.8.8.8",
       "1.1.1.1",
       "192.168.1.1"
     ]
   }
   ```

2. **Receive real-time results**:
   Once the IP addresses are submitted, the scan results will be sent via WebSocket to the connected frontend.

   Example WebSocket connection:
   ```javascript
   const socket = new WebSocket('ws://localhost:8000/ws/ip-check/');
   
   socket.onmessage = function(event) {
       const data = JSON.parse(event.data);
       console.log('Received:', data.message);
   };
   ```
   or check postman collection 

## Project Structure

```
ip-address-repuation/
├── ip_scanner/                  # Main Django project folder
│   ├── __init__.py
│   ├── asgi.py                  # ASGI configuration for Channels
│   ├── celery.py                # Celery configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── reputation_app/              # App handling IP reputation scanning
│   ├── __init__.py
│   ├── websocket/               # WebSocket consumers
│   │   ├── routing.py           # WebSocket routing
│   │   ├── consumers.py         # WebSocket consumers
│   ├── tasks.py                 # Celery tasks
│   ├── serializers.py           # DRF serializers for validating IPs
│   ├── views.py                 # API views
│   ├── routing.py               # WebSocket routing
├── manage.py                    # Django management script
```
