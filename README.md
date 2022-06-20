# XxMaxiexX's Bed
## Important
You should start the server first and then run Jetson and Frontend.
## How to run Jetson
```bash
cd jetson
```
Install packages for Jetson Nano
```bash
$ pip3 install -r requirements.txt
```
Setup docker
```bash
# Pull image
$ docker pull eclipse-mosquitto
# Run docker container
$ docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
```
Run main code
```bash
$ bash run.sh
```

## How to run Frontend and Backend
```bash
cd computer
```
Setup
```bash
$ npm install
```
Run Frontend
```bash
$ npm start
```
Run Backend
```bash
$ npm run server
```
