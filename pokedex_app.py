import tkinter as tk
from PIL import Image, ImageTk
from get_poke_info import Pokedex
from voice_to_text import voice_command
import time

class ToolTip:
    '''
    Tooltip class found online
    '''
    def __init__(self, button, text='widget info'):
        self.button = button
        self.text = text
        self.button.bind("<Enter>", self.enter)
        self.button.bind("<Leave>", self.close)

    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.button.bbox("insert")
        x += self.button.winfo_rootx() + 25
        y += self.button.winfo_rooty() + 20
        self.tooltip = tk.Toplevel(self.button)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tooltip, text=self.text, justify='left',
                       background='yellow', relief='solid', borderwidth=1,
                       font=("times", "8", "normal"))
        label.pack(ipadx=1)

    def close(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()

def add_sprite(file_name, pokemon_icon_slot, bottom_frame):
    size = int(bottom_frame.winfo_height()*0.25)
    img = ImageTk.PhotoImage(Image.open('./poke_sprites/'+ file_name).resize((size, size)))
    pokemon_icon_slot.delete("all")
    pokemon_icon_slot.create_image(0,0, anchor='nw', image=img)
    pokemon_icon_slot.image = img

def display_results(input_box, button, results, pokemon_icon_slot, bottom_frame, isAudio=False):
    #get id of pokemon by voice input
    if isAudio:
        button['state'] = 'disabled'
        poke_name, poke_description, dex_num = voice_command()
        #In case of error
        if poke_name is None:
            button['state']='normal'
            return
        input_box.delete(0,tk.END)
        input_box.insert(0, str(dex_num))
        time.sleep(1)
    else:
        dex_num = input_box.get().strip()
        poke_name, poke_description = Pokedex.get_poke_info(dex_num)
    results['text'] = 'Name: {}\nDescription: {}'.format(poke_name, poke_description)
    try:
        poke_icon = Pokedex.get_poke_sprite(poke_name.strip())
        add_sprite(poke_icon, pokemon_icon_slot, bottom_frame)
    except Exception as e:
        print('Exception Occured:' + str(e))
    finally:
        button['state']='normal'


def gui():
    #Create the root
    root = tk.Tk()
    root.title('Voice Dex')
    root.iconbitmap('C:/Users/Daniel/Documents/voice-encoder-gui/pokedex_icon.ico')

    #Define the canvas
    HEIGHT = 475
    WIDTH = 400
    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    background_image = ImageTk.PhotoImage(Image.open('./pokedex.png').resize((WIDTH, HEIGHT)))
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    canvas.pack()
    
    #Add the top frame and content
    frame = tk.Frame(root,  bg='#c20a19', bd=5)
    frame.place(relx=0.73, rely=0.1, relwidth=0.33, relheight=0.1, anchor='n')
    
    #Adding the input bar
    textbox = tk.Entry(frame, font=40)
    textbox.place(relwidth=0.45, relheight=1)

    #Adding the text-search button
    pokeball_icon = tk.PhotoImage(file = './pokeball.png')
    button = tk.Button(frame, text='Pokemon', image=pokeball_icon, font=40, command=lambda: display_results(textbox, button, results, pokemon_icon, bottom_frame))
    button.place(relx=0.47, relheight=1, relwidth=0.25)
    button_tooltip = ToolTip(button, "Search for a pokemon based on dex num")

    #Adding the audio-search button
    mic_icon = tk.PhotoImage(file='micicon.png')
    audio_button = tk.Button(frame, text='Speak', image=mic_icon, font=40, command=lambda: display_results(textbox, button, results, pokemon_icon, bottom_frame, True))
    audio_button.place(relx=0.74, relheight=1, relwidth=0.25)
    audio_button_tooltip = ToolTip(audio_button, "Say a number between 1 and 800")

    #Add the bottom frame and content
    bottom_frame = tk.Frame(root, bg='#c20a19', bd=10)
    bottom_frame.place(relx=0.55, rely=0.25, relwidth=0.7, relheight=0.6, anchor='n')

    #Display the results of the api call
    bg_color = 'white'
    results = tk.Label(bottom_frame, anchor='nw', wraplength=260, justify='left', bd=4)
    results.config(font=("Courier", 11), bg=bg_color)
    results.place(relwidth=1, relheight=1)

    #sprite icon goes here
    pokemon_icon = tk.Canvas(results, bg=bg_color, bd=0, highlightthickness=0)
    pokemon_icon.place(relx=.36, rely=.75, relwidth=1, relheight=0.5)

    root.resizable(False, False)
    root.mainloop()    

if __name__ == '__main__':
    gui()