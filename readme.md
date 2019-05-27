# server-network-speed

A cron job and flask app to keep track of my remote server's network speeds.

The cron job runs on the server and stores the results of a speed test in a database.

The flask app reads the database and shows me the speeds over time.