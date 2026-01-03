FROM php:8.2-cli

ENV user warp

RUN adduser $user
ADD ./deploy/php /var/www/html
WORKDIR /var/www/html

USER $user
