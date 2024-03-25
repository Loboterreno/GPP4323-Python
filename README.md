# GPP4323-Python
Library to control the GW-instek GPP4323 through visa commands

Usage:
The library can be easily tested doing an import of it and then running the commands of connect and get device information

ex:

python
import INST_GPP4323
INST_GPP4323.connect()
>>INST_GPP4323.get_device_identity()
>>"GW INSTEK, GPP-3323,  SN: xxxxxxxx, Vx.xx "
