# whisper-api-self-hosted

## Install

### Installing core dependencies

```
sudo apt install python3 python3-pip -y

pip3 install virtualenv
```

### Virtual virtual environment

Create

```python3 -m virtualenv venv```

Run

```
source venv/bin/activate
```

### Install dependencies

```
pip3 install -r requirements.txt
```

# Run

```
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Systemd instalation

#### **Step 1: Create a Startup Script**

First, create a shell script that activates your virtual environment and starts the Uvicorn server.

1. **Create the script file**:

```bash
sudo nano start_server.sh
```

2. **Add the following content**:

   ```bash
   #!/bin/bash

   # Activate the virtual environment
   source venv/bin/activate

   # Run the Uvicorn server
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

3. **Make the script executable**:

   ```bash
   chmod +x start_server.sh
   ```

#### **Step 2: Create a `systemd` Service File**

(as root)

1. **Create the service file**:

   ```bash
   sudo nano /etc/systemd/system/whisper_api.service
   ```

2. **Add the following content**:

```ini
[Unit]
Description=Whisper API FastAPI Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/whisper-api-self-hosted
ExecStart=/bin/bash /var/www/whisper-api-self-hosted/start_server.sh
Restart=always
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/path/to/your/venv/bin:/var/www/whisper-api-self-hosted/venv/bin"

[Install]
WantedBy=multi-user.target
```

#### **Step 3: Reload `systemd` and Start the Service**

1. **Reload the `systemd` daemon**:

```bash
sudo systemctl daemon-reload
```

2. **Start the service**:

```bash
sudo systemctl start whisper_api.service
```

3. **Enable the service to start on boot**:

```bash
sudo systemctl enable whisper_api.service
```

#### **Step 4: Verify the Service**

1. **Check the status**:

```bash
sudo systemctl status whisper_api.service
```

   - You should see that the service is **active (running)**.
   - If there are errors, they will be displayed here for troubleshooting.

2. **View logs (optional)**:

```bash
sudo journalctl -u whisper_api.service -f
```

#### **Step 5: Managing the Service**

- **Stop the service**:

  ```bash
  sudo systemctl stop whisper_api.service
  ```

- **Restart the service**:

  ```bash
  sudo systemctl restart whisper_api.service
  ```