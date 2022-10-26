# autoDimmingService
Sets the master brightness of the trees to a smaller value at nighttime hours

# Instructions
* Copy service to /etc/systemd/system "sudo cp ./squaredDimmingService /etc/systemd/system"
* Enable the service "sudo systemctl enable squaredDimmingService"
* Reboot
* Check service "sudo systemctl status squaredDimmingService"
* Edit lines 9-12 in autoDimmingService.py and change the times it turns on and off and also the brightness
```
dimmingStartHour =  7
dimmingEndHour = 8
dimmedBrightness = 1
nonDimmedBrightness = 1
```
