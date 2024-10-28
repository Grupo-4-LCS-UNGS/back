sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.13 python3.13-dev build-essential libpq-dev
python3.13 -m venv virtual
source virtual/Scripts/activate
pip install psycopg2-binary
pip install -r requirements.txt