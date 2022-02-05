# MCP300X\_pico
An MCP3008, MCP3004, MCP3002 ADC converter chip for the Raspberry Pi Pico.
The MCP300x chips have a resolution of 10-bit, hence the 5V or 3.3V reference voltage is divided over the value range 0-1023.

The MCP300x requires an SPI bus to work.


### MCP3008 Pinout

| Pin | Description | Pin | Description |
|-----|:------------|:----|:------------|
| 01  |     CH0     | 09  | Vdd - Supply voltage (2.7V - 5.5V) |
| 02  |     CH1     | 10  | Vref - Reference voltage |
| 03  |     CH2     | 11  | AGND - Analog ground |
| 04  |     CH3     | 12  | CLK - SPI Clock (SCLK) |
| 05  |     CH4     | 13  | Dout - Data out (MISO) |
| 06  |     CH5     | 14  | Din - Data in (MOSI) |
| 07  |     CH6     | 15  | CS - Chip select (CE0# or CE1#) |
| 08  |     CH7     | 16  | DGND - Digital ground |


## Usage

A working example is included in the code. Import the module to make it work.
You have to create an SPI bus configuration first and pass that as initialization parameter, including the chip select and optionally the model choice.

It is also possible to measure the difference between channels.
- Channel 0 = CH0 - CH1
- Channel 1 = CH1 - CH0
- Channel 2 = CH2 - CH3
- Channel 3 = CH3 - CH2
- Channel 4 = CH4 - CH5
- Channel 5 = CH5 - CH4
- Channel 6 = CH6 - CH7
- Channel 7 = CH7 - CH6


### Example:
``` python
from MCP300X import MCP300X

spi_bus = 0
spi =  SPI(spi_bus,
           baudrate = 1000000,
           firstbit = SPI.MSB,
           sck = Pin(2),
           mosi = Pin(3),
           miso = Pin(4))

# Select chip
cs = Pin(5, mode=Pin.OUT)   # GPIO 5, pin 7

# create the mcp object
mcp = MCP300X(spi, cs, model=8)

channel = 0
print("ADC Value", channel, ":", mcp.read(channel), "voltage:", mcp.readVolt(channel), "V", "raw:", mcp.readRAW(channel))
print("ADC Value", channel, ":", mcp.read(channel, is_differential=True), "raw:", mcp.readRAW(channel, is_differential=True))
```
