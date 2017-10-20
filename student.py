import pigo
import time  # import just in case students need
import random

# setup logs
import logging
LOG_LEVEL = logging.INFO
LOG_FILE = "/home/pi/PnR-Final/log_robot.log"  # don't forget to make this file!
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)


class Piggy(pigo.Pigo):
    """Student project, inherits teacher Pigo class which wraps all RPi specific functions"""

    def __init__(self):
        """The robot's constructor: sets variables and runs menu loop"""
        print("I have been instantiated!")
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 77
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.SAFE_STOP_DIST = 30
        self.HARD_STOP_DIST = 15
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 90
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 110
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.menu()

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "o": ("Obstacle count", self.obstacle_count),
                "d": ("Dance", self.dance),
                "c": ("Calibrate", self.calibrate),
                "s": ("Check status", self.status),
                "q": ("Quit", quit_now)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    def obstacle_count(self):
        """scans and estimates the number of obstacles within sight"""
        self.wide_scan()
        found_something = False
        counter = 0
        for distance in self.scan:
            if distance and distance < 60 and not found_something:
                found_something = True
                counter += 2
                print("Object # %d found, I think" % counter)
                if distance and distance > 60 and found_something:
                    found_something = False
        print("\n----I SEE %d OBJECTS----\n" % counter)


    # YOU DECIDE: How does your GoPiggy dance?
    def dance(self):
        """executes a series of methods that add up to a compound dance"""
        print("\n---- LET'S DANCE ----\n")
        ##### WRITE YOUR FIRST PROJECT HERE

        if self.safety_check():
            self.to_the_right()
            self.to_the_left()
            self.now_dab()
            self.now_spin()
            self.now_walk_it_by_yourself()

    def safety_check(self):
        self.servo(self.MIDPOINT)  # look straight ahead
        for loop in range(4):
            if not self.is_clear():
                print("NOT GOING TO DANCE!")
                return False
            self.encR(8)
            print("Check #%d" % (loop + 1))
        print("Safe to dance!")
        return True

                # Loop 3 times
                # Turn 60 deg
                # scan again

    def to_the_right(self):
        """subroutine of dance method"""
        for x in range(3):
            self.servo(160)
            self.encR(20)
            self.encF(5)

    def to_the_left(self):
        """subroutine of dance method"""
        for x in range(3):
            self.encR(10)
            self.encF(5)

    def now_dab(self):
        """subroutine of dance method"""
        for x in range(3):
            self.encR(10)
            self.encF(5)

    def now_spin(self):
        """subroutine of dance speed"""
        for x in range (3):
            self.encR(10)
            self.encF(5)
            self.servo(90, 60, -90)

    def now_walk_it_by_yourself(self):
        for x in range(3):
            self.encR(10)
            self.encF(5)

    def nav(self):
        """auto pilots and attempts to maintain original heading"""
        logging.debug("Starting the nav method")
        print("---------! NAVIGATION ACTIVATED !----------\n")
        print("------ [ Press CTRL + C to stop me ] ------\n")
        print("---------! NAVIGATION ACTIVATED !----------\n")
        while True:
            if self.is_clear():
                self.cruise()
            else:
                self.encR(10)

    def cruise (self):
        """drive straight while path is clear"""
        self.fwd()
        while self.dist() > self.SAFE_STOP_DIST:
            time.sleep(.5)
        self.stop()

    def safe_turn (self):
        """rotate until path is clear"""
        self.servo()
        self.right_rot()
        while self.dist() > self.SAFE_STOP_DIST:
         self.stop()
####################################################
############### STATIC FUNCTIONS

def error():
    logging.error("ERROR")
    print('ERROR')


def quit_now():
    """shuts down app"""
    raise SystemExit

##################################################################
######## The app starts right here when we instantiate our GoPiggy


try:
    g = Piggy()
except (KeyboardInterrupt, SystemExit):
    pigo.stop_now()
except Exception as ee:
    logging.error(ee.__str__())