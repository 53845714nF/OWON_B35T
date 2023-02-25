"""
Modul to connect to B35T+.
"""

from os import system
from sys import byteorder, exit
from argparse import ArgumentParser
from binascii import unhexlify
from pexpect import exceptions, spawn


class B35T:
    """
    Class that allows the reading of B35T+.
    """

    def __init__(self, mac):
        self.child = spawn('gatttool -I')
        self.connect_to_device(mac)
        self.process_data()

    def connect_to_device(self, mac):
        """
        Connect to the B35t device
        :param mac: Bluetooth MAC Address
        """

        try:
            print(f'Connecting to {mac}')
            self.child.sendline(f'connect {mac}')
            self.child.expect('Connection successful', timeout=5)
            print('Connected!')
        except exceptions.TIMEOUT:
            print('Failed while trying to connect.')

    def process_data(self):
        """
        Processing and printing of the data.
        """

        while True:
            try:
                self.child.expect('Notification handle = 0x002e value: ', timeout=4)
                self.child.expect('\r\n', timeout=2)
                data = bytes.decode(self.child.before).split(' ')

                # First two Bytes from the Gatttool
                # to calculate scale, measure and decimal point
                scale, measure, decimal = self.input_data_1(data[0] + data[1])
                # Second two Bytes from the Gatttool to function
                function = self.input_data_2(data[2] + data[3])
                # Third two Bytes from the Gatttool to value
                value = self.input_data_3(data[4] + data[5], decimal)

                system('clear')
                print(f'{function} \n {value} {scale} {measure} \n \n Use "Ctrl + c"  to stop')

            except KeyboardInterrupt:
                exit()

    @staticmethod
    def hex_to_bin(hex_data):
        """
        This function convert hexadecimal values to binary values.
        :param hex_data: Hexadecimal values
        :return: binary values
        """

        # hex to uint16
        int_data = int.from_bytes(unhexlify(hex_data), byteorder=byteorder)
        # uint16 to bin
        bin_data = bin(int(int_data))[2:]

        return bin_data

    @staticmethod
    def transfer_measure(measure_number):
        """
        This function look for measure string.
        :param measure_number: Integer values from in the Range from 0 to 12.
        :return: measure string
        """

        if not isinstance(measure_number, int):
            raise TypeError('The parameter must be an integer.')
        if not 0 <= measure_number <= 12:
            raise ValueError('The number must be between zero and twelve.')

        measure = {
            0: 'Vdc',
            1: 'Vac',
            2: 'Adc',
            3: 'Aac',
            4: 'Ohms',
            5: 'F',
            6: 'Hz',
            7: '%%',
            8: '°C',
            9: '°F',
            10: 'V',
            11: 'Ohms',
            12: 'hFE'
        }

        return measure.get(measure_number, 'Invalid Input for measure.')

    @staticmethod
    def transfer_scale(scale_number):
        """
        This function look for scale string.

        :param scale_number: Integer values from in the Range from 1,2,3,5 and 6.
        :return: scale string
        """

        if not isinstance(scale_number, int):
            raise TypeError('The parameter must be an integer.')

        scale = {
            1: 'n',
            2: 'u',
            3: 'm',
            5: 'k',
            6: 'M'
        }

        return scale.get(scale_number, ' ')

    @staticmethod
    def transfer_function(function_number):
        """
        This function look for function string.

        :param function_number: Integer values from in the Range
        from 1,2,4,8,16 and 32.
        :return: function string
        """

        if not isinstance(function_number, int):
            raise TypeError('The parameter must be an integer.')

        function = {
            1: 'Hold',
            2: 'Δ',
            4: 'Auto',
            8: 'Low Battery',
            16: 'min',
            32: 'max'
        }

        return function.get(function_number, ' ')

    def input_data_1(self, hex_data):
        """
        This function create the scale, measure and decimal point
        of the multimeter from the first two bytes.

        :param hex_data: the first two bytes of the BT input
        :return: scale, measure and position of the decimal point
        """

        bin_data = self.hex_to_bin(hex_data)

        # select the right position of the numbers
        measure_number = int(str(bin_data[6]) +
                             str(bin_data[7]) +
                             str(bin_data[8]) +
                             str(bin_data[9]), 2)

        scale_number = int(str(bin_data[10]) +
                           str(bin_data[11]) +
                           str(bin_data[12]), 2)

        decimal = int(str(bin_data[13]) +
                      str(bin_data[14]) +
                      str(bin_data[15]), 2)

        scale = self.transfer_scale(scale_number)
        measure = self.transfer_measure(measure_number)

        return scale, measure, decimal

    def input_data_2(self, hex_data):
        """
        This function create the function
        of the multimeter from the second two bytes.

        :param hex_data: the second two bytes of the BT input
        :return: function of the multimeter
        """

        bin_data = self.hex_to_bin(hex_data)
        function_number = int(str(bin_data), 2)

        function = self.transfer_function(function_number)

        return function

    def input_data_3(self, hex_data, decimal):
        """
        This function create the value
        of the multimeter from the third two bytes
        and the decimal point position.

        :param hex_data: the third two bytes of the BT input
        :param decimal: the decimal point position
        :return: value of the multimeter represented as string
        """

        bin_data = self.hex_to_bin(hex_data)
        value = int(str(bin_data), 2)

        # Signed number representations for negative numbers
        # sign int16 von (-32768 to 32767)
        # (2 ** 16) /2 -1 = 32767.0
        if value > 32767:
            value = -1 * (value & 32767)

        # decimal point notation
        value = value / 10 ** decimal

        return str(value)


def main():
    parser = ArgumentParser()
    parser.add_argument('-m', '--mac', dest='mac_address', help='New MAC address')
    options = parser.parse_args()

    if not options.mac_address:
        parser.error('[-] Please specify a new mac address, use --help for more information')

    B35T(options.mac_address)


if __name__ == "__main__":
    main()
