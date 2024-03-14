import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Load CSV data for openings and player Elos
opening_data = pd.read_csv('RankedOpenings.csv')
black_elo_data = pd.read_csv('BlackElo.csv')
white_elo_data = pd.read_csv('WhiteElo.csv')


# Player names combining both datasets
player_names = sorted(set(black_elo_data['Black'].unique()) | set(white_elo_data['White'].unique()))

# Function definitions for plotting...
def plot_win_rate(opening_name, data):
    fig, ax = plt.subplots()
    opening_data = data[data['Opening'] == opening_name]
    win_rate = opening_data['SuccessRate'].iloc[0]
    ax.bar(opening_name, win_rate)
    ax.set_ylabel('Win Rate')
    ax.set_ylim(0, 1)
    return fig

def plot_average_rating(opening_name, data):
    fig, ax = plt.subplots()
    opening_data = data[data['Opening'] == opening_name]
    white_elo = opening_data['AverageWhiteElo'].iloc[0]
    black_elo = opening_data['AverageBlackElo'].iloc[0]
    ax.bar(['Average White Elo', 'Average Black Elo'], [white_elo, black_elo])
    return fig

def plot_elo_progress(player_name, color):
    fig, ax = plt.subplots()
    if color == 'Black':
        player_data = black_elo_data[black_elo_data['Black'] == player_name]
        ax.plot(player_data['Elo'], marker='o', label='Black Elo')
    else:
        player_data = white_elo_data[white_elo_data['White'] == player_name]
        ax.plot(player_data['Elo'], marker='o', label='White Elo')
    ax.set_title(f'Elo Progression for {player_name}')
    ax.set_xlabel('Game Number')
    ax.set_ylabel('Elo Rating')
    ax.legend()
    return fig

# Function to switch between analysis GUIs
def switch_analysis_gui(event):
    # Clear widgets and canvas
    for widget in window.winfo_children():
        if widget != analysis_type_combobox:  # Keep the analysis type dropdown
            widget.destroy()
    if canvas:
        canvas.get_tk_widget().pack_forget()

    # Define analysis type specific functions
    def on_opening_analysis_selected(event):
        opening_name = opening_combobox.get()
        selected_analysis = analysis_combobox.get()
        analysis_functions = {
            "Win Rate per Opening": plot_win_rate,
            "Average Rating per Opening": plot_average_rating
        }
        fig = analysis_functions[selected_analysis](opening_name, opening_data)
        show_figure(fig)

    def on_player_selected(event):
        player_name = player_name_combobox.get()
        color = color_combobox.get()
        fig = plot_elo_progress(player_name, color)
        show_figure(fig)

    # Show respective analysis based on selection
    selected_analysis_type = analysis_type_combobox.get()
    if selected_analysis_type == 'Openings Explorer':
        # Dropdown menu for selecting opening
        ttk.Label(window, text="Select an opening:").pack(pady=5)
        opening_combobox = ttk.Combobox(window, values=sorted(opening_data['Opening'].unique()), width=50)
        opening_combobox.pack(pady=5)
        opening_combobox.current(0)

        # Dropdown menu for analyses
        ttk.Label(window, text="Select analysis:").pack(pady=5)
        analysis_combobox = ttk.Combobox(window, values=['Win Rate per Opening', 'Average Rating per Opening'], width=50)
        analysis_combobox.pack(pady=5)
        analysis_combobox.current(0)
        analysis_combobox.bind('<<ComboboxSelected>>', on_opening_analysis_selected)

    elif selected_analysis_type == 'Player Elo Progression':
        # Dropdown menu for selecting player name
        ttk.Label(window, text="Select a player:").pack(pady=5)
        player_name_combobox = ttk.Combobox(window, values=player_names, width=50)
        player_name_combobox.pack(pady=5)
        player_name_combobox.current(0)

        # Dropdown menu for selecting color
        ttk.Label(window, text="Select color:").pack(pady=5)
        color_combobox = ttk.Combobox(window, values=['Black', 'White'], width=50)
        color_combobox.pack(pady=5)
        color_combobox.current(0)
        color_combobox.bind('<<ComboboxSelected>>', on_player_selected)


# Function to show matplotlib figure in Tkinter window
def show_figure(fig):
    global canvas
    if canvas:
        canvas.get_tk_widget().pack_forget()  # Clear previous plot
    canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Main window setup
window = tk.Tk()
window.title("Chess Analysis Dashboard")

# Dropdown menu for selecting analysis type
analysis_type_combobox = ttk.Combobox(window, values=['Openings Explorer', 'Player Elo Progression'], width=50)
analysis_type_combobox.pack(pady=20)
analysis_type_combobox.current(0)

# Placeholder for plot canvas
canvas = None

# Initial load the default (first) analysis GUI
switch_analysis_gui(None)

# Bind the analysis change function to the combobox
analysis_type_combobox.bind('<<ComboboxSelected>>', switch_analysis_gui)

# Begin the Tkinter event loop
window.mainloop()