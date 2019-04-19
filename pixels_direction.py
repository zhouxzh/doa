import time
from pixels import Pixels, pixels
from fire_led_pattern import FireLedPattern

if __name__ == '__main__':

    pixels.pattern = FireLedPattern(show=pixels.show)

    for direction in range(360):
        pixels.wakeup(direction)
        time.sleep(0.1)

    while True:

        try:
            pixels.wakeup()
            time.sleep(3)
            pixels.think()
            time.sleep(3)
            pixels.speak()
            time.sleep(6)
            pixels.off()
            time.sleep(3)
        except KeyboardInterrupt:
            break


    pixels.off()
