import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load CSV data
dfop = pd.read_csv('test.csv')  # ECO data
dftc = pd.read_csv('test2.csv')  # Time Control data
dfad = pd.read_csv('test3.csv')  # Time Control Advantage data

# Create the main TKinter window
window = tk.Tk()
window.title("Chess Analysis Tool")

# Define global variable for the Matplotlib figure canvas
canvas = None


# Analysis function for ECO Win Rate
def analyse_eco_win_rate(player, eco):
    global canvas
    data = dfop[(dfop['Player'].str.lower() == player.lower()) & (dfop['ECO'].str.lower() == eco.lower())]
    if not data.empty:
        win_rate = data['TotalWinRate'].iloc[0]
        loss_rate = 1 - win_rate
        fig, ax = plt.subplots()
        ax.pie([win_rate, loss_rate], labels=['Win', 'Loss or Draw'], autopct='%1.1f%%', startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.
        ax.set_title(f"Win Rate for {player} [ECO: {eco}]")

        # If a canvas already exists, clear and update it; otherwise, create a new one
        if canvas:
            canvas.get_tk_widget().destroy()
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()
    else:
        print("No data found.")


# Analysis function for Time Control Win Rate
# Analysis function for Time Control Win Rate
def analyse_time_control_win_rate(player, time_control):
    global canvas
    data = dftc[
        (dftc['Player'].str.lower() == player.lower()) & (dftc['TimeControl'].str.lower() == time_control.lower())]
    if not data.empty:
        win_rate = data['TotalWinRate'].iloc[0]
        loss_rate = 1 - win_rate
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie([win_rate, loss_rate], labels=['Win', 'Loss or Draw'], autopct='%1.1f%%', startangle=140)
        ax.axis('equal')
        ax.set_title(f"Win Rate for {player} (Time Control: {time_control})")

        if canvas:
            canvas.get_tk_widget().destroy()
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()
    else:
        print("No data found.")


# Analysis function for Time Control Advantage
def display_time_control_advantage(time_control):
    global canvas
    data = dfad[dfad['TimeControl'].str.lower() == time_control.lower()]
    fig, ax = plt.subplots(figsize=(6, 6))
    if not data.empty:
        advantage = data['Advantage'].iloc[0]
        ax.text(0.5, 0.5, f"Advantage: {advantage}", ha='center', va='center')
        ax.set_title(f"Advantage (Time Control: {time_control})")
        ax.axis('off')  # Hide the axes

        if canvas:
            canvas.get_tk_widget().destroy()
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()
    else:
        print("No data found.")


# Handler when the analysis type is changed in the dropdown
def on_analysis_change(event):
    selected_analysis = analysis_type_var.get()

    # Hide all frames and only show the one relevant to the selected analysis
    eco_frame.pack_forget()
    time_control_frame.pack_forget()
    advantage_frame.pack_forget()

    if selected_analysis == "ECO Win Rate":
        eco_frame.pack()
    elif selected_analysis == "Time Control Win Rate":
        time_control_frame.pack()
    elif selected_analysis == "Time Control Advantage":
        advantage_frame.pack()


# Create a dropdown to select the type of analysis
analysis_types = ['ECO Win Rate', 'Time Control Win Rate', 'Time Control Advantage']
analysis_type_var = tk.StringVar()
analysis_dropdown = ttk.Combobox(window, textvariable=analysis_type_var, values=analysis_types, state='readonly')
analysis_dropdown.pack(pady=5)
analysis_dropdown.bind('<<ComboboxSelected>>', on_analysis_change)
analysis_type_var.set(analysis_types[0])  # Set default value

# Frame for ECO Win Rate analysis options
eco_frame = tk.Frame(window)
player_eco_label = tk.Label(eco_frame, text="Player Name:")
player_eco_label.pack(side='left')
player_eco_dropdown = ttk.Combobox(eco_frame, values=list(dfop['Player'].unique()))
player_eco_dropdown.pack(side='left', padx=5)
eco_code_label = tk.Label(eco_frame, text="ECO Code:")
eco_code_label.pack(side='left')
eco_code_dropdown = ttk.Combobox(eco_frame, values=list(dfop['ECO'].unique()))
eco_code_dropdown.pack(side='left', padx=5)
eco_analyse_button = ttk.Button(eco_frame, text="Analyse",
                                command=lambda: analyse_eco_win_rate(player_eco_dropdown.get(),
                                                                     eco_code_dropdown.get()))
eco_analyse_button.pack(side='left')

# Frame for Time Control Win Rate analysis options
time_control_frame = tk.Frame(window)
player_tc_label = tk.Label(time_control_frame, text="Player Name:")
player_tc_label.pack(side='left')
player_tc_dropdown = ttk.Combobox(time_control_frame, values=list(dftc['Player']), width=15)
player_tc_dropdown.pack(side='left', padx=5)
tc_label = tk.Label(time_control_frame, text="Time Control:")
tc_label.pack(side='left')
tc_dropdown = ttk.Combobox(time_control_frame, values=list(dftc['TimeControl']), width=15)
tc_dropdown.pack(side='left', padx=5)
tc_analyse_button = ttk.Button(time_control_frame, text="Analyse", command=lambda: analyse_time_control_win_rate(player_tc_dropdown.get(), tc_dropdown.get()))
tc_analyse_button.pack(side='left')

# Frame for Time Control Advantage analysis options
advantage_frame = tk.Frame(window)
tc_advantage_label = tk.Label(advantage_frame, text="Time Control:")
tc_advantage_label.pack(side='left')
tc_advantage_dropdown = ttk.Combobox(advantage_frame, values=list(dfad['TimeControl']), width=15)
tc_advantage_dropdown.pack(side='left', padx=5)
advantage_button = ttk.Button(advantage_frame, text="Show Advantage", command=lambda: display_time_control_advantage(tc_advantage_dropdown.get()))
advantage_button.pack(side='left')

# Show canvas for plots
fig, ax = plt.subplots()  # Initial empty plot
canvas = FigureCanvasTkAgg(fig, master=window)  # Create and pack a canvas with the figure
canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

window.mainloop()  # Start the main loop of the application