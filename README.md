#setup#

1. install python3 `sudo apt-get install python3`
2. install virutalenv `sudo apt-get install virtualenv`
3. clone this repo somewhere `git clone blah blah blah` 
4. cd into repo foldoer `cd ~/ozzytron-slack`
5. make a virtual env `virtualenv -p python3 .venv`
6. activate virtual env `source ./.venv/bin/activate`
7. install requirement `pip install -r requirements.txt`
8. add config `mkdir instance`, `vi ozzytron.cfg`, add entries for `BOT_OAUTH` and `BASE_SLACK_API`
9. test debug server wtih `python app.py`

#deploying (just google nginx + gunicorn)#
1. get nginx `sudo apt-get install nginx`
2. create systemd entry so gunicorn service runs in background, `sudo nano /etc/systemd/system/ozzytron.service`, make it look like:

```
[Unit]
Description=Gunicorn instance to serve ozzytron
After=network.target

[Service]
User=your-user-here
Group=www-data
WorkingDirectory=/path/to/checkout/of/ozzytron-slack
Environment="PATH=/path/to/checkout/of/ozzytron-slack/.venv/bin"
ExecStart=/path/to/checkout/of/ozzytron-slack/.venv/bin/gunicorn --workers 3 --bind unix:ozzytron.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

3. start service `sudo systemctl start ozzytron`
4. check status `sudo systemctl status ozzytron`
5. if everything good then enable on boot `sudo systemctl enable ozzytron`
6. now wire it into your nginx config like this:

```
    location /ozzytron {
        rewrite ^/ozzytron(.+)$ /$1 break;
        include proxy_params;
        proxy_pass http://unix:/path/to/checkout/of/ozzytron-slack/ozzytron.sock;
        proxy_redirect     off;

        proxy_set_header   Host                 $host;
        proxy_set_header   X-Real-IP            $remote_addr;
        proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto    $scheme;
    }
```
