sudo docker build -t ru-bubot-telegram .
sudo docker image rm ru-bubot-telegram

sudo docker run --detach --name ru-bubot-telegram -it -p 8081:8080 --rm ru-bubot-telegram
 
sudo docker run --name ru-bubot-telegram --rm \
  --publish 8081:8080 \
  --volume /home/businka/project/ru-bubot-telegram/conf/device:/var/ru-bubot-telegram/conf/device \
  ru-bubot-telegram 

sudo docker logs ru-bubot-telegram