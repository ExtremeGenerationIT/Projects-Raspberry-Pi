"""
Developed by ExtremeGeneration.it (2018)
http://www.extremegeneration.it

Made available under GNU GENERAL PUBLIC LICENSE

# Subscribe to our Youtube Channel http://www.youtube.com/user/eXtremegenerationIT
# for many other tutorials
# Download the Raspberry Pi APP
# https://play.google.com/store/apps/details?id=it.extremegeneration.raspberrypiprogetti
"""

import driverLCD  # Custom library to use the LCD display with Raspberry Pi
import urllib.request
import json
import time

# Custom CryptoCurrency Symbols
bitcoin_symbol = [
    [0b01010,
     0b11110,
     0b01001,
     0b01001,
     0b01110,
     0b01001,
     0b11111,
     0b01010]]

ethereum_symbol = [
    [0b00100,
     0b01110,
     0b11111,
     0b11111,
     0b01110,
     0b11111,
     0b01110,
     0b00100]]

# Initialize LCD screen
LCDscreen = driverLCD.lcd()
# Set BackLight 1=activate, 0=deactivate
LCDscreen.backlight(1)


# Define Scroll Text Function
# Pass the text, the column and number of iterations
def scroll_text(text, iterations, column=2, row=1, speed=0.2):
    # create string with 16 empty spaces
    str_pad = " " * 16
    iterate = 0
    while (iterations > iterate):
        for i in range(0, len(text)):
            lcd_text = text[i:(i + 16)]
            LCDscreen.lcd_display_string(lcd_text, column, row)
            time.sleep(speed)
            LCDscreen.lcd_display_string(str_pad, column, row)
        iterate += 1


# Initialize, greeting message & brand
scroll_text('    Crypto Tracker - ExtremeGeneration.it', column=1, iterations=1, row=1)


def query_Api():
    # The cryptocompare API allows to compare several crypto-currencies
    data = urllib.request.urlopen(
        'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=ETH,IOT,BTC&tsyms=BTC,USD,EUR,ETH,IOT').read()
    dataJSON = json.loads(data.decode('utf-8'))
    return dataJSON


while True:
    # Query the API
    dataJSON = query_Api()

    # Function to compute the sign (+ or -) of the percentage variation
    sign = lambda x: '+' if x > 0 else ""

    #################### Show BITCOIN DATA ###########################
    # Get % daily
    BTC_open_euro = float(dataJSON['RAW']['BTC']['EUR']['OPEN24HOUR'])
    BTC_current_euro = float(dataJSON['RAW']['BTC']['EUR']['PRICE'])
    BTC_var_percentage = ((BTC_current_euro - BTC_open_euro) / BTC_open_euro) * 100
    # Get ETH/BTC price
    ETH_BTC = float(dataJSON['RAW']['BTC']['ETH']['PRICE'])
    # Get IOTA/BTC price
    IOTA_BTC = float(dataJSON['RAW']['BTC']['IOT']['PRICE'])
    # Display Bitcoin symbol
    LCDscreen.lcd_load_custom_chars(bitcoin_symbol)
    LCDscreen.lcd_write(0X80)
    LCDscreen.lcd_write_char(0)
    # Show row 1
    LCDscreen.lcd_display_string('itcoin {}{:04.2f}%'.format(sign(BTC_var_percentage), BTC_var_percentage), 1, 1)
    # Create a String for the second column
    BTC_feed = ('   EUR {:04.2f}  ETH {:04.2f}  IOTA {:04.2f}'.format(BTC_current_euro, ETH_BTC, IOTA_BTC))
    # Show row 2 (scrolling)
    scroll_text(BTC_feed, speed=0.4, iterations=2, row=1)
    # Clean the LCD Display
    LCDscreen.lcd_clear()


    ########################## Show ETHEREUM DATA ########################
    # Get % daily
    ETH_open_euro = float(dataJSON['RAW']['ETH']['EUR']['OPEN24HOUR'])
    ETH_current_euro = float(dataJSON['RAW']['ETH']['EUR']['PRICE'])
    ETH_var_percentage = ((ETH_current_euro - ETH_open_euro) / ETH_open_euro) * 100
    # Get BTC/ETH price
    BTC_ETH = float(dataJSON['RAW']['ETH']['BTC']['PRICE'])
    # Get IOTA/ETH price
    IOTA_ETH = float(dataJSON['RAW']['ETH']['IOT']['PRICE'])
    # Display Ethereum symbol
    LCDscreen.lcd_load_custom_chars(ethereum_symbol)
    LCDscreen.lcd_write(0X80)
    LCDscreen.lcd_write_char(0)  # Set row
    # Show row 1
    LCDscreen.lcd_display_string('thereum {}{:04.2f}%'.format(sign(ETH_var_percentage), ETH_var_percentage), 1, 1)
    # Create a String for the second column
    ETH_feed = ('   EUR {:04.2f}  BTC {:04.2f}  IOTA {:04.2f}'.format(ETH_current_euro, BTC_ETH, IOTA_ETH))
    # Show row 2 (scrolling)
    scroll_text(ETH_feed, speed=0.4, iterations=2, row=1)
    # Clean the LCD Display
    LCDscreen.lcd_clear()


    ##########################SHow IOTA DATA###########################
    # Get % daily
    IOTA_open_euro = float(dataJSON['RAW']['IOT']['EUR']['OPEN24HOUR'])
    IOTA_current_euro = float(dataJSON['RAW']['IOT']['EUR']['PRICE'])
    IOTA_var_percentage = ((IOTA_current_euro - IOTA_open_euro) / IOTA_open_euro) * 100
    # Get BTC/IOTA price
    BTC_IOTA = float(dataJSON['RAW']['IOT']['BTC']['PRICE'])
    # Get ETH/IOTA price
    ETH_IOTA = float(dataJSON['RAW']['IOT']['ETH']['PRICE'])
    # Show row 1
    LCDscreen.lcd_display_string('IOTA {}{:04.2f}%'.format(sign(IOTA_var_percentage), IOTA_var_percentage), 1, 1)
    # Create a String for the second column
    IOTA_feed = ('   EUR {:04.2f}  BTC {:04.6f}  ETH {:04.6f}'.format(IOTA_current_euro, BTC_IOTA, ETH_IOTA))
    # Show row 2 (scrolling)
    scroll_text(IOTA_feed, speed=0.4, iterations=2, row=1)
    # Clean the LCD Display
    LCDscreen.lcd_clear()
