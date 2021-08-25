Scrape local MTG sites to find cards I'm looking for :)

Will eventually have recurring way to search and notify me when they get stock of the things I'm looking for.

Get it running:  

Make env and pip install requirements.txt  
Populate `config.py` in `instance`  
docker-compose up -d  
make init-db  
make init-kafka  
make start-web  
make start-consumer  
 
