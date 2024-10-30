# whisper-api-self-hosted

## Install

### Installing core dependencies

```
sudo apt install python3 python3-pip -y

pip3 install virtualenv
```

### Create virtual environment

```python3 -m virtualenv venv```

## Run

```
source venv/bin/activate
```

```
uvicorn app:app --host 0.0.0.0 --port 8000
```