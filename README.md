# flask-docker-stack
 
My stack for developing, testing and deploying small Flask applications.
Services:
* MySQL database
* PHPMyAdmin
* Flask App
* nginx webserver with certbot dns-1 challenge via AWS Route53

Other features:
* compose override file for local testing and developing of the Flask App
* MySQL data persistence via a mounted folder (this means seperate local test DB and remote deployed DB)


### Configuring

1. Change \*\*mydomain.com\*\* to your domain name. In `ssl/conf.d/base.conf`
2. Set you AWS id and key in `ssl/aws/credentials` 
3. Add your flask app to `web/app`.  (Entry point is `app.py`)
4. Add any Python dependencies to `web/app/requirements.txt`
5. `docker compose build` from the flask-docker-stack directory
6. `docker compose up`

### Deploying

`docker-compose.override.yml` should not be included on the deployment server.  This override file removes SSL and makes a few other changes to the services to run locally.

If testing locally your app will be at http://127.0.0.1:5000
   