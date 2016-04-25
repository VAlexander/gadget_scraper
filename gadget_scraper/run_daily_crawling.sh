cd /home/ubuntu/gadget_scraper/gadget_scraper
python ./run_compare_my_mobile_tablets_spider.py
./change_tor_node.sh
echo "Changed TOR node"
python ./run_compare_my_mobile_phones_spider.py
