## gadget_scraper
Scrapy project for comparemymobile.com website
## Description
## Installation
```bash
git clone https://github.com/danbok/gadget_scraper/
cd gadget_scraper
sudo apt-get install libxml2-dev libssl-dev python-dev libxslt1-dev build-essential libffi-dev
pip install -r requirements.txt
```
After that, try to get Scrapy version typing `scrapy version`
Output should be `"Scrapy 1.0.5".`
This is enough for basic setup. However, if you want to enable mailing, you need to set up SMTP server, for example, Postfix
```bash
sudo apt-get install -y postfix
```
and enable mailing in settings.
Last option is scraping through TOR network. To enable this, you need to install TOR
```bash
sudo apt-get install tor privoxy
```
and enable TOR proxy usage in settings.
## Configuration
## Usage example
## Output example
