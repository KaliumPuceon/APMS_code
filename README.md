# APMS Source Code

This code repository contains all the software required to operate an Automated Penguin Monitoring
System, including an installation script.

## Contents

### hx711py

This is a duplicate of [Tatobari's HX711 interface library](https://github.com/tatobari/hx711py).

### res

This is a collection of resources used when setting up the APMS, including cronjobs, fstab entries
and sudoers file rules.

### scripts

These are the management scripts used in the running of the APMS.

* `scripts/gsm.sh` sets up the SIM7600E 4G modem as a USB network device
* `scripts/connect.py` manages the reverse SSH tunnel

### systemd

These are systemd services responsible for keeping the system alive automatically. They are
installed to the system services by `setup.sh`

### testing

These scripts and tools are used to run simulated tests of the APMS

### tuxcap_v2

The core software for the APMS, provides the data collecting features

* `camera.py` captures a video buffer from a USB webcam
* `fake_hx711.py` is a stand-in HX711 library used for simulated tests
* `main.py` is the central coordinating process for the APMS
* `rfid.py` provides logging and reading features for the USB RFID device, as well as triggering the
  camera
* `scale.py` reads from the scale and logs to disk, as well as triggering the camera
* `tuxconf.py` contains a set of use-editable configuration options for the monitoring system

### setup.sh

An automatic installation script.

# Installing

To begin, download this repository and extract it. Move the contents of the respository into the
home directory of the default `pi` user of a new Raspbian Lite installation. Ensure that you have a
reliable internet connection, and run the `setup.sh` script as root. This will install all the
required packages, modify user permissions, install fstab rules and set up services.
