# LCD I2C
## Use an I2C LCD with Python

Basic library for interacting with I2C LCD screens. It started off as a Python port of the Arduino [LiquidCristal_I2C](https://github.com/johnrickman/LiquidCrystal_I2C/) library and ended up implementing an object oriented API, for easier use.

Tested using a Raspberry Pi Zero 2W.

## Examples

### Connect to LCD screen and print some text:

```python
from lcd_i2c import LCD_I2C

lcd = LCD_I2C(39, 16, 2)

# Turn on the backlight
lcd.backlight.on()

# Show the blinking cursor
lcd.blink.on()
# or:
# lcd.cursor.blink.on()

# Print some text
lcd.write_text('Hola!')
```
