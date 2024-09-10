
import logging
from web3 import Web3
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import requests
from prometheus_client import start_http_server, Counter
import time

# Load environment variables (if using a .env file)
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tracker.log'),
        logging.StreamHandler()
    ]
)

# Create a logger object
logger = logging.getLogger(__name__)

# Replace with your actual values
INFURA_URL = os.getenv('INFURA_URL')  # Alchemy URL from .env
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Check connection
if web3.is_connected():
    logger.info("Connected to Ethereum network")
else:
    logger.error("Failed to connect")

# Beacon Deposit Contract Address
contract_address = '0x00000000219ab540356cBB839Cbe05303d7705Fa'

# MongoDB connection
mongo_uri = os.getenv('MONGO_URI')  # MongoDB connection string from .env
client = MongoClient(mongo_uri)
db = client['your_database_name']  
collection = db['your_collection_name']  

# Telegram notification function
BOT_TOKEN = '7411494795:AAHCTIGi5MpdAGfSF9_mLv_WHTV7t-rQkx0'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
CHAT_IDS_FILE = 'chat_ids.txt'
PROCESSED_TX_FILE = 'processed_tx.txt'

def send_telegram_message(message, chat_ids):
    for chat_id in chat_ids:
        try:
            response = requests.post(TELEGRAM_API_URL, data={'chat_id': chat_id, 'text': message})
            response.raise_for_status()
            logger.info(f"Message sent successfully to chat ID: {chat_id}")
        except Exception as e:
            logger.error(f"Error sending message to chat ID {chat_id}: {e}")

def read_chat_ids():
    try:
        with open(CHAT_IDS_FILE, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

def get_processed_transactions():
    """Read processed transactions from a file."""
    try:
        with open(PROCESSED_TX_FILE, 'r') as file:
            return set(line.strip() for line in file.readlines())
    except FileNotFoundError:
        return set()

def add_processed_transaction(tx_hash):
    """Add a transaction hash to the processed transactions file."""
    with open(PROCESSED_TX_FILE, 'a') as file:
        file.write(f"{tx_hash}\n")

# Function to get transaction receipt
def get_transaction_receipt(tx_hash):
    try:
        receipt = web3.eth.get_transaction_receipt(tx_hash)
        return receipt
    except Exception as e:
        logger.error(f"Error fetching transaction receipt: {e}")
        return None

# Function to get block details
def get_block_details(block_number):
    try:
        block = web3.eth.get_block(block_number)
        return block
    except Exception as e:
        logger.error(f"Error fetching block details: {e}")
        return None

# Function to fetch deposit logs
def fetch_deposit_logs():
    latest_block = web3.eth.block_number
    start_block = latest_block - 100  # Adjust range as needed
    logger.info(f"Fetching logs from block {start_block} to {latest_block}...")
    
    try:
        deposit_filter = web3.eth.filter({
            "address": contract_address,
            "fromBlock": start_block,
            "toBlock": latest_block
        })

        logs = deposit_filter.get_all_entries()
        logger.info(f"Fetched {len(logs)} logs.")
        return logs
    except Exception as e:
        logger.error(f"Error fetching deposit logs: {e}")
        return []

# Define a metric to count deposits
deposit_counter = Counter('deposits', 'Number of deposits detected')

def process_logs(logs):
    if not logs:
        logger.info("No logs found.")
        return

    chat_ids = read_chat_ids()
    processed_tx_hashes = get_processed_transactions()

    for log in logs:
        tx_hash = log['transactionHash'].hex()
        
        # Check if this transaction has already been processed
        if tx_hash in processed_tx_hashes:
            continue

        receipt = get_transaction_receipt(tx_hash)
        
        if receipt:
            block_number = receipt['blockNumber']
            block = get_block_details(block_number)
            
            if block:
                block_timestamp = block['timestamp']
                deposit_counter.inc()  # Increment deposit count
                
                # Notify via Telegram
                if chat_ids:
                    send_telegram_message(f"New deposit detected: {{'transactionHash': '{tx_hash}', 'blockNumber': {block_number}, 'blockTimestamp': {block_timestamp}}}", chat_ids)
                
                # Extract additional information from logs if needed
                for log_entry in receipt['logs']:
                    if log_entry['transactionHash'] == tx_hash:
                        document = {
                            "transactionHash": tx_hash,
                            "blockNumber": block_number,
                            "blockTimestamp": block_timestamp,
                            "logIndex": log_entry['logIndex'],
                            "contractAddress": contract_address,
                            "data": log_entry['data']
                        }
                        result = collection.insert_one(document)
                        logger.info(f"Document inserted with ID: {result.inserted_id}")

                # Mark this transaction as processed
                add_processed_transaction(tx_hash)
            else:
                logger.warning(f"Failed to fetch block details for block number {block_number}")
        else:
            logger.warning(f"Failed to fetch transaction receipt for hash {tx_hash}")

# Fetch and process logs
if __name__ == '__main__':
    start_http_server(9090)  # Expose metrics on port 9090
    while True:
        logs = fetch_deposit_logs()
        process_logs(logs)
        time.sleep(60)  # Sleep for 60 seconds before the next fetch





