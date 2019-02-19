# The allmighty MVG Checker for RaspberryPi

run it:
```
docker run -dt -e MVG_CHECKER='["marienplatz", "karlsplatz"]' zepp/mvg-checker:latest
```

and check the webinterfaces:
http://127.0.0.1/marienplatz
http://127.0.0.1/karlsplatz

If you got the 7 Inch Display (or any other) connected to your RaspberryPi you can have a fancy Display in your room :-)

# How it works

Pass your stations of interest as environment variables as in the example above and the rest is autogenerated. If you don't pass any environment variables, defaults will jump in.
It checks the MVG API for the corresponding ID of your station, then fetches the latest data and provides it via Flask.

There is no "main-entrypoint" right now like an `index.html`, all pages are autogenerated by their name / station. Same for the menu. Yes, its very simple.

# Configure the Raspberry

add `pi` user to docker group:
```
sudo usermod -aG docker pi
```

correct the brightness of the screen:
```
sudo echo 50 > /sys/class/backlight/rpi_backlight/brightness
```

create autostart config
```
mkdir -p /home/pi/.config/lxsession/LXDE-pi/
cat <<EOF > /home/pi/.config/lxsession/LXDE-pi/autostart
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@point-rpi
@bash /home/pi/kiosk.sh
EOF
```

create `/home/pi/kiosk.sh` with the following content:
```
#!/bin/bash

# cleanup docker and start container
/usr/bin/docker rm --name mvgchecker
/usr/bin/docker container rm $(/usr/bin/docker container ls -aq)
/usr/bin/docker rmi zepp/mvg-checker:latest
/usr/bin/docker run -dt --name mvgchecker -p 80:80 -e MVG_CHECKER='["prinzregentenplatz", "marienplatz", "karlsplatz"]' zepp/mvg-checker:latest

# no warnings etc in chromium
unclutter -idle 0.5 -root &
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/pi/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/pi/.config/chromium/Default/Preferences

/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk http://127.0.0.1/prinzregentenplatz &

# autoreload
while true; do
    xdotool keydown ctrl+r; xdotool keyup ctrl+r;
    sleep 60
done
```
