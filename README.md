# XapiProject
<p>
XapiProject is web application that gets data from Watershed LRS in form of xAPI and from Moodle.
XapiProject visualizes and analyzes this data.
</p>


## Instalation
1. Install Docker
2. Download this repository 
3. Download docker-compose for Moodle on your computer on https://github.com/mvlcak/Moodle
4. Follow installation of the Moodle repository from README.md
5. Create your account in Watershed LRS
6. In watershed go to Data > xAPI Data and create activity provider
7. In project\app\cron.py change endpoint in url 
```
https://watershedlrs.com/api/organizations/<yourLrsEndpoint>/query/export?type=json
```
to  your endpoint from Watershed LRS
8. In project\app\views.py change variable host to the host that you have run your Moodle and token to the token generated in Moodle
9. Run<br>
```
docker compose up
```
10. Run command
```
docker container ps
```
11. Copy container ID of application
12. Run command
```
docker exec -it <your app ID> bash
```
13. And then run commands

```
apt-get update
apt-get install cron
```
14. Change directory to be in same folder as manage.py 
```
cd project
```
15. Run commands
```
python manage.py crontab add
service cron start
python manage.py migrate
```
16. Congratulation, you have installed XapiProject 
