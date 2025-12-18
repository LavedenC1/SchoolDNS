# SchoolDNS

Bypass school content blockers

## Usage (for users)

### Short explanation
Let's say `poki.com` is blocked
<br>The answer to fix this is easy.
<br>By default, the `victim` is `school.com`
<br>So, instead of typing in `poki.com`, type in:
<br>`poki.com.school.com`
<br>You got access to blocked website!<br>

### How to get it set up

1. Go to your wifi settings
2. Find DNS server settings in the wifi settings
3. Set it to custom DNS servers
4. Enter the IP which is given
5. Disconnect/Reconnect to wifi or reboot
6. It's done, and permanent!
> If you can't change your DNS settings, use ONCs to force it

## For hosters
> This is built for linux, I haven't tried it on windows.<br>I assume you have basic knowledge of DNS
### Set it up

1. Clone the repo (on the server)
```
git clone https://github.com/LavedenC1/SchoolDNS.git
```
2. Create venv/Install requirements
```
python3 -m venv .venv
pip install -r requirements.txt
```
3. Run it (with sudo)
```
sudo .venv/bin/python3 server.py
```

4. Done, just share your server's public ip
5. (If you want, create a systemd service to keep it running)