# Hadley Blalock
# PLTW Create Task: Moon Phases
# vFinal: 11/18/2026

#-----IMPORTS-----
import turtle as turt
import pandas as pd
import csv
from moon import Moon

#-----GLOBAL CONSTANTS-----
# radius of moon
r = 150

# initializes csv header row
data = [
    ["Date", "Phase", "Illumination", "Age"]
]

#-----FUNCTIONS-----
#---Moons---
# new moon
def new_moon(t):
    t.circle(r)

# full moon
def full_moon(t):
    t.begin_fill()
    t.circle(r)
    t.end_fill()

# crescents 
def waxing_crescent(t, illumination):
    t.begin_fill()
    t.circle(r)
    t.end_fill()
    t.penup()
    t.goto(-illumination*2, t.ycor())
    t.color("black")
    t.pendown()
    t.begin_fill()
    t.circle(r)
    t.end_fill()

def waning_crescent(t, illumination):
    t.begin_fill()
    t.circle(r)
    t.end_fill()
    t.penup()
    t.goto(illumination*2, t.ycor())
    t.color("black")
    t.pendown()
    t.begin_fill()
    t.circle(r)
    t.end_fill()
    
# quarters
def first_quarter(t):
    t.begin_fill()
    t.circle(r, 180)
    t.left(90)
    t.forward(2*r)
    t.end_fill()

def third_quarter(t):
    t.setheading(180)
    t.begin_fill()
    t.circle(-r, 180)
    t.left(90)
    t.backward(2*r)
    t.end_fill()

# gibbous
def waxing_gibbous(t, illumination):
    t.circle(r)
    t.begin_fill()
    t.circle(r, 180-(100-illumination)/2) # goes back up halfway the arc of the circle minus a section for the illumination
    t.penup()
    t.setheading(180)
    t.circle(r, 180-(100-illumination)/2) # draws a partial semi-circle ased on the illumination
    t.end_fill()

def waning_gibbous(t, illumination):
    t.circle(r)
    t.begin_fill()
    t.setheading(180)
    t.circle(-r, 180-(100-illumination)/2) # goes back up halfway the arc of the circle minus a section for the illumination
    t.penup()
    t.setheading(180)
    t.circle(r, -(180-(100-illumination)/2)) # draws a partial semi-circle ased on the illumination
    t.end_fill()

#---User Interface---
def draw_moon(phase, illumination, date):
    # screen set-up
    screen = turt.Screen()
    screen.clear()
    screen.bgcolor("black")
    
    # turtle set-up
    t = turt.Turtle()
    t.color("white")

    # write the moon phase before drawing
    t.penup()
    t.goto(0, 200)    
    t.pendown()
    t.write(f"Moon Phase on {date}", align="center", font=("Futura", 24, "bold"))
    t.penup()
    t.goto(0, 150) 
    t.pendown()
    t.write(f"{phase}", align="center", font=("Futura", 20))
    t.penup()
    t.goto(10, 125) 
    t.pendown()
    t.write(f"Illumination Percentage: {illumination}%", align="center", font=("Futura", 20))
    t.penup()
    t.goto(0, -200)
    t.pendown()

    # cleaning moon phase string for easier comparisons
    phase = phase.replace(" ", "").lower()

    # calls the moon function to draw based on the phase
    if phase == "newmoon":
        new_moon(t)
    elif phase == "fullmoon":
        full_moon(t)
    elif phase == "firstquarter":
        first_quarter(t)
    elif phase == "thirdquarter":
        third_quarter(t)
    elif phase == "waxingcrescent":
        waxing_crescent(t, illumination)
    elif phase == "waxinggibbous":
        waxing_gibbous(t, illumination)
    elif phase == "waningcrescent":
        waning_crescent(t, illumination)
    elif phase == "waninggibbous":
        waning_gibbous(t, illumination)
    else:
        print("Please enter a valid date.")
        main()

def get_date():
    # gets the date from the user (limited up to 2011)
    date = input("Please enter a date to see the moon from that night (MM/DD/YYYY): ")
    # splits date to reformat to fit moon object date
    month = date.split("/")[0]
    day = date.split("/")[1]
    year = date.split("/")[2]

    # returns the date in the format for the moon API
    return f"{year}-{month}-{day}"

def get_moon_phase():
    # initializes moon object
    m = Moon()
    # sets the date of the moon to user input date
    user_date = get_date()
    m.set_moon_phase(date=user_date, hour=12)

    # m.info is a dictionary
    # returns the phase percentage of the moon
    illumination = round(m.info["phase"])
    # age is the days since the new moon
    days_since_new_moon = round(m.info["age"])

    # uses the moon phase percentage and age to determine closest approximate phase
    # new moon ~= 0% and 0 days
    # quarter moons ~= 50%
    # crescent moons ~= 1%-49%
    # gibbous moons ~= 51%-100%
    # full moon ~= 100% and 15 days
        # the 15 day marked is used to determine waxing or waning
    if illumination < 2:
        moon_phase = "New Moon"
    elif (illumination > 2 and illumination < 46) and days_since_new_moon < 15:
        moon_phase = "Waxing Crescent"
    elif (illumination > 45 and illumination < 55) and days_since_new_moon < 15:
        moon_phase = "First Quarter"
    elif (illumination > 55 and illumination < 98) and days_since_new_moon < 15:
        moon_phase = "Waxing Gibbous"
    elif illumination > 98:
        moon_phase = "Full Moon"
    elif (illumination > 55 and illumination < 98) and days_since_new_moon > 15:
        moon_phase = "Waning Gibbous"
    elif (illumination > 45 and illumination < 55) and days_since_new_moon > 15:
        moon_phase = "Third Quarter"
    elif (illumination > 2 and illumination < 46) and days_since_new_moon > 15:
        moon_phase = "Waning Crescent"

    # adds the moon to the database
    data.append([user_date, moon_phase, illumination, days_since_new_moon])
    
    # draws the moon
    draw_moon(moon_phase, illumination, user_date)

def view_database():
    # writes data to csv
    with open("moon.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    # reads the moon csv
    df = pd.read_csv("moon.csv")
    # print the entire table formatted
    print(df.to_markdown(index=False, tablefmt="psql"))

def main():
    # runs the first part of the program
    get_moon_phase()

    # once at least one date has been entered the user can choose to view the database
    next = input("Would you like to enter another date or view the database?\n1. Enter New Date\n2. View Database\n")
    if next == "1":
        main()
    elif next == "2":
        view_database()
        main()
    else:
        print("Thank you goodbye!")

#-----Main-----
main()