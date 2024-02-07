# Protocol

Connect to the Device with: `gatttool -I <Mac Address>`

Following this operation, you'll receive 6 bytes of data. These bytes need to be split into 2-byte chunks for interpretation

## First 2 Bytes
The first 2 bytes represent the scale, measurement, and decimal point position.
To elaborate further: The initial two bytes you receive encode crucial information about the nature of the measurement.
The scale indicates the magnitude or unit of measurement, such as nano, micro, milli, kilo, or mega.


| Number | Value of scale |
| :----- | :------------: |
| 1      |    n (nano)    |
| 2      |   u (micro)    |
| 3      |   m (milli )   |
| 5      |    k (kilo)    |
| 6      |    M (mega)    |

## Second 2 Bytes 
The second two bytes represent the function of the multimeter.

| Number | Value of measure |
| :----- | :--------------: |
| 1      |       Vdc        |
| 2      |       Vac        |
| 3      |       Adc        |
| 4      |       Ohms       |
| 5      |        F         |
| 6      |        Hz        |
| 7      |        %%        |
| 8      |        °C        |
| 9      |        °F        |
| 10     |        V         |
| 11     |       Ohms       |
| 12     |       hFE        |

## Last 2 Bytes
The final two bytes represent additional information about the value displayed on the multimeter.

| Number | Value of function |
| :----- | :---------------: |
| 1      |       Hold        |
| 2      |         Δ         |
| 4      |       Auto        |
| 8      |    Low Battery    |
| 16     |        min        |
| 32     |        max        |

