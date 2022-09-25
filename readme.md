# home-network-speed

[![Main Workflow](https://github.com/nolanbconaway/home-network-speed/actions/workflows/push.yml/badge.svg)](https://github.com/nolanbconaway/home-network-speed/actions/workflows/push.yml)

This is a python application which keeps track of my home network performance. There is a cron job running on a raspberry pi throughout the day, which stores the results of a speed test in a database. There is also a flask app reads the database and shows me the speeds over time.