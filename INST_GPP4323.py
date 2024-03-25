##
## GPP4323 Library
##
## This library has been made to operate the basic functionalities of the GPP4323
## such as connect, measure, set voltage, set intensity and turn ON and OFF the 
## each of the channels of the GPP-4323.
## Author : German G.
##

from math import isnan
import pyvisa
from functools import wraps
from pyvisa.constants import StopBits, Parity

#Constants initialization
TIMEOUT= 2000
TERMINATION = "\n"
BAUD_RATE=57600   ## configured at the GPP4323
DATA_BITS=8      ## default at the GPP4323
DEVICE_DESCRIPTION = "ASRL13::INSTR"
DEVICE_NAME = "GPP4323"
DEBUG = True

#Variable initialization
I = "I"
V = "V"
v = "V"
i = "I"

## Connectivity error handler
def connectivity_error_handler(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except NameError as e:
            print(DEVICE_NAME+":ERROR.Device not connected.Use "+DEVICE_NAME+".connect() first")
        except AssertionError as e:
            print(DEVICE_NAME+":ERROR.Could not perform action.Check the device is correctly detected by the OS, or the connection parameters are adequate.")
        except AttributeError as e:
            print(DEVICE_NAME+":ERROR.Device not connected.Check the device is correctly detected by the OS, or the connection parameters are adequate.")
    return decorator

## Connects to the GPP4323. Since this device behaves as any random Serial port device,
## the connection settings must be specified.
def connect(): 
    global instrument
    rm = pyvisa.ResourceManager()
    rlist = rm.list_resources()
    instrument = None
    for resource in rlist:
        if DEVICE_DESCRIPTION in resource:
            instrument = rm.open_resource(resource, baud_rate=BAUD_RATE, data_bits=DATA_BITS, parity=Parity.none, stop_bits=StopBits.one)
            instrument.read_termination = TERMINATION
            instrument.write_termination = TERMINATION
            instrument.timeout = TIMEOUT
            print(DEVICE_NAME+":Correctly detected and connected")
            return True
    if instrument == None:
            print(DEVICE_NAME+":ERROR.Device not detected.Check connection cables, drivers or instrument at OS settings. Current instrument description:'"+DEVICE_DESCRIPTION+"'")
            return False
     
def disconnect(): 
    global instrument
    response = instrument.close()
    return response
     
## Upon loading the library, the device will attempt a connection     
#connect()
## Ask for the IDN of the device in VISA programming language -OK
## example command: SSA3075X.get_device_identity()
@connectivity_error_handler
def get_device_identity():
    global instrument
    command = "*IDN?"
    instrument.write(command)
    #print("Sending: "+command )
    response = instrument.read()
    return response

@connectivity_error_handler
def get_measured_voltage(N): # N defined as the channel
    global instrument 
    
    if N not in [1,2,3,4]:
        print("Unexpected values")
    command = "MEAS"+str(N)+":VOLT?"

    instrument.write(command)
    #print("Sending: "+command )
    response = instrument.read()
    #print(response)
    return response
    
@connectivity_error_handler
def get_measured_current(N): # N defined as the channel
    global instrument 
    
    if N not in [1,2,3,4]:
        print("Unexpected values")
    command = "MEAS"+str(N)+":CURR?"

    instrument.write(command)
    #print("Sending: "+command )
    response = instrument.read()
    #print(response)
    return response

@connectivity_error_handler
def get_measured_power(N): # N defined as the channel and T "type" I, V or power
    global instrument 
    
    if N not in [1,2,3,4]:
        print("Unexpected values")

    command = "MEAS"+str(N)+":POWER?"

    instrument.write(command)
    #print("Sending: "+command )
    measurement = instrument.read()
    #print(measurement)
    return measurement

@connectivity_error_handler
def get_state(N): # N defined as the channel and S "ON" or "OFF"    
    global instrument
        
    if N not in [1,2,3,4]:
        print("Unexpected values")

    command = "OUTP"+str(N)+":STAT?"
    instrument.write(command)
    response = instrument.read()
    #print(response)
    return response

@connectivity_error_handler
def set_state(N,S): # N defined as the channel and S "ON" or "OFF"    
    global instrument
        
    if N not in [1,2,3,4]:
        print("Unexpected values")

    if S == "ON":
        T = "STAT ON"
    elif S == "on":
        T = "STAT ON"
    elif S == "On":
        T = "STAT ON"
    else:
        T= "STAT OFF"

    command = "OUTP"+str(N)+":"+T

    instrument.write(command)
    #print("Sending: "+command )

@connectivity_error_handler
def set_voltage_protection(N,v): # N defined as the channel and v voltage value
    global instrument
        
    if N not in [1,2,3,4]:
        print("Unexpected values")

    if isnan(v):
        print("voltage not a number")
        
    command = "OUTP"+str(N)+":OVP "+str(v)
    instrument.write(command)
    #print("Sending: "+command )

@connectivity_error_handler
def set_current_protection(N,i): # N defined as the channel and i current value
    global instrument
    
    if N not in [1,2,3,4]:
        print("Unexpected values")

    if isnan(i):
        print("voltage not a number")
        
    command = "OUTP"+str(N)+":OCP "+str(i)
    instrument.write(command)
    #print("Sending: "+command )

@connectivity_error_handler
def get_voltage(N): # N defined as the channel
    global instrument
        
    if N not in [1,2,3,4]:
        print("Unexpected values")
        
    command = "SOUR"+str(N)+":VOLT?"

    instrument.write(command)
    #print("Sending: "+command )
    measurement = instrument.read()
    #print(measurement)
    return measurement

@connectivity_error_handler
def set_voltage(N,V): # N defined as the channel and v voltage value
    global instrument
        
    if N not in [1,2,3,4]:
        print("Unexpected values")

    if isnan(V):
        print("voltage not a number")
        
    command = "SOUR"+str(N)+":VOLT "+str(V)
    instrument.write(command)
    #print("Sending: "+command )

@connectivity_error_handler
def get_current(N): # N defined as the channel 
    global instrument
        
    if N not in [1,2,3,4]:
        print("Unexpected values")
        
    command = "SOUR"+str(N)+":CURR?"

    instrument.write(command)
    #print("Sending: "+command )
    measurement = instrument.read()
    #print(measurement)
    return measurement

@connectivity_error_handler
def set_current(N,I): # N defined as the channel and i current value
    global instrument
        
    if N not in [1,2,3,4]:
        print("Unexpected values")

    if isnan(I):
        print("voltage not a number")
        
    command = "SOUR"+str(N)+":CURR "+str(I)
    instrument.write(command)
    #print("Sending: "+command )

#exit()