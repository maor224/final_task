<h2>Simple HTTP Server</h2>

This is a simple HTTP server implemented in Python that provides basic functionality for managing user accounts and transactions. The server uses the MongoDB database to store user and transaction data.</p>

<h3>Setup</h3>

<ol>
    <li>Install Python 3.6 .</li>
    <li>Install the required dependencies by running the following command:<br>pip install pymongo</li>
    <li>Make sure you have MongoDB installed and running.</li>
</ol>

<h3>Usage</h3>
<p>
    To start the server, run the following command:
    <br>
    python app_driver.py (MongoDB password)
    <br>
    Replace (MongoDB password) with your MongoDB Atlas password.
    The server will start listening on the specified host and port (default: localhost:8080).
</p>

<h3>Endpoints</h3>
<ul>
    <li>/ (Home Page): Displays the home page with login form.</li>
    <li>/details?id=(user_id): Displays the details of a user identified by the (user_id).</li>
    <li>/deposit?id=(user_id): Allows users to deposit money into their account.</li>
    <li>/withdraw?id=(user_id): Allows users to withdraw money from their account.</li>
    <li>/transactions?id=(user_id): Displays the transaction history for a user identified by the (user_id).</li>
</ul>

<h3>Templates</h3>
<p>The server uses HTML templates to render the web pages. The templates are located in the templates directory.</p>
<ul>
    <li>home.html: The home page template.</li>
    <li>details.html: The user details page template.</li>
    <li>deposit.html: The deposit page template.</li>
    <li>withdraw.html: The withdraw page template.</li>
    <li>transactions.html: The transactions page template.</li>
</ul>
<p>You can modify these templates to customize the appearance of the web pages.</p>

<h3>Database</h3>
<p>The server uses MongoDB to store user and transaction data. The database connection URL is provided as a command-line argument when starting the server.</p>

