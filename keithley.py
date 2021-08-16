import pyvisa
import time
import csv

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


class Keithley2400:
    def __init__(self):
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()
        self.keithley = rm.open_resource(resources[0])
        print(self.keithley.query('*IDN?'))

    def measure_current(self, start_time, end_time, delta_time, start_voltage, end_voltage, voltage_range,
                        comp_current_limit, current_range, file_name):

        self.keithley.write('*RST')
        self.keithley.write(':SOUR:FUNC VOLT')
        self.keithley.write(':SOUR:VOLT:MODE FIXED')
        self.keithley.write(':SOUR:VOLT:RANG ' + str(voltage_range))
        self.keithley.write(':SOUR:VOLT:LEV ' + str(start_voltage))
        self.keithley.write(':SENS:CURR:PROT ' + str(comp_current_limit))
        self.keithley.write(':SENS:FUNC \"CURR\"')
        self.keithley.write(':SENS:CURR:RANG ' + str(current_range))
        self.keithley.write(':FORM:ELEM TIME, VOLT, CURR')
        self.keithley.write(':SYST:TIME:RES')
        self.keithley.write(':OUTPUT ON')

        given_time = start_time
        number_of_measurements = (end_time - start_time)/delta_time
        delta_voltage = (end_voltage - start_voltage)/number_of_measurements
        current_voltage = start_voltage
        time.sleep(start_time)

        with open(file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            while given_time <= end_time:
                self.keithley.write(':SOUR:VOLT:LEV ' + str(current_voltage))
                row = self.keithley.query_ascii_values(':READ?')
                time.sleep(delta_time)
                given_time += delta_time
                current_voltage += delta_voltage
                writer.writerow(row)

        self.keithley.write('OUTPUT OFF')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
