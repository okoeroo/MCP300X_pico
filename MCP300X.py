from machine import SPI, Pin


class MCP300X(object):
    def __init__(self, model, spi_id, cs, sck_pin, mosi_pin, miso_pin, max_speed_hz=976000):
        # Modes Single
        self.CH0 = 8     # single-ended CH0
        self.CH1 = 9     # single-ended CH1
        self.CH2 = 10    # single-ended CH2
        self.CH3 = 11    # single-ended CH3
        self.CH4 = 12    # single-ended CH4
        self.CH5 = 13    # single-ended CH5
        self.CH6 = 14    # single-ended CH6
        self.CH7 = 15    # single-ended CH7

        # Modes Diff
        self.DF0 = 0     # differential CH0 = IN+ CH1 = IN-
        self.DF1 = 1     # differential CH0 = IN- CH1 = IN+
        self.DF2 = 2     # differential CH2 = IN+ CH3 = IN-
        self.DF3 = 3     # differential CH2 = IN- CH3 = IN+
        self.DF4 = 4     # differential CH4 = IN+ CH5 = IN-
        self.DF5 = 5     # differential CH4 = IN- CH5 = IN+
        self.DF6 = 6     # differential CH6 = IN+ CH7 = IN-
        self.DF7 = 7     # differential CH6 = IN- CH7 = IN+

        # const
        self.HIGH = 1
        self.LOW  = 0

        # Only accept values 4 or 8
        if model != 4 or model != 8:
            raise ValueError("Only accepts model MCP3004 or MCP3008 by value 4 or 8")

        self.max_channels = model

        # speed
        self.max_speed_hz = max_speed_hz

        # pins
        self.chipselect = cs
        self.chipselect_pin = Pin(cs, Pin.OUT)

        self.spi_id = spi_id

        self.sck  = Pin(sck_pin)
        self.mosi = Pin(mosi_pin)
        self.miso = Pin(miso_pin)

        # First stage
        self.chipSelectHigh()
        self.spi =  SPI(self.spi_id,
                        baudrate=self.max_speed_hz,
                        firstbit=SPI.MSB,
                        sck = self.sck,
                        mosi = self.mosi,
                        miso = self.miso)

    def chipSelectHigh(self):
        self.chipselect_state = self.HIGH
        self.chipselect_pin.on()

    def chipSelectLow(self):
        self.chipselect_state = self.LOW
        self.chipselect_pin.off()

    def _SPIread(self, channel, differential):
        if channel >= self.max:
            raise ValueError("Unsupported channel number selected")

        buf = bytearray(3)
        try:
            buf[0] = 0x01
            buf[1] = (differential << 7) | (channel << 4)
            buf[0] = 0x00

        ### Write buffer to SPI
        try:
            self.chipSelectLow()
            self.spi.write(buf)

            data = spi.read(2)
        finally:
            self.chipSelectHigh()

#        value = (byte1%4 << 8) + byte2
        return data


    # Read ADC channel
    # per channel
    def readADC(self, channel):
        return self._SPIread(channel, False)


    # Read differential ADC channel.
    #  0: Return channel 0 minus channel 1
    #  1: Return channel 1 minus channel 0
    #  2: Return channel 2 minus channel 3
    #  3: Return channel 3 minus channel 2
    #  4: Return channel 4 minus channel 5
    #  5: Return channel 5 minus channel 4
    #  6: Return channel 6 minus channel 7
    #  7: Return channel 7 minus channel 6
    def readADCdifferential(self, channel):
        return self._SPIread(channel, True)


### MAIN
if __name__ == '__main__':
    import utime

    print("Hello")

    adcs = 8
    spi_id = 0
    cs = 5 # GPIO 5, pin 7
    sck = 2
    mosi = 3
    miso = 4

    mcp0 = MCP300X(adcs, spi_id, cs, sck, mosi, miso)

    while True:
        for x in range(0, 8):
        print("Measure ADC:", x)

        value = mcp0.readADC(x)

        print(value)

