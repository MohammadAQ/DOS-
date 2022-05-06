# DOS-PROJECT
# Bazar - online book store
Bazar is an Online book store that works with microservices.
## Introduction 
The store will employ a two-tier web design - a front-end and a back- end - and use microservices at each tier. The front-end tier will accept user requests and perform initial processing. The backend consists of two components: a catalog server and an order server.

Where this store works with Microservices - also known as the microservice architecture - is an architectural style that structures an application as a collection of services that are
1. Highly maintainable and testable.
2. Loosely coupled.
3. Independently deployable.
4. Organized around business capabilities.
5. Owned by a small team.
    
    
---
# How to run this project: 
### First: setup your environment.
in this project, we need to setup five machines, where each one works with others. where its recommended to be at the same network, or make a virtual environments. using **VMware** or **VirtualBox** for example. 


### Second : Installation.
First, make sure that you have **Python** installed on your device(s).

Next, make sure that you have **pip** if you don't have it on your device from [here](https://pip.pypa.io/en/stable/installing/).

On each virtual environment that works as a microservice is in its own folder. --> on CLI:  
```
git clone https://github.com/MohammadAQ/DOS-
```

For each machine, install the required Python packages using pip:
```
pip3 install -r requirements.txt
```
---

# Networking 
In this project, we will use the same **NIC** on all machines. **BRIDGE** for example. 
## First you need to edit the `flask_app` file on each machine by adding the other machines addresses. as shown in the table below.

Environment Variable | Description | 
-------------------- | ----------- | 
`CATALOG_ADDRESS` | The address of the catalog service. Used in the order and front-end services. 
`ORDER_ADDRESS` | The address of the order service. Used in the front-end and catalog services. 
`FRONT_END_ADDRESS` | The address of the front-end service. Used in the catalog and order services.
`FLASK_ENV` | Define the enviroment of the Flask application. Can be `development` or `production`. `development` enables the use of debug mode.
`FLASK_DEBUG` | Enable debug mode or not. In debug mode, modifications to the Flask application files automatically refreshes the service. Requires `FLASK_ENV` to be set to `development`. Can be `True` or `False`. 
`FLASK_PORT` | Define the port number used by the microservice. 

## Next, after setting up all the above simply you can run this project by executing this command on each machine.
```
python3 ./app.py
```
**Note** if not work, you need to but the path to the `app.py` file. it should work. 

