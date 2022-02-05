from machine import SPI, Pin


class MCP300X(object):
    """
    MCP3008 Differential channel mapping. The following list of available differential readings
    takes the form ``(positive_pin, negative_pin) = (channel A) - (channel B)``.
    - (P0, P1) = CH0 - CH1
    - (P1, P0) = CH1 - CH0
    - (P2, P3) = CH2 - CH3
    - (P3, P2) = CH3 - CH2
    - (P4, P5) = CH4 - CH5
    - (P5, P4) = CH5 - CH4
    - (P6, P7) = CH6 - CH7
    - (P7, P6) = CH7 - CH6
    """

    def __init__(self, spi_bus, cs, ref_voltage=3.3, model=8):
        # init
        self._model = model
        self._spi_bus = spi_bus
        self._ref_voltage = ref_voltage

        self._cs = cs


        # Model filter
        if not (model == 8 or
                model == 4 or
                model == 2):
            raise ValueError("Not a valid type, use \"8\" for MCP3008, \"4\" for MCP3004, or \"2\" for MCP3002 chip types")


        # Enable high on chip
        self._cs.value(1)        


    def reference_voltage(self):
        """Returns the MCP3xxx's reference voltage. (read-only)"""
        return self._ref_voltage


    def verifyModelToChannel(self, channel):
        if channel >= self._model:
            raise ValueError("Channel", channel, "is higher than model supports")


    def readRAW(self, channel, is_differential=False):
        # Model filter
        self.verifyModelToChannel(channel)
        
        # The MCP3xxx ADC has 10-bit resolution, hence 0-1023
        out_buf = bytearray(3)
        in_buf = bytearray(3)

        # Start bit
        out_buf[0] = 0x01
        
        # Select chip
        self._cs.value(0)
        try:
            out_buf[1] = ((not is_differential) << 7) | (channel << 4)
            self._spi_bus.write_readinto(out_buf, in_buf)
        
        finally:
            # De-select chip        
            self._cs.value(1)

        return in_buf


    def read(self, channel, is_differential=False):
        # Model filter
        self.verifyModelToChannel(channel)
        
        in_buf = self.readRAW(channel, is_differential)
        return ((in_buf[1] & 0x03) << 8) | in_buf[2]


    def readVolt(self, channel):
        # Model filter
        self.verifyModelToChannel(channel)
        
        value = self.read(channel)
        return (value * self._ref_voltage) / 1024


### MAIN
if __name__ == '__main__':
    import utime
    
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

    
    # demo selection, channel selection
    ar = [True, True, True, False, False, False, False, False]

    while True:
        print('--')
        # Value
        for i in range(8):
            if ar[i]:
                print("ADC Value", i, ":", mcp.read(i), "voltage:", mcp.readVolt(i), "V", "raw:", mcp.readRAW(i))

        print()

        # diff
        for i in range(8):
            if ar[i]:
                print("ADC Diff", i, ":", mcp.read(i, is_differential=True), "raw:", mcp.readRAW(i, is_differential=True))

        print()
        utime.sleep(2)
