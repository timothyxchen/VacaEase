# coding: utf-8

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import __init__ as init
import datetime as dt
import tkinter.messagebox

HEIGHT = 800
WIDTH = 1200


# this method will resize the background image to fit the screen
def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    background_label.config(image=photo)
    background_label.image = photo


# this method will create the table view structure
def table_builder():
    lower_frame = tk.Frame(root, bg='grey', bd=10)
    lower_frame.place(relx=0.5, rely=0.35, relwidth=0.75, relheight=0.6, anchor='n')
    tree = ttk.Treeview(lower_frame, columns=['1', '2', '3', '4', '5', '6', '7'], show='headings', height=25)
    tree.column('1', width=100)
    tree.column('2', width=250)
    tree.column('3', width=70)
    tree.column('4', width=70)
    tree.column('5', width=70)
    tree.column('6', width=120)
    tree.column('7', width=200)
    tree.heading('1', text='Category')
    tree.heading('2', text='Name')
    tree.heading('3', text='Rating')
    tree.heading('4', text='Popularity')
    tree.heading('5', text='Price')
    tree.heading('6', text='Phone')
    tree.heading('7', text='Traffic')

    df_to_table(tree)
    tree.grid()
    stat_button = ttk.Button(frame, text='Comparison', width=9, command=setup_comparison_window).place(relx=0.7,
                                                                                                       rely=0.8)


# this method will create a new window that displays route comparison
def setup_comparison_window():
    comparison_window = tk.Toplevel(height=300, width=1000)

    traffic_photo = Image.open('./img/traffic.png').resize((350, 300), Image.ANTIALIAS)
    rating_photo = Image.open('./img/rating.png').resize((350, 300), Image.ANTIALIAS)
    popularity_photo = Image.open('./img/popularity.png').resize((350, 300), Image.ANTIALIAS)
    traffic_img = ImageTk.PhotoImage(traffic_photo)
    rating_img = ImageTk.PhotoImage(rating_photo)
    popularity_img = ImageTk.PhotoImage(popularity_photo)
    traffic_label = tk.Label(comparison_window, image=traffic_img)
    traffic_label.place(relx=0.17, rely=0, relheight=1, relwidth=0.33, anchor='n')

    rating_label = tk.Label(comparison_window, image=rating_img)
    rating_label.place(relx=0.49, rely=0, relheight=1, relwidth=0.33, anchor='n')

    rating_label = tk.Label(comparison_window, image=popularity_img)
    rating_label.place(relx=0.82, rely=0, relheight=1, relwidth=0.33, anchor='n')
    comparison_window.mainloop()


# this method will organize three data frame to a table view
def df_to_table(tree):
    weather_in_date = get_weather()
    route_num = 1
    for index, route in routes.iterrows():
        tree.insert('', 'end', values=["", "###################"])
        tree.insert('', 'end', values=["", "#            Route {}            #".format(route_num)])
        tree.insert('', 'end', values=["", "###################"])
        day_num = 1
        for day in route:
            if weather_in_date is not None:
                try:
                    tree.insert('', 'end', values=["***Day {}***".format(day_num),
                                                   'Weather: {} {}'.format(
                                                       weather_in_date.iloc[day_num - 1].Description,
                                                       weather_in_date.iloc[day_num - 1].loc[
                                                           'High / Low'])])
                except:
                    tree.insert('', 'end', values=["***Day {}***".format(day_num)])
            else:
                tree.insert('', 'end', values=["***Day {}***".format(day_num)])
            for i in range(len(day)):
                if i == 0 or i == 5:
                    poi = ['Hotel'] + (list(day[i][[0, 2, 3, 4, 8]]))
                if i == 1 or i == 3:
                    poi = ['Attraction'] + (list(day[i][[0, 2, 3, 4, 8]]))
                if i == 2 or i == 4:
                    poi = ['Restaurant'] + (list(day[i][[0, 2, 3, 4, 8]]))
                distance_array = route_distance.loc[index].loc['day{}'.format(day_num)][i]
                distance_string = ', '.join(str(x) for x in distance_array)
                if distance_string != '0, 0':
                    poi.append(distance_string)
                tree.insert('', 'end', values=poi)
            day_num += 1
            tree.insert('', 'end', values=[""])
        route_num += 1
        tree.insert('', 'end', values=[""])


# this method will get needed weather data from the day trip starts
def get_weather():
    if weather_date in weather_output.index:
        print("Weather during the trip")
        print(weather_output.loc[weather_date:])
        return weather_output.loc[weather_date:]


# submit button that handles submission, it will also call validation method to validate input
def submit():
    global city, start_date, end_date, preference, weather_date
    global routes, route_distance, weather_output
    city = city_tkvar.get()
    start_date = start_date_entry.get()
    num_days = end_date_entry.get()
    preference = pref_tkver.get()
    if validator(city, start_date, num_days, preference):
        end_date = (dt.datetime.strptime(start_date, "%Y-%m-%d").date() + dt.timedelta(int(num_days))).strftime(
            '%Y-%m-%d')
        weather_date = dt.datetime.strptime(start_date, "%Y-%m-%d").date().strftime('%b %-d').upper()
        routes, route_distance, weather_output = init.init(city, start_date, end_date, preference)
        table_builder()


# a validator method to validate user input
def validator(city, start_date, num_days, preference):
    if city == 'Please select the city to visit':
        tk.messagebox.showerror('Error', 'Please select a destination.')
        return False
    if preference == 'Select your preference':
        tk.messagebox.showerror('Error', 'Please select a sorting preference.')
        return False
    if num_days == 'Please select number of days':
        tk.messagebox.showerror('Error', 'Please select number of days.')
        return False
    try:
        dt.datetime.strptime(start_date, "%Y-%m-%d").date()
    except:
        tk.messagebox.showerror('Error', 'Please enter valid date.')
        return False
    if dt.datetime.strptime(start_date, "%Y-%m-%d").date() < dt.date.today():
        tk.messagebox.showerror('Error', 'Please enter a date that is later than today')
        return False
    return True


# the following are all UI setups
root = tk.Tk()
root.title('VacaEase')
root.resizable(width=False, height=False)
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

image = Image.open('./img/background.JPG')
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)

background_label = tk.Label(canvas, image=photo, height=HEIGHT, width=WIDTH)
background_label.bind('<Configure>', resize_image)
background_label.image = photo
background_label.place(relwidth=1, relheight=1)
background_label.pack()

label_photo = Image.open('./img/V.png')
label_photo = label_photo.resize((360, 130), Image.ANTIALIAS)
label_img = ImageTk.PhotoImage(label_photo)
label_0 = tk.Label(root, image=label_img, font=("bold", 30))
label_0.place(relx=0.5, rely=0, relheight=0.15, relwidth=0.3, anchor='n')

frame = tk.Frame(root, bg='grey', bd=5)
frame.place(relx=0.5, rely=0.15, relwidth=0.75, relheight=0.2, anchor='n')

city_list = {'Boston', 'Los angeles', 'New York', 'Pittsburgh', 'Seattle'}
city_tkvar = tk.StringVar()
city_label = tk.Label(frame, text="City", width=6, font=("bold", 20), bg='grey')
city_label.place(relx=0.13, rely=0.05)
city_popupMenu = ttk.OptionMenu(frame, city_tkvar, "Select the city to visit", *city_list)
city_popupMenu.config(width=30)
city_popupMenu.place(relx=0.3, rely=0.05)

start_date = tk.Label(frame, text="Start Date", font=("bold", 20), bg='grey')
start_date.place(relx=0.15, rely=0.3)
start_date_entry = ttk.Entry(frame, font=20)
start_date_entry.config(width=30)
start_date_entry.place(relx=0.3, rely=0.30)
start_date_warning = tk.Label(frame, text="(yyyy-mm-dd) ex. 2019-02-21", font=("bold", 10), bg='grey')
start_date_warning.place(relx=0.63, rely=0.35)

end_date = tk.Label(frame, text="Days", font=("bold", 20), bg='grey')
end_date.place(relx=0.15, rely=0.55)
Length = [1, 2, 3, 4, 5]
end_date_entry = tk.StringVar()
Length_list = ttk.OptionMenu(frame, end_date_entry, "Select number of days", *Length)
Length_list.config(width=30)
Length_list.place(relx=0.3, rely=0.55)

preference = tk.Label(frame, text="Preference", font=("bold", 20), bg='grey')
preference.place(relx=0.15, rely=0.8)
preference_list = ['ratings', 'popularity', 'cost'];
pref_tkver = tk.StringVar()
preference_list_popupMenu = ttk.OptionMenu(frame, pref_tkver, "Select your preference", *preference_list)
preference_list_popupMenu.config(width=30)
preference_list_popupMenu.place(relx=0.3, rely=0.8)

button = ttk.Button(frame, text='Submit', width=10, command=submit).place(relx=0.85, rely=0.8)

root.mainloop()
