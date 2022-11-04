# autoDimmingService
Sets the master brightness of the trees to a smaller value at nighttime hours. This works
with Squared and not Entwined. It does seem to correctly make a system request to Entwined,
but the master brightness gets overwritten every second.

Code was ported to Python3 in 2022. Look for checkins before then if you need to revive
the python2 version for some reason.

# Instructions
* Change the path in `autodimmer.service` to reflect where you cloned this directory
* Edit lines 9-12 in autoDimmingService.py and change the times it turns on and off and also the brightness
```
dimmingStartHour =  23
dimmingEndHour = 16
dimmedBrightness = 0
nonDimmedBrightness = 1
```
* Copy service to /etc/systemd/system `sudo cp ./autodimmer.service /etc/systemd/system`
* Set the privs correctly - `sudo chmod 0644 /etc/systemd/system/autodimmer.service`
* Enable the service `sudo systemctl enable autodimmer`
* Reboot
* Check service `sudo systemctl status autodimmer`
