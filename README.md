# Breast Pump Vacuum Monitoring System

This project was made for Allison Tolman (New Little Life) to test the vacuum performance of breast pumps. The project consists of a python script that interfaces with a controller, display, and pressure transducer.  
The project files also include STL file for the 3D printed hardware.

## Hardware Description

## Usage

1) Power Raspberry Pi  
2) Insert the supplied USB stick (ensure that a folder titled 'data' exists on the home directory of the drive)  
3) Select 'Continue' to enter the main menu (selections are made by pressing down on the selector stick. Moving back in the menus is done by pressing left on the selector stick.)

### Main Menu

**Run Test**

The user has the option to select from three standardized test lengths (10s, 20s, and 30s) or perform a manual length test. The standardized tests will stop on there own, analyze the data, and produce graphs to the specified folder title at the top of the screen or they can be manually stopped by selecting 'Stop Test' at anytime during the test. The manual length test requires the user to end the test by selecting 'Stop Test'. Graphs, summary, and raw data are stored in the specified folder after each test.

**Change Units**

The user has the option to select which units are used in the data analysis and graph production. When first entering the menu, the current units being used are always highlited. When a user selects new units, the program automatically reverts back to the main menu.  

**Reset LPS35**

The user has the option to re-zero the pressure transducer in the event that the reading drifts away from zero by selecting 'Zero_LPS35'. The user can also specify the transducer to use an absolute measurement, however this is not recommended.  

**Eject USB**

The user must eject the USB stick prior to physically removing it from the Raspberry Pi. This is done by selecting this menu and removing the USB stick before hitting 'Continue' on the next screen. This will send the screen back to the initial screen which requires the USB stick to be reinserted in order to enter back into the main menu.  

**Shutdown**

The user must select 'Shutdown' prior to removing the power source from the Raspberry Pi. The next screen allows the user to abort the shutdown command within 3s if it was pressed by mistake. To restart the program and raspberry pi the user will have to unplug and plug in again the power supply.  

### USB Stick

The USB stick is keyed to the program and requires a folder titled 'data' at the top directory. Test folders can be removed from the data folder at will.

## Authors

* **Paul Wadsworth** - *Initial Work*
