import logging
import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize request counterequest_counter = 0

def log_request(ip_address, user_agent, endpoint):
    global request_counter
    request_counter += 1
    logging.info(f'API Request {request_counter}: {datetime.datetime.utcnow().isoformat()} - IP: {ip_address}, Endpoint: {endpoint}, User-Agent: {user_agent}')

# Example usage
# log_request('192.168.1.1', 'Mozilla/5.0', '/api/endpoint')
