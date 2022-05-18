#sudo docker network create --gateway 10.0.2.1 --subnet 10.0.2.0/24 -d bridge "bazar_network_home"


sudo docker build -t catalog_image:latest ./catalog-server
sudo docker build -t catalog_image_rep:latest ./catalog-server-rep
sudo docker build -t order_image:latest ./order-server
sudo docker build -t order_image_rep:latest ./oreder-server-rep
sudo docker build -t front_image:latest ./front-server



sudo docker run -dit --network "bazar_network_home" --ip 10.0.2.10 -p 5000:5000 --name front_server front_image:latest
sudo docker run -dit --network "bazar_network_home" --ip 10.0.2.8 -p 5004:5000 --name catalog_server_rep catalog_image_rep:latest
sudo docker run -dit --network "bazar_network_home" --ip 10.0.2.7 -p 5003:5000 --name catalog_server catalog_image:latest
sudo docker run -dit --network "bazar_network_home" --ip 10.0.2.15 -p 5002:5000 --name order_server_rep order_image_rep:latest
sudo docker run -dit --network "bazar_network_home" --ip 10.0.2.11 -p 5001:5000 --name order_server order_image:latest


