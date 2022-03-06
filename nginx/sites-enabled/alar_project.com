server {

    listen 188;

    server_name localhost;
    charset utf-8;

    location /api {
        proxy_pass http://backend:8888;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location ^~ / {
        alias /usr/src/app/static/;
        try_files $uri /index.html;
        autoindex off;
    }
}