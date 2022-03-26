echo "======================= STARTED!!! ======================="
echo "CREATE ENVIRONMENT"
python3 -m venv env

echo "ACTIVE ENVIRONMENT"
source env/bin/activate

echo "UPDATE SETUPTOOLS"
pip install --upgrade pip
pip install --upgrade setuptools

echo "INSTALL LIBRARY"
pip install -r requirements.txt

echo "MOVE FOLDER"
cd items_list_spider/

echo "RUN CRAWL ITEMS IN STORE"
echo "https://www.etopfun.com/en/store/"
scrapy crawl storeItems -O storeItems.csv

echo "======================= FINISHED!!! ======================="