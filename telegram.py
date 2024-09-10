'''
import requests
import json
import time
import os
from web3 import Web3

BOT_TOKEN = '7411494795:AAHCTIGi5MpdAGfSF9_mLv_WHTV7t-rQkx0'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
CHAT_IDS_FILE = 'chat_ids.txt'


INFURA_PROJECT_ID = f'5f9a3597d4b7435fb3ee128658db212e'
ETHEREUM_NODE_URL = f'https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}'
web3 = Web3(Web3.HTTPProvider(ETHEREUM_NODE_URL))

# Using the ETH2.0 Deposit Contract address (convert to checksum)
CONTRACT_ADDRESS = web3.to_checksum_address('0x00000000219ab540356cbb839cbe05303d7705fa')

# The ABI provided
CONTRACT_ABI = [
    {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "bytes", "name": "pubkey", "type": "bytes"},
            {"indexed": False, "internalType": "bytes", "name": "withdrawal_credentials", "type": "bytes"},
            {"indexed": False, "internalType": "bytes", "name": "amount", "type": "bytes"},
            {"indexed": False, "internalType": "bytes", "name": "signature", "type": "bytes"},
            {"indexed": False, "internalType": "bytes", "name": "index", "type": "bytes"},
        ],
        "name": "DepositEvent",
        "type": "event",
    },
    {
        "inputs": [
            {"internalType": "bytes", "name": "pubkey", "type": "bytes"},
            {"internalType": "bytes", "name": "withdrawal_credentials", "type": "bytes"},
            {"internalType": "bytes", "name": "signature", "type": "bytes"},
            {"internalType": "bytes32", "name": "deposit_data_root", "type": "bytes32"},
        ],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "get_deposit_count",
        "outputs": [{"internalType": "bytes", "name": "", "type": "bytes"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "get_deposit_root",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}],
        "name": "supportsInterface",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "pure",
        "type": "function",
    },
]

# Initialize the contract
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def send_telegram_message(message, chat_ids):
    """Sends a message to all chat IDs."""
    for chat_id in chat_ids:
        try:
            response = requests.post(TELEGRAM_API_URL, data={'chat_id': chat_id, 'text': message})
            response.raise_for_status()
            print(f"Message sent successfully to chat ID: {chat_id}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending message to chat ID {chat_id}: {e}")

def update_chat_ids():
    """Updates chat IDs from the bot's updates and saves them to a file."""
    try:
        response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates')
        response.raise_for_status()
        data = response.json()

        if not os.path.exists(CHAT_IDS_FILE):
            open(CHAT_IDS_FILE, 'w').close()

        existing_chat_ids = read_chat_ids()
        new_chat_ids = [update['message']['chat']['id'] for update in data.get('result', []) if 'message' in update]

        with open(CHAT_IDS_FILE, 'a') as file:
            for chat_id in new_chat_ids:
                if chat_id not in existing_chat_ids:
                    file.write(f"{chat_id}\n")
                    print(f"New chat ID {chat_id} added.")
                else:
                    print(f"Chat ID {chat_id} already exists.")

        return new_chat_ids
    except requests.exceptions.RequestException as e:
        print(f"Error fetching updates from Telegram API: {e}")
        return []

def read_chat_ids():
    """Reads chat IDs from the file."""
    try:
        with open(CHAT_IDS_FILE, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"File {CHAT_IDS_FILE} not found.")
        return []

def handle_new_deposit(event):
    """Handles new deposit events and sends a message."""
    transaction_hash = event['transactionHash'].hex()
    block_number = event['blockNumber']
    block_timestamp = web3.eth.get_block(block_number)['timestamp']

    message = (
        f"New deposit detected:\n"
        f"Transaction Hash: {transaction_hash}\n"
        f"Block Number: {block_number}\n"
        f"Block Timestamp: {block_timestamp}"
    )
    print(message)

    # Send message to all registered chat IDs
    chat_ids = read_chat_ids()
    send_telegram_message(message, chat_ids)

def monitor_deposits():
    """Monitors the contract for new deposit events."""
    try:
        event_filter = contract.events.DepositEvent.create_filter(from_block='latest')
        print("Monitoring deposits...")
        while True:
            print("Checking for new events...")
            try:
                new_entries = event_filter.get_new_entries()
                if not new_entries:
                    print("No new entries found.")
                for event in new_entries:
                    handle_new_deposit(event)
            except Exception as e:
                print(f"Error getting new entries: {e}")
            time.sleep(10)  # Sleep for a short period to avoid overloading the node
    except Exception as e:
        print(f"An error occurred: {e}")




if __name__ == "__main__":
    # Update chat IDs (optional, run this separately if needed)
    update_chat_ids()

    # Monitor Ethereum blockchain for new deposits
    monitor_deposits()
'''
import requests
import json
import os
import time
from web3 import Web3

# Replace with your actual bot token
BOT_TOKEN = f'7411494795:AAHCTIGi5MpdAGfSF9_mLv_WHTV7t-rQkx0'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
CHAT_IDS_FILE = 'chat_ids.txt'

# Replace with your actual Infura project ID
INFURA_PROJECT_ID = f'5f9a3597d4b7435fb3ee128658db212e'
ETHEREUM_NODE_URL = f'https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}'
web3 = Web3(Web3.HTTPProvider(ETHEREUM_NODE_URL))

# Using the ETH2.0 Deposit Contract address (convert to checksum)
CONTRACT_ADDRESS = web3.to_checksum_address('0x00000000219ab540356cbb839cbe05303d7705fa')

# The ABI you provided
CONTRACT_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "bytes", "name": "pubkey", "type": "bytes"},
            {"indexed": False, "internalType": "bytes", "name": "withdrawal_credentials", "type": "bytes"},
            {"indexed": False, "internalType": "bytes", "name": "amount", "type": "bytes"},
            {"indexed": False, "internalType": "bytes", "name": "signature", "type": "bytes"},
            {"indexed": False, "internalType": "bytes", "name": "index", "type": "bytes"},
        ],
        "name": "DepositEvent",
        "type": "event",
    },
]

# Initialize the contract
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def send_telegram_message(message, chat_ids):
    """Sends a message to all chat IDs."""
    for chat_id in chat_ids:
        try:
            response = requests.post(TELEGRAM_API_URL, data={'chat_id': chat_id, 'text': message})
            response.raise_for_status()
            print(f"Message sent successfully to chat ID: {chat_id}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending message to chat ID {chat_id}: {e}")

def update_chat_ids():
    """Updates chat IDs from the bot's updates and saves them to a file."""
    try:
        response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates')
        response.raise_for_status()
        data = response.json()

        if not os.path.exists(CHAT_IDS_FILE):
            open(CHAT_IDS_FILE, 'w').close()

        existing_chat_ids = read_chat_ids()
        new_chat_ids = [update['message']['chat']['id'] for update in data.get('result', []) if 'message' in update]

        with open(CHAT_IDS_FILE, 'a') as file:
            for chat_id in new_chat_ids:
                if chat_id not in existing_chat_ids:
                    file.write(f"{chat_id}\n")
                    print(f"New chat ID {chat_id} added.")
                else:
                    print(f"Chat ID {chat_id} already exists.")

        return new_chat_ids
    except requests.exceptions.RequestException as e:
        print(f"Error fetching updates from Telegram API: {e}")
        return []

def read_chat_ids():
    """Reads chat IDs from the file."""
    try:
        with open(CHAT_IDS_FILE, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"File {CHAT_IDS_FILE} not found.")
        return []

def handle_new_deposit(event):
    """Handles new deposit events and sends a message."""
    transaction_hash = event['transactionHash'].hex()
    block_number = event['blockNumber']
    block_timestamp = web3.eth.get_block(block_number)['timestamp']

    message = (
        f"New deposit detected:\n"
        f"Transaction Hash: {transaction_hash}\n"
        f"Block Number: {block_number}\n"
        f"Block Timestamp: {block_timestamp}"
    )
    print(message)

    # Send message to all registered chat IDs
    chat_ids = read_chat_ids()
    send_telegram_message(message, chat_ids)

def monitor_deposits(max_tries=20):
    """Monitors the contract for new deposit events and stops after a specified number of tries."""
    event_filter = contract.events.DepositEvent.create_filter(from_block='latest')
    print("Monitoring deposits...")

    tries = 0
    while tries < max_tries:
        print("Checking for new events...")
        try:
            new_entries = event_filter.get_new_entries()
            if new_entries:
                for event in new_entries:
                    handle_new_deposit(event)
            else:
                print("No new entries found.")
        except Exception as e:
            print(f"Error getting new entries: {e}")
        
        time.sleep(10)  # Sleep for a short period to avoid overloading the node
        tries += 1

    print("Stopped monitoring after 20 tries.")


if __name__ == "__main__":
    # Update chat IDs (optional, run this separately if needed)
    update_chat_ids()

    # Monitor Ethereum blockchain for new deposits
    monitor_deposits()

