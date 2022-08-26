### Requirements
1. Edge computing solution: Intel [NUC](https://www.intel.com/content/www/us/en/products/details/nuc.html) or Nvidia Jetson [Xavier NX](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-xavier-nx/) if using deep learning 
2. Ubuntu 18.04 
3. Opencv installation <br>
```sudo apt-get install python3-pip```<br>
```pip3 install scikit-build -i https://mirrors.aliyun.com/pypi/simple```<br>
```pip3 install pip -U```<br>
```pip3 install cmake -i https://mirrors.aliyun.com/pypi/simple```<br>
```pip3 install opencv-python -i https://mirrors.aliyun.com/pypi/simple```<br>
4. Other dependencies <br>
```pipreqs ./ --encoding=utf8 --force``` <br>
```pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple```<br>

### PLC connection
1. List system port:
```dmesg | grep ttyS*```<br>
2. Modify port authentication: 
```sudo usermod -aG dialout username```<br>
3. [modbus_tk](https://github.com/ljean/modbus-tk) for PLC and PC communication

### Ubuntu18.04 auto-suspend prohibition
1. Check sleep status: ```systemctl status sleep.target```<br>
2. Mask sleep status: ```sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target```<br>
3. Install ```sudo apt-get install gnome-tweak-tool```<br>
Run: ```gnome-tweaks``` and turn OFF "Suspend when laptop lid is closed"

### Auto execute python scripts when system boots
1. Run: ```gnome-session-properties```<br>
2. Add Command: ```gnome-terminal -x python3 xxx.py ```<br>

