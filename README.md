# HTTP POST Log Viewer

A lightweight tool to capture and display HTTP POST request details in real time.
Run it directly with **Python** or deploy easily with **Docker**.

## ✨ Features

* 📡 Logs all incoming HTTP POST requests
* ⏱ Real-time request monitoring
* 🐍 Simple Python script, no heavy dependencies
* 🐳 Docker support for quick deployment
* 🔐 Bearer authentication

## 🚀 Usage

### Run with Python

```bash
# Clone the repository
git clone https://github.com/yourname/http-post-log-viewer.git
cd http-post-log-viewer

# A fictional secret token for the example
export AUTH_TOKEN="abc123-very-secret-token-xyz789"

# Start the server
python server.py
```

### Run with Docker

```bash
# Build the image
docker build -t http-post-log-viewer .

# A fictional secret token for the example
export AUTH_TOKEN="abc123-very-secret-token-xyz789"

# Run the container
docker run -d -p 3000:3000 \
  -e AUTH_TOKEN="$AUTH_TOKEN" \
  --name request-logger-container \
  http-post-log-viewer
```

## 📖 Example

Send a POST request:

```bash
curl  -X POST -d "key1=value1&key2=value2" http://localhost:3000 -H "Authorization: Bearer $AUTH_TOKEN"
```

You will see the logged details in real time.
