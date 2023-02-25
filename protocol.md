# Protocol

Connect to the Device with: `gatttool -I <Mac Address>`

Then you get 6 Byte:

For reading you have to split in to 2 Byte of the Input.
The first 2 Byte present the scale, measure, decimal Point Position.

| Number | Value of scale |
| :----- | :------------: |
| 1      |    n (nano)    |
| 2      |   u (micro)    |
| 3      |   m (milli )   |
| 5      |    k (kilo)    |
| 6      |    M (mega)    |

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

The second two bytes represent the function. 

| Number | Value of function |
| :----- | :---------------: |
| 1      |       Hold        |
| 2      |         Δ         |
| 4      |       Auto        |
| 8      |    Low Battery    |
| 16     |        min        |
| 32     |        max        |

The last two bytes represent the value that can be seen on the multimeter. 