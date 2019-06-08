# home-network-speed

[![my badge](https://action-badges.now.sh/nolanbconaway/home-network-speed)](https://github.com/nolanbconaway/home-network-speed/actions)


This is a python application which keeps track of my home network performance. There is a cron job running on a raspberry pi throughout the day, which stores the results of a speed test in a database. There is also a flask app reads the database and shows me the speeds over time.