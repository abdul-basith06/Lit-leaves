# server {
#     listen 80;
#     server_name 16.170.98.1, www.litleaves.store, litleaves.store;

#     location = /favicon.ico { access_log off; log_not_found off; }
   
#     location / {
#         include proxy_params;
#         proxy_pass http://unix:/run/gunicorn.sock;
#     }
# }