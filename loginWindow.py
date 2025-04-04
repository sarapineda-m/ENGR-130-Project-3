from graphics import *
'''
import tkinter as tk
import tkinter as tk
from tkintermapview import TkinterMapView
'''
def main():
    temp_root = GraphWin("Temp", 100, 100)
    screen_width = temp_root.winfo_screenwidth()
    screen_height = temp_root.winfo_screenheight()
    temp_root.close()

    win = GraphWin("BoilerPark", screen_width, screen_height)
    win.setCoords(0, 0, screen_width, screen_height)  # Optional: set coordinate system
    win.setBackground("#cfb991")
    # Simulated text box 1
    box1 = Rectangle(Point(screen_width/2 - 100, screen_height/2 + 40),
                  Point(screen_width/2 + 100, screen_height/2 + 80))
    box1.setFill("white")
    box1.draw(win)
    label1 = Text(box1.getCenter(), "Text Box 1")
    label1.setSize(10)
    label1.draw(win)

     # Simulated text box 2
    box2 = Rectangle(Point(screen_width/2 - 100, screen_height/2 - 40),
                  Point(screen_width/2 + 100, screen_height/2))
    box2.setFill("white")
    box2.draw(win)
    label2 = Text(box2.getCenter(), "Text Box 2")
    label2.setSize(10)
    label2.draw(win)

    win.getMouse()
    win.close()
    '''
    # Create the main window
    root = tk.Tk()
    root.title("Embedded Google Map")
    root.geometry("800x600")

    # Create a frame for the map
    map_frame = tk.Frame(root, width=800, height=600)
    map_frame.pack(fill="both", expand=True)

    # Initialize the map widget
    map_widget = TkinterMapView(map_frame, width=800, height=600, corner_radius=0)
    map_widget.pack(fill="both", expand=True)

    # Set the tile server to Google Maps
    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    # Set the default location (e.g., New York City)
    map_widget.set_address("New York City, USA", marker=True)

    # Start the Tkinter main loop
    root.mainloop()
    '''

if __name__ == "__main__":
    main()