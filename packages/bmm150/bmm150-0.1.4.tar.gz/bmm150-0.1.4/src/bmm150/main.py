from .bmm150_defs import *
import time

import ctypes
import smbus2  # type: ignore


class BMM150:
    settings = bmm150_settings()
    raw_mag_data = bmm150_raw_mag_data()
    mag_data = bmm150_mag_data()
    trim_data = bmm150_trim_registers()

    def __init__(self, bus_number=1):
        """
        :param bus_number: The used i2c bus, defaults to 1
        :type bus_number: int

        :return: None
        :rtype: None
        """
        self.bus_number = bus_number

        self.i2c_bus = smbus2.SMBus(bus_number)

    def initialize(self):

        # Power up the sensor from suspend to sleep mode
        self.set_op_mode(BMM150_SLEEP_MODE)
        time.sleep(BMM150_START_UP_TIME / 1000.0)

        # Check chip ID
        chip_id = self.i2c_bus.read_byte_data(BMM150_I2C_Address, BMM150_CHIP_ID_ADDR)
        if chip_id != BMM150_CHIP_ID:
            return BMM150_E_ID_NOT_CONFORM

        # Function to update trim values
        self.read_trim_registers()

        # Setting the power mode as normal
        self.set_op_mode(BMM150_NORMAL_MODE)

        #  Setting the preset mode as Low power mode
        #    i.e. data rate = 10Hz XY-rep = 1 Z-rep = 2
        self.set_presetmode(BMM150_PRESETMODE_LOWPOWER)
        # set_presetmode(BMM150_HIGHACCURACY_REPZ)

        return BMM150_OK

    def set_op_mode(self, pwr_mode):
        # Select the power mode to set
        if pwr_mode == BMM150_NORMAL_MODE:
            #  If the sensor is in suspend mode
            #    put the device to sleep mode
            self.suspend_to_sleep_mode()
            # write the op mode
            self.write_op_mode(pwr_mode)
        elif pwr_mode == BMM150_FORCED_MODE:
            #  If the sensor is in suspend mode
            #    put the device to sleep mode
            self.suspend_to_sleep_mode()
            # write the op mode
            self.write_op_mode(pwr_mode)
        elif pwr_mode == BMM150_SLEEP_MODE:
            #  If the sensor is in suspend mode
            #    put the device to sleep mode
            self.suspend_to_sleep_mode()
            # write the op mode
            self.write_op_mode(pwr_mode)
        elif pwr_mode == BMM150_SUSPEND_MODE:
            # Set the power control bit to zero
            self.set_power_control_bit(BMM150_POWER_CNTRL_DISABLE)

    def suspend_to_sleep_mode(self):
        self.set_power_control_bit(BMM150_POWER_CNTRL_ENABLE)
        # Start-up time delay of 3ms
        time.sleep(BMM150_START_UP_TIME / 1000.0)

    def write_op_mode(self, op_mode):
        reg_data = self.i2c_bus.read_byte_data(BMM150_I2C_Address, BMM150_OP_MODE_ADDR)
        # Set the op_mode value in Opmode bits of 0x4C
        reg_data = BMM150_SET_BITS(
            reg_data, BMM150_OP_MODE_MSK, BMM150_OP_MODE_POS, op_mode
        )
        self.i2c_bus.write_byte_data(BMM150_I2C_Address, BMM150_OP_MODE_ADDR, reg_data)

    def set_power_control_bit(self, pwrcntrl_bit):
        # Power control register 0x4B is read
        reg_data = self.i2c_bus.read_byte_data(
            BMM150_I2C_Address, BMM150_POWER_CONTROL_ADDR
        )
        # Sets the value of power control bit
        reg_data = BMM150_SET_BITS_POS_0(reg_data, BMM150_PWR_CNTRL_MSK, pwrcntrl_bit)
        self.i2c_bus.write_byte_data(
            BMM150_I2C_Address, BMM150_POWER_CONTROL_ADDR, reg_data
        )

    def set_presetmode(self, preset_mode):
        if preset_mode == BMM150_PRESETMODE_LOWPOWER:
            #  Set the data rate x,y,z repetition
            #    for Low Power mode
            self.settings.data_rate = BMM150_DATA_RATE_10HZ
            self.settings.xy_rep = BMM150_LOWPOWER_REPXY
            self.settings.z_rep = BMM150_LOWPOWER_REPZ
            self.set_odr_xyz_rep()
        elif preset_mode == BMM150_PRESETMODE_REGULAR:
            #  Set the data rate x,y,z repetition
            #    for Regular mode
            self.settings.data_rate = BMM150_DATA_RATE_10HZ
            self.settings.xy_rep = BMM150_REGULAR_REPXY
            self.settings.z_rep = BMM150_REGULAR_REPZ
            self.set_odr_xyz_rep()
        elif preset_mode == BMM150_PRESETMODE_HIGHACCURACY:
            #  Set the data rate x,y,z repetition
            #    for High Accuracy mode
            self.settings.data_rate = BMM150_DATA_RATE_20HZ
            self.settings.xy_rep = BMM150_HIGHACCURACY_REPXY
            self.settings.z_rep = BMM150_HIGHACCURACY_REPZ
            self.set_odr_xyz_rep()
        elif preset_mode == BMM150_PRESETMODE_ENHANCED:
            #  Set the data rate x,y,z repetition
            #    for Enhanced Accuracy mode
            self.settings.data_rate = BMM150_DATA_RATE_10HZ
            self.settings.xy_rep = BMM150_ENHANCED_REPXY
            self.settings.z_rep = BMM150_ENHANCED_REPZ
            self.set_odr_xyz_rep()

    def set_odr_xyz_rep(self):
        # Set the ODR
        self.set_odr()
        # Set the XY-repetitions number
        self.i2c_bus.write_byte_data(
            BMM150_I2C_Address, BMM150_REP_XY_ADDR, self.settings.xy_rep
        )
        # Set the Z-repetitions number
        self.i2c_bus.write_byte_data(
            BMM150_I2C_Address, BMM150_REP_Z_ADDR, self.settings.z_rep
        )

    def set_odr(self):
        reg_data = self.i2c_bus.read_byte_data(BMM150_I2C_Address, BMM150_OP_MODE_ADDR)
        # Set the ODR value
        reg_data = BMM150_SET_BITS(
            reg_data, BMM150_ODR_MSK, BMM150_ODR_POS, self.settings.data_rate
        )
        self.i2c_bus.write_byte_data(BMM150_I2C_Address, BMM150_OP_MODE_ADDR, reg_data)

    def soft_reset(self):
        reg_data = self.i2c_bus.read_byte_data(
            BMM150_I2C_Address, BMM150_POWER_CONTROL_ADDR
        )
        reg_data = reg_data | BMM150_SET_SOFT_RESET
        self.i2c_bus.write_byte_data(
            BMM150_I2C_Address, BMM150_POWER_CONTROL_ADDR, reg_data
        )
        time.sleep(BMM150_SOFT_RESET_DELAY / 1000.0)

    def read_trim_registers(self):
        trim_x1y1 = self.i2c_bus.read_i2c_block_data(
            BMM150_I2C_Address, BMM150_DIG_X1, 2
        )
        trim_xyz_data = self.i2c_bus.read_i2c_block_data(
            BMM150_I2C_Address, BMM150_DIG_Z4_LSB, 4
        )
        trim_xy1xy2 = self.i2c_bus.read_i2c_block_data(
            BMM150_I2C_Address, BMM150_DIG_Z2_LSB, 10
        )

        #  Trim data which is read is updated
        #    in the device structure
        self.trim_data.dig_x1 = trim_x1y1[0]
        self.trim_data.dig_y1 = trim_x1y1[1]

        self.trim_data.dig_x2 = trim_xyz_data[2]
        self.trim_data.dig_y2 = trim_xyz_data[3]

        temp_msb = trim_xy1xy2[3] << 8
        self.trim_data.dig_z1 = temp_msb | trim_xy1xy2[2]

        temp_msb = trim_xy1xy2[1] << 8
        self.trim_data.dig_z2 = temp_msb | trim_xy1xy2[0]

        temp_msb = trim_xy1xy2[7] << 8
        self.trim_data.dig_z3 = temp_msb | trim_xy1xy2[6]

        temp_msb = trim_xyz_data[1] << 8
        self.trim_data.dig_z4 = temp_msb | trim_xyz_data[0]

        self.trim_data.dig_xy1 = trim_xy1xy2[9]
        self.trim_data.dig_xy2 = trim_xy1xy2[8]

        temp_msb = trim_xy1xy2[5] & 0x7F << 8
        self.trim_data.dig_xyz1 = temp_msb | trim_xy1xy2[4]

    def read_raw_mag_data(self):
        """
        Reads registers containing X, Y, Z and R data from the device.

        :return: None
        :rtype: None
        """
        reg_data = self.i2c_bus.read_i2c_block_data(
            BMM150_I2C_Address, BMM150_DATA_X_LSB, BMM150_XYZR_DATA_LEN
        )

        # Mag X axis data
        reg_data[0] = BMM150_GET_BITS(reg_data[0], BMM150_DATA_X_MSK, BMM150_DATA_X_POS)
        # Convert to a c-type int8, to add a twos-complement awareness
        reg_data[1] = ctypes.c_int8(reg_data[1]).value
        # Shift the MSB data to left by 5 bits
        # Multiply by 32 to get the shift left by 5 value
        msb_data = reg_data[1] * 32
        # Raw mag X axis data
        self.raw_mag_data.raw_datax = msb_data | reg_data[0]

        # Mag Y axis data
        reg_data[2] = BMM150_GET_BITS(reg_data[2], BMM150_DATA_Y_MSK, BMM150_DATA_Y_POS)
        # Convert to a c-type int8, to add a twos-complement awareness
        reg_data[3] = ctypes.c_int8(reg_data[3]).value
        # Shift the MSB data to left by 5 bits
        # Multiply by 32 to get the shift left by 5 value
        msb_data = reg_data[3] * 32
        # Raw mag Y axis data
        self.raw_mag_data.raw_datay = msb_data | reg_data[2]

        # Mag Z axis data
        reg_data[4] = BMM150_GET_BITS(reg_data[4], BMM150_DATA_Z_MSK, BMM150_DATA_Z_POS)
        # Convert to a c-type int8, to add a twos-complement awareness
        reg_data[5] = ctypes.c_int8(reg_data[5]).value
        # Shift the MSB data to left by 7 bits
        # Multiply by 128 to get the shift left by 7 value
        msb_data = reg_data[5] * 128
        # Raw mag Z axis data
        self.raw_mag_data.raw_dataz = msb_data | reg_data[4]

        # Mag R-HALL data
        # R-hall is always unsigned, no need for twos-complement awareness
        reg_data[6] = BMM150_GET_BITS(
            reg_data[6], BMM150_DATA_RHALL_MSK, BMM150_DATA_RHALL_POS
        )
        self.raw_mag_data.raw_data_r = reg_data[7] << 6 | reg_data[6]

        return (
            self.raw_mag_data.raw_datax,
            self.raw_mag_data.raw_datay,
            self.raw_mag_data.raw_dataz,
            self.raw_mag_data.raw_data_r,
        )

    def read_mag_data(self):

        self.read_raw_mag_data()

        # Compensated Mag X data in floating point format
        self.mag_data.x = self.compensate_x(
            self.raw_mag_data.raw_datax, self.raw_mag_data.raw_data_r
        )
        # Compensated Mag Y data in floating point format
        self.mag_data.y = self.compensate_y(
            self.raw_mag_data.raw_datay, self.raw_mag_data.raw_data_r
        )
        # Compensated Mag Z data in floating point format
        self.mag_data.z = self.compensate_z(
            self.raw_mag_data.raw_dataz, self.raw_mag_data.raw_data_r
        )

        return self.mag_data.x, self.mag_data.y, self.mag_data.z

    # @brief This internal API is used to obtain the compensated
    # magnetometer X axis data(micro-tesla) in floating point.

    def compensate_x(self, mag_data_x, data_rhall):

        # /* Overflow condition check */
        if ((mag_data_x != BMM150_XYAXES_FLIP_OVERFLOW_ADCVAL) and (data_rhall != 0) and (self.trim_data.dig_xyz1 != 0)) :
            # /* Processing compensation equations */
            process_comp_x0 = ((self.trim_data.dig_xyz1) * 16384.0 / data_rhall)
            retval = (process_comp_x0 - 16384.0)
            process_comp_x1 = (self.trim_data.dig_xy2) * (retval * retval / 268435456.0)
            process_comp_x2 = process_comp_x1 + retval * (self.trim_data.dig_xy1) / 16384.0
            process_comp_x3 = (self.trim_data.dig_x2) + 160.0
            process_comp_x4 = mag_data_x * ((process_comp_x2 + 256.0) * process_comp_x3)
            retval = ((process_comp_x4 / 8192.0) + ((self.trim_data.dig_x1) * 8.0)) / 16.0
        else :
            # /* Overflow, set output to 0.0 */
            retval = BMM150_OVERFLOW_OUTPUT

        return retval

    # @brief This internal API is used to obtain the compensated
    # magnetometer Y axis data(micro-tesla) in floating point.

    def compensate_y(self, mag_data_y, data_rhall):

        # /* Overflow condition check */
        if ((mag_data_y != BMM150_XYAXES_FLIP_OVERFLOW_ADCVAL) and (data_rhall != 0) and (self.trim_data.dig_xyz1 != 0)) :
            # /* Processing compensation equations */
            process_comp_y0 = (self.trim_data.dig_xyz1) * 16384.0 / data_rhall
            retval = process_comp_y0 - 16384.0
            process_comp_y1 = (self.trim_data.dig_xy2) * (retval * retval / 268435456.0)
            process_comp_y2 = process_comp_y1 + retval * (self.trim_data.dig_xy1) / 16384.0
            process_comp_y3 = (self.trim_data.dig_y2) + 160.0
            process_comp_y4 = mag_data_y * (((process_comp_y2) + 256.0) * process_comp_y3)
            retval = ((process_comp_y4 / 8192.0) + ((self.trim_data.dig_y1) * 8.0)) / 16.0
        else :
            # /* Overflow, set output to 0.0 */
            retval = BMM150_OVERFLOW_OUTPUT

        return retval

    # @brief This internal API is used to obtain the compensated
    # magnetometer Z axis data(micro-tesla) in floating point.

    def compensate_z(self, mag_data_z, data_rhall):

        # /* Overflow condition check */
        if ((mag_data_z != BMM150_ZAXIS_HALL_OVERFLOW_ADCVAL) and (self.trim_data.dig_z2 != 0) and
            (self.trim_data.dig_z1 != 0) and (self.trim_data.dig_xyz1 != 0) and (data_rhall != 0)):
            #  /* Processing compensation equations */
            process_comp_z0 = (mag_data_z) - (self.trim_data.dig_z4)
            process_comp_z1 = (data_rhall) - (self.trim_data.dig_xyz1)
            process_comp_z2 = ((self.trim_data.dig_z3) * process_comp_z1)
            process_comp_z3 = (self.trim_data.dig_z1) * (data_rhall) / 32768.0
            process_comp_z4 = (self.trim_data.dig_z2) + process_comp_z3
            process_comp_z5 = (process_comp_z0 * 131072.0) - process_comp_z2
            retval = (process_comp_z5 / ((process_comp_z4) * 4.0)) / 16.0
        else :
            # /* Overflow, set output to 0.0 */
            retval = BMM150_OVERFLOW_OUTPUT

        return retval
