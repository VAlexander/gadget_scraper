cd /home/ubuntu/gadget_scraper/gadget_scraper
python ./run_musicmagpie_consoles_spider.py
python ./run_musicmagpie_ipods_spider.py
./change_tor_node.sh
echo "Changed TOR node"
python ./run_compare_my_mobile_consoles_spider.py
./change_tor_node.sh
echo "Changed TOR node"
python ./run_compare_my_mobile_handheld_consoles_spider.py
./change_tor_node.sh
echo "Changed TOR node"
python ./run_compare_my_mobile_ipods_spider.py
./change_tor_node.sh
echo "Changed TOR node"
python ./run_compare_my_mobile_smartwatches_spider.py