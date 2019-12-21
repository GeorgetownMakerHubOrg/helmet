# Helmet code
# Pascal Girard
from time import sleep
import random
import board
import neopixel
from touchio import TouchIn
from random import randint
from time import sleep

# Configure the setup
PIXEL_PIN = board.D1   # pin that the NeoPixel is connected to
ORDER = neopixel.RGB   # pixel color channel order
PIXELS = 47
SPARKS = 3
RED = (0,255,0)
BLUE = (0,0,255)
GREEN = (255,0,0)
PURPLE = (0,0x80,0x80)
CLEAR = (0, 0, 0)      # clear (or second color)
DELAY = 0.25           # blink rate in seconds
SPEED = 10/1000
OFFSET = 12

# Create the NeoPixel object
pixel = neopixel.NeoPixel(PIXEL_PIN, 47, pixel_order=ORDER)

# Capacitive touch on A2
touch2 = TouchIn(board.A2)

def randomcolor():
  return (wheel(random.randint(1,255)))

def cops(pixel, first, second):
  print('in cops')
  for i in range(5):
    for block in 7,8,9,30,31,32:  # 3 pixel blocks on front & back
      pixel[color] = first
    for block in 14,15,16,37,38,39: # 3 pixel blocks on front & back
      pixel[color] = second
    pixel.write()
    sleep(1/1000)
    clearpixels(pixel)
  sleep(1/10)

def clearpixels(pixel) :
  for i in range(PIXELS):
    pixel[i] = (CLEAR)
    pixel.write()

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def sparks(colors):
  for i in range(SPARKS) :
    current_pixel = randint(0,PIXELS-1)
    speed = randint(1,10) # in milliseconds
    slot = randint(0,SPARKS-1)
    #print ('turn off pixel: ', colors[slot], 'slot is', slot)
    pixel[colors[slot]] = (CLEAR)
    colors[slot] = current_pixel
    pixel[current_pixel] = randomcolor()
    #print ('turn on pixel: ', current_pixel)
    pixel.write()
    sleep(speed/1000)

def knightrider(speed):
  # rainbows!
  port = randomcolor()
  starboard = randomcolor()
  """# halloween!
  port = wheel(9)
  starboard = wheel(80)
  starboard = wheel(225)"""
  for i in range(PIXELS):
    pixel[(i+OFFSET)%47] = (port)
    pixel[(i-1+OFFSET)%47] = (CLEAR)
    pixel[(OFFSET-i)%47] = (starboard)
    pixel[(OFFSET-i+1)%47] = (CLEAR)
    pixel.write()
    sleep(speed)

def colorscale(hexstr, scalefactor):
    def clamp(val, minimum=0, maximum=255):
      if val < minimum:
        return minimum
      if val > maximum:
        return maximum
      return int(val)
    hexstr = hexstr.strip('#')
    if scalefactor < 0 or len(hexstr) != 6:
        return hexstr
    r, g, b = int(hexstr[:2], 16), int(hexstr[2:4], 16), int(hexstr[4:], 16)
    r = clamp(r * scalefactor)
    g = clamp(g * scalefactor)
    b = clamp(b * scalefactor)
    # return "#%02x%02x%02x" % (r, g, b)
    return (r, g, b)

# Loop forever and blink the color
speed = SPEED
touch = 0
colors = {}
clearpixels(pixel)

for i in range(SPARKS) :   # set up a list of sparks we want to light.
  pair = {i : randint(0,PIXELS-1)}
  colors.update(pair)

"""for i in range(255):
  print ("I is:", i)
  pixel[0] = wheel(i)
  pixel[1] = wheel(i)
  pixel[2] = wheel(i)
  pixel.write()
  sleep(1/2)"""
while True:
  # use A2 as capacitive touch to turn on internal LED
  if touch2.value:
    print("A2 touched!")
    touch += 1
    speed = speed/5
  if touch % 2 == 0:
    sparks(colors)
  else:
    knightrider(speed)
while True:
  cops(pixel, RED, BLUE)
  cops(pixel, BLUE, RED)
  

