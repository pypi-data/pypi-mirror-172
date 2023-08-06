# Fellas in COMPSCI 399
Kiwrious Python Sensor Library - An open-source Python library for programming with real-time sensor data. 

## Background  
Input to programs created using Python typically happen using keyboard and mouse. The ability to incorporate real-time
environmental data measured through sensors as input could open doors to new programming experiences.

With this in mind, we have developed a toolkit consisting of six plug-and-play Kiwrious USB sensors that measure various physical phenomena such as humidity, temperature, conductance, air quality, light and heart rate.

## Project Description
The goal of this project is to develop a python library that services all sensor communications to allow users to easily program with their data.

Basic functions that the library should handle include establishing stable sensor connectivity, decoding live sensor data and
providing appropriate methods for working with this data.

Users can then use this sensor data in tasks like visualizations (e.g. Matplotlib), creating data models for investigations (e.g. sci-kit) or developing games that react to changes in the environment (e.g. pygame).

## Installation Guide
This library can be installed through pip like so:

    python -m pip install kiwrious
    
## Available Resources

Below are the available methods included in this library as well as a brief description of their function:

```get_raw_data(sensor_type)```  
This method takes a specified sensor as an input and returns a list of the raw packet data in the form of a byte string.

```get_connected_sensors()```  
This method returns a list of all Kiwrious sensors that are connected to your computer.

```get_sensor_reading(sensor_type)```  
This method takes in a specfied sensor as an input and returns the processed data reading. Each sensor will return two different readings, which are specified in the returned list.  
If no sensor is specified, it will automatically detect the connected sensor(s) and return the data readings.

### Callback Methods
This library also includes callback methods, which allows the user to specify a defined method to run once the callback's condition has been met. A brief description and their functions are described below:  

``` on_sensor_connection(callback_method, sensor_type, timeout, close_on_completion, *args) ```  
This callback method enables the user to run their self-defined function once a sensor is connected to the computer. The arguments of this callback method are defined as: 

callback_method: the user defined method to run  
sensor_type: the sensor that the callback looks for to run callback_method once it is connected. If no sensor_type is specified, callback_method will run once any sensor is connected  
timeout: the amount of time the service waits for a sensor to be connected before exiting the program. By default, this is set to 0, meaning it will never automatically exit  
close_on_completion: a boolean value which is set to False by default. If set to True, the service will stop once callback_method has completed  
args: these are the arguments that will be passed to callback_method

``` on_sensor_disconnect(callback_method, sensor_type, timeout, close_on_completion, *args) ```  
This callback method enables the user to run their self-defined function once a sensor has been disconnected from the computer. The arguments for this method are the same as the above.

## Basic Usage
Once the Kiwrious library has been installed, it is quite easy to start reading data from the sensors. You simply import the library into a python file and do the following:
```
my_service = KiwriousService()
my_service.start_service()

my_service.get_sensor_reading(my_service.HUMIDITY)

my_service.stop_service
```

## Demo Programs
You can access some demo programs to get an idea of the more in depth usage of the library [here](link_here.com)
