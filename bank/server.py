import html
import socket
import logging
import threading

from db_handler import DBHandler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class HTTPServer:
    def __init__(self, host, port):
        """
        Initialize the HTTPServer object.

        Args:
            host (str): The host IP address.
            port (int): The port number to listen on.
        """
        self.host = host
        self.port = port
        self.db = DBHandler()
        self.locks = {}

    def serve_user_details(self, user_id):
        """
        Serve the details page for a user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            bytes: The HTML content of the details page.
        """
        user = self.db.get_user_by_id(user_id)
        with open('templates/details.html', 'rb') as file:
            name = html.escape(user["first_name"] + " " + user["last_name"])
            balance = html.escape(str(user["balance"]))
            file_code = file.read().replace(b'name', name.encode())
            return file_code.replace(b'amount', balance.encode())

    @staticmethod
    def serve_home_page():
        """
        Serve the home page.

        Returns:
            bytes: The HTML content of the home page.
        """
        with open('templates/home.html', 'rb') as file:
            return file.read()

    @staticmethod
    def serve_deposit_page():
        """
        Serve the deposit page.

        Returns:
            bytes: The HTML content of the deposit page.
        """
        with open('templates/deposit.html', 'rb') as file:
            return file.read()

    @staticmethod
    def serve_withdraw_page():
        """
        Serve the withdraw page.

        Returns:
            bytes: The HTML content of the withdraw page.
        """
        with open('templates/withdraw.html', 'rb') as file:
            return file.read()

    def serve_transactions_page(self, user_id):
        """
        Serve the transactions page for a user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            bytes: The HTML content of the transactions page.
        """
        user = self.db.get_user_by_id(user_id)
        transactions = self.db.get_transactions_by_user_id(user_id)

        with open('templates/transactions.html', 'rb') as file:
            file_code = file.read().decode()
            file_code = file_code.replace('name', user['first_name'] + ' ' + user['last_name'])

            transaction_list = ''
            for transaction in transactions:
                if transaction['transaction_type'] == 0:
                    transaction_html = f"<li>deposit: {transaction['amount']}<br>Time: {transaction['timestamp']}</li>"
                    transaction_list += transaction_html
                if transaction['transaction_type'] == 1:
                    transaction_html = f"<li>withdraw: {transaction['amount']}<br>Time: {transaction['timestamp']}</li>"
                    transaction_list += transaction_html

            file_code = file_code.replace('transactions', transaction_list)

            return file_code.encode()

    def handle_login_request(self, code):
        """
        Handle a login request.

        Args:
            code (str): The login code.

        Returns:
            str: The redirect path after login.
        """
        code = html.escape(code)
        if code != '' and len(code) == 4:
            if self.db.login(code):
                user = self.db.get_user_by_code(code)
                _id = str(user["_id"])
                return f"/details?id={_id}"
        return "/"

    def handle_transaction_request(self, user_id, amount, transaction_type):
        """
        Handle a transaction request.

        Args:
            user_id (str): The ID of the user.
            amount (str): The amount of the transaction.
            transaction_type (int): The type of the transaction (0 for deposit, 1 for withdraw).

        Returns:
            str: The redirect path after the transaction.
        """
        amount = html.escape(amount)
        if amount.isdigit() and int(amount) > 0:
            user = self.db.get_user_by_id(user_id)

            # Acquire the lock for the user
            lock = self.get_user_lock(user_id)
            lock.acquire()

            try:
                if self.db.update_user_balance(user['code'], int(amount), transaction_type) and \
                        self.db.insert_transaction(user_id, int(amount), transaction_type):
                    return f"/details?id={user_id}"
            finally:
                # Release the lock after the transaction is completed
                lock.release()

        return f"/{'deposit' if transaction_type == 0 else 'withdraw'}?id={user_id}"

    def get_user_lock(self, user_id):
        """
        Get or create a lock for the specified user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            threading.Lock: The lock object for the user.
        """
        if user_id not in self.locks:
            self.locks[user_id] = threading.Lock()
        return self.locks[user_id]

    def handle_request(self, client_socket):
        """
        Handle a client request.

        Args:
            client_socket (socket.socket): The client socket.

        Returns:
            None
        """
        request = client_socket.recv(1024).decode('utf-8')

        # Extract the requested path from the HTTP request
        path = request.split(' ')[1]

        try:
            if path == '/':
                response_body = self.serve_home_page()
            elif path.startswith('/user'):
                if request.startswith('POST'):
                    code = request.split('\r\n')[-1].split('=')[1]
                    redirect_path = self.handle_login_request(code)
                    response_header = f"HTTP/1.1 302 Found\r\nLocation: {redirect_path}\r\n\r\n"
                    client_socket.sendall(response_header.encode('utf-8'))
                    client_socket.close()
                    logging.info(f"Redirecting to: {redirect_path}")
                    return
                else:
                    response_body = b"Not Found"
            elif path.startswith('/details'):
                user_id = path.split('=')[1]
                response_body = self.serve_user_details(user_id)
            elif path.startswith('/deposit'):
                if request.startswith('POST'):
                    user_id = request.split('\r\n')[0].split('=')[1].split(" ")[0]
                    amount = request.split('\r\n')[-1].split('=')[1]
                    redirect_path = self.handle_transaction_request(user_id, amount, 0)
                    response_header = f"HTTP/1.1 302 Found\r\nLocation: {redirect_path}\r\n\r\n"
                    client_socket.sendall(response_header.encode('utf-8'))
                    client_socket.close()
                    logging.info(f"Redirecting to: {redirect_path}")
                    return
                else:
                    response_body = self.serve_deposit_page()
            elif path.startswith('/withdraw'):
                if request.startswith('POST'):
                    user_id = request.split('\r\n')[0].split('=')[1].split(" ")[0]
                    amount = request.split('\r\n')[-1].split('=')[1]
                    redirect_path = self.handle_transaction_request(user_id, amount, 1)
                    response_header = f"HTTP/1.1 302 Found\r\nLocation: {redirect_path}\r\n\r\n"
                    client_socket.sendall(response_header.encode('utf-8'))
                    client_socket.close()
                    logging.info(f"Redirecting to: {redirect_path}")
                    return
                else:
                    response_body = self.serve_withdraw_page()
            elif path.startswith('/transactions'):
                user_id = path.split('=')[1]
                response_body = self.serve_transactions_page(user_id)
            else:
                response_body = b"Not Found"

            # Generate the response header
            response_header = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_body)}\r\n\r\n"

            # Send the response
            client_socket.sendall(response_header.encode('utf-8') + response_body)

        except Exception as e:
            # Handle any exception gracefully
            logging.error(f"An error occurred: {str(e)}")
            response_body = b"Internal Server Error"

            # Generate the response header
            response_header = f"HTTP/1.1 500 Internal Server Error\r\nContent-Length: {len(response_body)}\r\n\r\n"

            # Send the response
            client_socket.sendall(response_header.encode('utf-8') + response_body)

        finally:
            # Close the connection
            client_socket.close()

    def run_server(self):
        """
        Run the HTTP server.

        Returns:
            None
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen()

            logging.info(f"Server listening on http://{self.host}:{self.port}")

            while True:
                client_socket, address = server_socket.accept()
                logging.info(f"Client connected from {address[0]}:{address[1]}")

                try:
                    # Handle the client request in a separate thread or process if needed
                    self.handle_request(client_socket)
                except Exception as e:
                    # Handle any exception gracefully
                    logging.error(f"An error occurred: {str(e)}")
                    client_socket.close()
