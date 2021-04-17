# cron: Multiple docker container

This docker-compose file will create 2 containers. The first one handles certbot, and the second one provides cron which
restarts the certbot container at the specified time interval to renew the created certificate.

## Usage

Download all files from this folder and place them into a single folder. Also adjust all placeholder
values `<placeholder-name>` in the `docker-compose.yml` file.

You can adjust the renewal time interval in the `crontab` file. By default, the time interval is 8 days at 3am.

Now just start all docker container with docker-compose:

```commandline
docker-compose up -d
```

The certbot container will stop after completion, while the cron container will run until it is manually stopped.

Do not remove the certbot container, otherwise the container can no longer be restarted by the cron container.

---

**Note:** Using cron in a Docker container to run scheduled jobs in it may not work properly and reliably in certain
situations. For example, when the container is recreated and thus the already elapsed time is not correctly accounted.
This is not so problematic with short time intervals (only a few minutes), but a cron job with several days or weeks is
more affected by this. Outsourcing cron to its own container like this example instead of a single container with
certbot + cron can reduce the mentioned problem with unreliability, but it cannot always be ensured for productive use.
A much more reliable method would be to use cron on the host system or a completely different method to schedule tasks.
**Before using the cron example, please be aware of what exactly you are doing.**

**Warning:** the cron container mounts
the [docker socket](https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-socket-option), which may has
some security risks.
