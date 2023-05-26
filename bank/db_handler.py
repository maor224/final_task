import pprint
import secrets
import string
import sys
from datetime import datetime
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from pymongo.mongo_client import MongoClient


class DBHandler:
    """
    Class for handling database operations related to users and transactions.
    """

    def __init__(self):
        """
        Initializes the DBHandler class by establishing a connection to the MongoDB database.
        """
        self.__db_connection = MongoClient(f"mongodb+srv://maor:{sys.argv[1]}@cluster.ddgbm9z.mongodb.net"
                                           "/?retryWrites=true&w=majority")
        self.__db = self.__db_connection['users']

    def getUsersCollection(self):
        """
        Retrieves the 'users' collection from the database.

        Returns:
            pymongo.collection.Collection: The 'users' collection object.
        """
        return self.__db['users']

    def getTransactionsCollection(self):
        """
        Retrieves the 'transactions' collection from the database.

        Returns:
            pymongo.collection.Collection: The 'transactions' collection object.
        """
        return self.__db['transactions']

    def _check_code_exist(self, code):
        """
        Checks if a user with the given code exists in the 'users' collection.

        Args:
            code (str): The user code to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        collection = self.getUsersCollection()
        flag = False
        for item in list(collection.find()):
            if item['code'] == code:
                flag = True

        return flag

    @staticmethod
    def _generate_code():
        """
        Generates a random 4-digit code.

        Returns:
            str: The generated code.
        """
        digits = string.digits
        code = ''.join(secrets.choice(digits) for _ in range(4))
        return code

    def insert_user(self, first_name, last_name):
        """
        Inserts a new user document into the 'users' collection.

        Args:
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
        """
        collection = self.getUsersCollection()
        code = self._generate_code()
        while self._check_code_exist(code):
            code = self._generate_code()

        user_document = {
            'code': code,
            'first_name': first_name,
            'last_name': last_name,
            'balance': 0
        }

        collection.insert_one(user_document)

    def find_all_users(self):
        """
        Prints all the user documents in the 'users' collection.
        """
        printer = pprint.PrettyPrinter()
        users = self.getUsersCollection().find()

        for user in users:
            printer.pprint(user)

    def login(self, code):
        """
        Checks if a user with the given code exists in the 'users' collection.

        Args:
            code (str): The user code to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        return self._check_code_exist(code)

    def get_user_by_code(self, code):
        """
        Retrieves a user document by the provided code from the 'users' collection.

        Args:
            code (str): The user code to retrieve.

        Returns:
            dict: The user document if found, None otherwise.
        """
        users = self.getUsersCollection()
        user = users.find_one({'code': code})
        return user

    def get_user_by_id(self, person_id):
        """
        Retrieves a user document by the provided ID from the 'users' collection.

        Args:
            person_id (str): The ID of the user.

        Returns:
            dict: The user document if found, None otherwise.
        """
        users = self.getUsersCollection()
        _id = ObjectId(person_id)
        user = users.find_one({"_id": _id})
        return user

    def update_user_balance(self, code, new_balance, actionType):
        """
        Updates the balance of a user in the 'users' collection.

        Args:
            code (str): The code of the user.
            new_balance (int): The new balance value.
            actionType (int): The type of action (0: deposit, 1: withdrawal).

        Returns:
            bool: True if the balance was updated successfully, False otherwise.
        """
        users = self.getUsersCollection()

        # Create a filter for the user code
        query_filter = {'code': code}

        # Create an update operation based on the action type
        if actionType == 0:
            update_operation = {'$inc': {'balance': new_balance}}
        elif actionType == 1:
            update_operation = {'$inc': {'balance': -new_balance}}
        else:
            return False

        try:
            # Try to perform the update operation with an optimistic concurrency control mechanism
            updated_user = users.find_one_and_update(query_filter, update_operation,
                                                     return_document=ReturnDocument.AFTER)

            # Check if the update was successful
            if updated_user:
                return True
            else:
                return False
        except DuplicateKeyError:
            # Handle the case where another transaction updated the document before this operation
            return False

    def insert_transaction(self, user_id, amount, transaction_type):
        """
        Inserts a new transaction document into the 'transactions' collection.

        Args:
            user_id (str): The ID of the user associated with the transaction.
            amount (int): The amount of the transaction.
            transaction_type (int): The type of the transaction (0: deposit, 1: withdrawal).

        Returns:
            bool: True if the transaction was inserted successfully, False otherwise.
        """
        transactions = self.getTransactionsCollection()

        # Retrieve the user associated with the transaction
        user = self.get_user_by_id(user_id)

        if transaction_type != 0 and transaction_type != 1:
            return False

        # Create a transaction document with the provided information
        transaction_document = {
            'user_id': ObjectId(user_id),
            'amount': amount,
            'transaction_type': transaction_type,
            'timestamp': datetime.now(),
            'balance': user['balance']
        }

        # Insert the transaction document into the collection
        transactions.insert_one(transaction_document)
        return True

    def get_transactions_by_user_id(self, user_id):
        """
        Retrieves all the transactions associated with a user from the 'transactions' collection.

        Args:
            user_id (str): The ID of the user.

        Returns:
            list: A list of transaction documents if any, an empty list otherwise.
        """
        transactions = self.getTransactionsCollection()
        user_transactions = transactions.find({'user_id': ObjectId(user_id)})
        return list(user_transactions)
