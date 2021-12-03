Scrape local MTG sites to find cards I'm looking for :)

Will eventually have recurring way to search and notify me when they get stock of the things I'm looking for.

## Get it running:

Populate `config.py` in `instance`

Build all images in their respective folders:
 - `docker build . -t web:latest`
 - `docker build . -t scrapyd:latest`
 - `docker build . -t scrapydweb:latest`
 - `docker build . -t consumer:latest`
 - `docker build . -t log-parser:latest`

### Start containers
docker-compose up -d
