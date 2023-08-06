
# pull official base image
FROM nginx:latest

LABEL fm.trove.image.name="Trove Cleaners React UI"
LABEL fm.trove.image.authors="Brian Farrell <brian.farrell@me.com>"

RUN rm /etc/nginx/conf.d/default.conf

COPY ./container /
COPY ./build /usr/share/nginx/html/

EXPOSE 80

CMD nginx -g "daemon off;"
