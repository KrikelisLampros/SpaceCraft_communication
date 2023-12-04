sudo apt-get update
sudo apt-get install curl
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker $USER
sudo apt-get install python3-pip
sudo pip3 install paho-mqtt
sudo chmod +x environment.sh