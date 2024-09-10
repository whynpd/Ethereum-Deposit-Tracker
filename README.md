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

### %Getting Started%
1. Clone the Repository
bash
Copy code
git clone https://github.com/yourusername/ethereum-deposit-tracker.git
cd ethereum-deposit-tracker
2. Set Up the Virtual Environment
It's recommended to create a virtual environment to manage dependencies:

_On Windows:_
```
bash
Copy code
python -m venv venv
.\venv\Scripts\activate
```

_On macOS/Linux:_
```
bash
Copy code
python -m venv venv
source venv/bin/activate
```

3. Install Dependencies
bash
Copy code
```
pip install -r requirements.txt
```
5. Configure Environment Variables

Create a .env file in the root directory and add the following variables:

plaintext
Copy code
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

configuration file with the following content:

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
bash
Copy code
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

bash
Copy code
python tracker.py
This will start the monitoring service, fetching Ethereum deposit events, sending Telegram notifications, logging data in MongoDB, and exposing metrics on port 9090.

Monitoring and Alerts
Prometheus: Access Prometheus at http://localhost:9090 to view and query metrics.
Grafana: Access Grafana at http://localhost:3000 to view your real-time deposit dashboards.
Telegram Alerts: When a new deposit event is detected, you'll receive a message in your Telegram chat with detailed information about the transaction.
Logging
All logs are stored in the tracker.log file. The logs will contain important information such as:

Deposit Events: Logs the details of detected deposit events.
Telegram Notifications: Logs the status of Telegram messages sent.
Errors: Logs any errors encountered during execution.
Screenshots and Outputs
1. Terminal Output
Here is an example of the terminal output when the tracker starts running and monitors deposits.


2. Telegram Notifications
You will receive notifications in Telegram similar to the following message when a new deposit event occurs:


3. Grafana Dashboard
Visualize the deposit activity in real-time on your Grafana dashboard:


4. Prometheus Metrics
Prometheus collects metrics that are visualized in Grafana. You can view raw data directly in Prometheus as well:


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
