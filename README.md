## **Ethereum Deposit Tracker**


The Ethereum Deposit Tracker is a real-time monitoring tool designed to observe deposit events on the Ethereum Beacon Chain. 

It listens for deposit events, stores data in MongoDB, and provides visualization and metrics collection using Prometheus and Grafana. Additionally, the tracker sends instant notifications to a Telegram chat when new deposits are detected, making it a valuable tool for blockchain analysts and Ethereum enthusiasts.<br>

**Features**

*Real-Time Deposit Monitoring:* Continuously listens for deposit events from the Ethereum Beacon Chain contract.<br>

*Telegram Notifications:* Sends alerts to a list of registered chat IDs via Telegram for every new deposit event.

*Detailed Logging:* Logs critical actions like deposit detection, errors, and notifications.

*Metrics Collection:* Tracks key metrics with Prometheus for data analysis.

*Data Storage:* Stores detailed deposit data in MongoDB for historical analysis.

*Visualization:* Creates real-time visual dashboards with Grafana for easy monitoring.


### _Prerequisites_

Before you begin, ensure you have the following installed:

Python 3.8+: The programming language.

pip: Python package installer to install dependencies.

MongoDB: NoSQL database for storing Ethereum deposit data.

Prometheus: A metrics collection tool.

Grafana: Visualization and dashboard tool.

Alchemy: A platform that simplifies and enhances the development of blockchain applications.

Infura: A development suite provides instant, scalable API access to the Ethereum and IPFS networks.

### %Getting Started%
1. Clone the Repository

git clone https://github.com/yourusername/ethereum-deposit-tracker.git

cd ethereum-deposit-tracker

2. Set Up the Virtual Environment

It's recommended to create a virtual environment to manage dependencies:

_On Windows:_
```
Copy code
python -m venv venv
.\venv\Scripts\activate
```

_On macOS/Linux:_
```
Copy code
python -m venv venv
source venv/bin/activate
```

3. Install Dependencies

Copy code
```
pip install -r requirements.txt
```
5. Configure Environment Variables

Create a .env file in the root directory and add the following variables:

```
INFURA_URL=https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID
MONGO_URI=mongodb://YOUR_MONGO_URI
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

Make sure to replace the placeholders with your actual Infura project ID, MongoDB URI, and Telegram bot token.

### Prometheus Setup

Install Prometheus: Follow the Prometheus installation guide.

Configure Prometheus: 

Create a prometheus.yml 

Configuration file with the following content:

yaml

_Copy code_

```
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ethereum_deposit_tracker'
    static_configs:
      - targets: ['localhost:9090']

Start Prometheus:

prometheus --config.file=prometheus.yml
```
Grafana Setup

Install Grafana: Follow the Grafana installation guide.

Configure Data Source:

Go to Configuration > Data Sources in Grafana.

Select Prometheus as the data source.

Set the URL to http://localhost:9090 and click Save & Test.

Create Dashboards:

Navigate to Create > Dashboard in Grafana.

Add a new panel and select Prometheus as the data source.

Use Prometheus queries to visualize metrics like deposit counts and transaction statistics.

Running the Application

After configuring the environment and setting up Prometheus and Grafana, you can run the Ethereum Deposit Tracker using:
 ```
python tracker.py
 ```
This will start the monitoring service, fetching Ethereum deposit events, sending Telegram notifications, logging data in MongoDB, and exposing metrics on port 9090.

Monitoring and Alerts

Prometheus: Access Prometheus at http://localhost:9090 to view and query metrics.

Grafana: Access Grafana at http://localhost:3000 to view your real-time deposit dashboards.

Telegram Alerts: When a new deposit event is detected, you'll receive a message in your Telegram chat with detailed information about the transaction.

Logging
All logs are stored in the tracker.log file. The logs will contain important information such as:

```
Deposit Events: Logs the details of detected deposit events.
Telegram Notifications: Logs the status of Telegram messages sent.
Errors: Logs any errors encountered during execution.
```

1. Terminal Output
Here is an example of the terminal output when the tracker starts running and monitors deposits.


2. Telegram Notifications
You will receive notifications in Telegram similar to the following message when a new deposit event occurs:
![Telegram Logo](https://github.com/whynpd/Luganodes---SDE-Assignment-21BCE2703/blob/main/Telegram.png)

3. Grafana Dashboard
Visualize the deposit activity in real-time on your Grafana dashboard:


4. Prometheus Metrics
Prometheus collects metrics that are visualized in Grafana. You can view raw data directly in Prometheus as well:

## _FILES INVOLVED IN THIS PROJECT_
### tracker.py

This Python script tracks Ethereum deposits from a specific contract, stores data in MongoDB, and exposes metrics to Prometheus. It also sends notifications to Telegram.

_Key Components_
Logging Configuration:

Purpose: To log debug information and errors.
Details: Logs are written to tracker.log and also output to the console. The logging level is set to DEBUG for detailed information.
python
Copy code
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tracker.log'),
        logging.StreamHandler()
    ]
)
Prometheus Metrics:

Purpose: To count the number of deposit events.
Details: Uses Prometheus Counter to track the number of deposits. The metric is exposed on port 8000.
python
Copy code
deposit_counter = Counter('deposits', 'Number of deposits detected')
Ethereum Connection:

Purpose: To connect to the Ethereum network.
Details: Uses the Infura URL from environment variables to create a Web3 instance.
python
Copy code
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
MongoDB Connection:

Purpose: To store deposit data.
Details: Connects to MongoDB using the URI from environment variables and selects the appropriate database and collection.
python
Copy code
client = MongoClient(mongo_uri)
db = client['your_database_name']
collection = db['your_collection_name']
Telegram Notifications:

Purpose: To notify users of new deposits.
Details: Sends messages to Telegram using a bot token. Chat IDs are read from chat_ids.txt.
python
Copy code
BOT_TOKEN = 'your_bot_token'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
Fetching Deposit Logs:

Purpose: To retrieve deposit logs from Ethereum.
Details: Fetches logs from a range of blocks and filters them based on the contract address.
python
Copy code
deposit_filter = web3.eth.filter({
    "address": contract_address,
    "fromBlock": start_block,
    "toBlock": latest_block
})
Processing Logs:

Purpose: To process each log entry and update metrics.
Details: Retrieves transaction receipts, block details, and updates the Prometheus counter. Stores relevant deposit information in MongoDB.
python
Copy code
deposit_counter.inc()  # Increment deposit count
Starting the Prometheus HTTP Server:

Purpose: To expose metrics to Prometheus.
Details: Starts an HTTP server on port 8000 to serve the Prometheus metrics.
python
Copy code
start_http_server(8000)
Main Loop:

Purpose: To continuously fetch and process logs.
Details: The script runs an infinite loop that periodically fetches logs and processes them.
python
Copy code
while True:
    logs = fetch_deposit_logs()
    process_logs(logs)



Contribution
Contributions are welcome! If you have any ideas or improvements, feel free to open an issue or submit a pull request. Please follow the standard GitHub Flow for contributions.

License
This project is licensed under the MIT License - see the LICENSE file for details.

FAQ
1. How does this project monitor Ethereum deposits?
The Ethereum Deposit Tracker listens for DepositEvent from the Ethereum Beacon Chain deposit contract. These events are fetched, processed, and then logged in MongoDB. Notifications are sent to Telegram for new deposits, and data is visualized in Grafana.

2. What technologies are used in this project?
Web3.py for interacting with the Ethereum blockchain.
MongoDB for storing transaction data.
Prometheus for collecting and exposing metrics.
Grafana for real-time visualization.
Telegram API for sending notifications.
3. How can I add more Telegram chat IDs?
Use the telegram.py script to update chat IDs by polling Telegram’s getUpdates API and storing new chat IDs in a chat_ids.txt file.

Additional Resources
Ethereum Beacon Chain Deposit Contract
Web3.py Documentation
Prometheus Documentation
Grafana Documentation
