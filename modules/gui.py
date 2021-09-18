from tkinter import *
from tkinter import ttk
from tkinter import font as tkFont
from PIL import Image, ImageTk
import time, string
from random import choice, random, randint, shuffle

class Mafia:
    """Class for the GUI of Mafia in Python"""
    def __init__(self, window):
        # Creating Canvas objects
        self.window = window
        self.canvas_frame = Frame(self.window, bg="#9c9c9c")
        self.canvas_frame.grid(row=0, column=0, rowspan=2)
        self.c = Canvas(self.canvas_frame, width=800, height=550, bg="#212121", highlightthickness=0)
        self.c.pack(padx=10, pady=10)
        self.c.create_line(40, 60, 760, 60, fill="white", width=2)
        self.round_no = 1
        self.round_status = self.c.create_text(40, 8, text=f"Round {self.round_no}", anchor=NW, fill="white", font="Arial 30")
        self.event_status = self.c.create_text(760, 8, anchor=NE, fill="white", font="Arial 30")
        
        # Creating Status Bar
        self.role_status = Label(self.window, text="\t\t\t\t   ", font="Arial 18", bg="#6cbb73", borderwidth=2, relief="raised")
        self.role_status.grid(row=0, column=1, sticky=N, padx=30, pady=5, ipadx=5)
        
        # Creating Chat Frame
        self.chat_frame = Frame(self.window, bg="#9c9c9c") 
        self.chat_frame.grid(row=1, column=1, sticky=N)
        
        self.img = PhotoImage(file="images/blank_profile.png")
        self.chat_image1 = Label(self.chat_frame, image=self.img, relief="raised", bg="#666666")
        self.chat_image1.grid(row=0, column=0)
        
        self.chat_image2 = Label(self.chat_frame, image=self.img, relief="raised", bg="#666666")
        self.chat_image2.grid(row=2, column=0)
        
        self.chat_image3 = Label(self.chat_frame, image=self.img, relief="raised", bg="#666666")
        self.chat_image3.grid(row=4, column=0)
        
        self.name_tag1 = Label(self.chat_frame, text="\t", relief="raised", bg="#9c9c9c", font="Arial 12")
        self.name_tag1.grid(row=1, column=0, pady=5)
        
        self.name_tag2 = Label(self.chat_frame, text="\t", relief="raised", bg="#9c9c9c", font="Arial 12")
        self.name_tag2.grid(row=3, column=0, pady=5)
        
        self.name_tag3 = Label(self.chat_frame, text="\t", relief="raised", bg="#9c9c9c", font="Arial 12")
        self.name_tag3.grid(row=5, column=0, pady=5)
        
        self.text_box1 = Text(self.chat_frame, width=31, height=5, font="Arial 14", padx=10, pady=10, bg="lightgray", wrap="word", state=DISABLED)
        self.text_box1.grid(row=0, column=1, rowspan=2, sticky=N, padx=10, pady=5)
        
        self.text_box2 = Text(self.chat_frame, width=31, height=5, font="Arial 14", padx=10, pady=10, bg="lightgray", wrap="word", state=DISABLED)
        self.text_box2.grid(row=2, column=1, rowspan=2, sticky=N, padx=10, pady=5)
        
        self.text_box3 = Text(self.chat_frame, width=31, height=5, font="Arial 14", padx=10, pady=10, bg="lightgray", wrap="word", state=DISABLED)
        self.text_box3.grid(row=4, column=1, rowspan=2, sticky=N, padx=10, pady=5)
        
        self.chat_widgets = {"Image" : [self.chat_image1, self.chat_image2, self.chat_image3],
                             "Name Tag" : [self.name_tag1, self.name_tag2, self.name_tag3],
                             "Textbox" : [self.text_box1, self.text_box2, self.text_box3]}
        
        self.suspicion_status = Label(self.chat_frame, text="\t\t", font="Arial 14", bg="#e55858", borderwidth=2, relief="raised")
        self.suspicion_status.grid(row=5, column=1, pady=5, ipadx=5)
        
        # Creating Reply Frame
        self.reply_frame = Frame(self.window, bg="#9c9c9c", highlightbackground="#212121", highlightthickness=2)
        self.reply_frame.grid(row=2, column=1)
        
        Label(self.reply_frame, text="Select Player:", font="Arial 14", bg="#9c9c9c").grid(row=0, column=0)
        self.reply_players = ttk.Combobox(self.reply_frame, width=12, font="Arial 14", state=DISABLED)
        self.reply_players.grid(row=0, column=1, pady=5)
        
        self.reply_options = ttk.Combobox(self.reply_frame, width=40, font="Arial 14", state=DISABLED)
        self.reply_options.grid(row=1, column=0, columnspan=2, pady=5, padx=10)
        
        self.reply_button = Button(self.reply_frame, text="Reply", font="Arial 10 bold", width=10, bg="#666666", fg="white", state=DISABLED)
        self.reply_button.grid(row=2, column=0, columnspan=2, pady=10, padx=5)
        
        # Creating Activity Frame
        self.activity_frame= Frame(self.window, bg="#9c9c9c") 
        self.activity_frame.grid(row=2, column=0)
        
    def text_converter(self, text):
        """Puts line breaks automatically in text"""
        self.arial36b = tkFont.Font(family='Arial', size=20)
        self.line, self.new_text = "", ""
        for word in text.split():
            self.width = self.arial36b.measure(self.line + word)
            if self.width <= 700:
                self.line = self.line + word + " "
            else:
                self.new_text = self.new_text + self.line + "\n"
                self.line = word + " "
        self.new_text = self.new_text + self.line
        return self.new_text
    
    def update_players(self, players):
        """Updates player number status"""
        self.role_status.config(text=f"{len(players)+1} Players Remaining – Role: {self.role}")
    
    def proceed(self):
        """Function for allowing the main program to proceed"""
        self.is_button_pressed = True
        for widget in self.activity_frame.winfo_children(): # goes through every widget inside the frame
            widget.destroy() # deletes that widget
        self.clean_reply_menu()
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121") 
        
    def introduction(self, players):
        """Introduction to the players"""
        self.c.create_text(40, 70, text="[Narrator]: Welcome to Mafia. Here are today's contestants:", anchor=NW, fill="white", font="Arial 20")
        self.photo_list = []
        for index in range(0, 6):
            self.photo_list.append(Image.open(players[index]["Photo"]))
            self.photo_list[index] = self.photo_list[index].resize((137, 180))
            self.photo_list[index] = ImageTk.PhotoImage(self.photo_list[index])
            self.c.create_image(index*120+30, 110, anchor=NW, image=self.photo_list[index])
            self.name = players[index]["Name"]
            for x in range(-(len(players[index]["Name"]))+8): # adds space to make name for centered
                self.name = " " + self.name
            self.c.create_text(index*120+40, 300, text=self.name, anchor=NW, fill="white", font="Arial 20")
        for index in range(6, 9):
            self.photo_list.append(Image.open(players[index]["Photo"]))
            self.photo_list[index] = self.photo_list[index].resize((137, 180))
            self.photo_list[index] = ImageTk.PhotoImage(self.photo_list[index])
            self.c.create_image(index*150-720, 330, anchor=NW, image=self.photo_list[index])
            self.name = players[index]["Name"]
            for x in range(-(len(players[index]["Name"]))+8): # adds space to make name for centered
                self.name = " " + self.name
            self.c.create_text(index*150-710, 510, text=self.name, anchor=NW, fill="white", font="Arial 20")
        self.c.itemconfig(self.event_status, text="Introduction")
        self.is_button_pressed = False
        Button(self.activity_frame, text="Let's Play", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)
        
    def update_suspicion_points(self, points):
        """Updates suspicion points status"""
        self.suspicion_points = points
        self.suspicion_status.config(text=f"Suspicion Points = {self.suspicion_points}")
        
    def update_round_number(self, round_no):
        """Updates suspicion points status"""
        self.round_no = round_no
        self.c.itemconfig(self.round_status, text=f"Round {self.round_no}")
    
    def clean_reply_menu(self):
        self.img = PhotoImage(file="images/blank_profile.png")
        self.chat_image1.config(image=self.img)
        self.chat_image2.config(image=self.img)
        self.chat_image3.config(image=self.img)
        self.name_tag1.config(text="\t")
        self.name_tag2.config(text="\t")
        self.name_tag3.config(text="\t")
        self.text_box1.config(state=NORMAL)
        self.text_box1.delete(1.0, END)
        self.text_box1.config(state=DISABLED)
        self.text_box2.config(state=NORMAL)
        self.text_box2.delete(1.0, END)
        self.text_box2.config(state=DISABLED)
        self.text_box3.config(state=NORMAL)
        self.text_box3.delete(1.0, END)
        self.text_box3.config(state=DISABLED)
        
        self.reply_button.config(state=DISABLED, text="Reply")
        self.reply_players.delete(0, END)
        self.reply_players.config(state=DISABLED)
        self.reply_options.delete(0, END)
        self.reply_options.config(state=DISABLED)
    
    def show_reply(self):
        """Shows CPU's reply"""
        self.reply_button.config(state=DISABLED)       
        # Clear reply window
        self.img = PhotoImage(file="images/blank_profile.png")
        self.chat_image2.config(image=self.img)
        self.chat_image3.config(image=self.img)
        self.name_tag2.config(text="\t")
        self.name_tag3.config(text="\t")
        self.text_box2.config(state=NORMAL)
        self.text_box2.delete(1.0, END)
        self.text_box2.config(state=DISABLED)
        self.text_box3.config(state=NORMAL)
        self.text_box3.delete(1.0, END)
        self.text_box3.config(state=DISABLED)
        
        # Configure text
        self.selected_name = self.chat_names.index(self.reply_players.get())
        self.selected_reply = self.replies.index(self.reply_options.get())
        self.chat_image1.config(image=self.chat_photo[self.selected_name])
        self.name_tag1.config(text=self.chat_names[self.selected_name])
        self.text_box1.config(state=NORMAL)
        self.text_box1.delete(1.0, END)
        self.text_box1.insert(1.0, self.introductions[self.selected_name]) 
        self.text_box1.config(state=DISABLED)
        
        self.window.update_idletasks() 
        time.sleep(1)
        self.img2 = PhotoImage(file="images/player1_profile.png")
        self.chat_image2.config(image=self.img2)
        self.name_tag2.config(text=self.p1_name)
        self.text_box2.config(state=NORMAL)
        self.text_box2.delete(1.0, END)
        self.text_box2.insert(1.0, self.replies[self.selected_reply]) 
        self.text_box2.config(state=DISABLED)
        
        self.window.update_idletasks() 
        time.sleep(2)
        self.chat_image3.config(image=self.chat_photo[self.selected_name])
        self.name_tag3.config(text=self.chat_names[self.selected_name])
        
        self.text = choice(self.chat_list[self.selected_name][self.selected_reply+3])
        self.text = self.text.replace("player_name", self.p1_name)
        self.text = self.text.replace("opponent_name", self.chat_player_list[-1]["Name"])
        
        self.text_box3.config(state=NORMAL)
        self.text_box3.delete(1.0, END)
        self.text_box3.insert(1.0, self.text) 
        self.text_box3.config(state=DISABLED)
        
        self.introductions[self.selected_name] = "(CONVERSATION COMPLETED)"
        self.reply_button.config(state=NORMAL, text="Go back", command = lambda: self.mingle(self.introductions, self.chat_list, self.chat_num, self.chat_player_list, self.p1_name))
    
    def mingle_reply(self, event):
        """Enabled Reply Button"""
        self.reply_button.config(state=NORMAL, command=self.show_reply)
    
    def show_mingle_option(self, event):
        """Shows reply option for mingle"""
        self.reply_button.config(state=DISABLED, text="Reply")
        self.replies = []
        self.selected = self.chat_names.index(self.reply_players.get())
        for reply in self.chat_list[self.selected][2]:
            self.reply_text = reply
            self.reply_text = self.reply_text.replace("opponent_name", self.chat_player_list[-1]["Name"])
            self.replies.append(self.reply_text)
        
        self.reply_players.delete(0, END)
        self.reply_players.insert(0, self.chat_names[self.selected])
        self.reply_options.config(state=NORMAL, values=self.replies)
        self.reply_options.delete(0, END)
        self.reply_options.insert(0, "Select Reply")
        self.reply_options.bind("<<ComboboxSelected>>", self.mingle_reply) 
        
        if self.reply_players.get() == "n/a":
            self.reply_options.delete(0, END)
            self.reply_options.config(state=DISABLED)
            
    def mingle(self, introductions, chat_list, chat_num, chat_player_list, p1_name):
        """CPU players greet player 1"""
        self.clean_reply_menu()
        self.introductions, self.chat_list, self.chat_num, self.chat_player_list, self.p1_name = introductions, chat_list, chat_num, chat_player_list, p1_name
        self.c.create_text(40, 70, text=self.text_converter("[Narrator]: Before the game starts, you may have a quick chat with fellow players.")+"\n\nUse the menu on the right to do so. \t\t\t→", anchor=NW, fill="white", font="Arial 20")
        self.chat_names, self.chat_photo = [], []
        for index, player in enumerate(self.chat_list):
            self.chat_names.append(player[0]["Name"])
            self.chat_photo.append(Image.open(player[0]["Photo"]))
            self.chat_photo[index] = self.chat_photo[index].resize((100, 132))
            self.chat_photo[index] = ImageTk.PhotoImage(self.chat_photo[index])
            
            self.chat_widgets["Name Tag"][index].config(text=player[0]["Name"])
            self.chat_widgets["Image"][index].config(image=self.chat_photo[index])
            self.chat_widgets["Textbox"][index].config(state=NORMAL)
            self.chat_widgets["Textbox"][index].insert(1.0, introductions[index]) 
            self.chat_widgets["Textbox"][index].config(state=DISABLED)
            
            if self.introductions[index] == "(CONVERSATION COMPLETED)":
                self.chat_names[index] = "n/a"
                self.chat_widgets["Textbox"][index].insert(END, " - (COMPLETED)")
            
        self.reply_players.config(state=NORMAL, values=self.chat_names)
        self.reply_players.delete(0, END)
        self.reply_players.insert(0, "")
        self.reply_players.bind("<<ComboboxSelected>>", self.show_mingle_option) 
        
        if set(self.chat_names) == {"n/a"}:
            self.reply_players.config(state=DISABLED)
        
        self.is_button_pressed = False
        if not self.activity_frame.winfo_children():
            Button(self.activity_frame, text="Begin Game", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)
            
    def assign_roles(self, text, role):
        """Assign roles to players"""
        self.role = role
        self.text = self.text_converter("[Narrator]: " +  text)
        self.c.create_text(40, 70, text="[Narrator]: I will now assign roles.", anchor=NW, fill="white", font="Arial 20")
        for x in range(1,4):
            self.window.update_idletasks() 
            time.sleep(1)
            self.c.create_text(250, 100+x*50, text="Assigning roles...", anchor=NW, fill="gray70", font="Arial 20")
        self.window.update_idletasks() 
        time.sleep(1)
        self.c.create_text(40, 350, text=self.text, anchor=NW, fill="white", font="Arial 20")
        self.update_suspicion_points(0)
        self.role_status.config(text=f"10 Players Remaining – Role: {role}")
        self.is_button_pressed = False
        Button(self.activity_frame, text="Begin Game", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)
    
    def lights_out(self):
        """Display lights out"""
        self.c.itemconfig(self.event_status, text="Lights out")
        self.c.create_text(40, 70, text=f"[Narrator]: Round {self.round_no} – Lights out.", anchor=NW, fill="white", font="Arial 20")
        
    def murder_player1(self, murder_name, murder_data):
        """If player 1 gets murdered"""
        self.murder_name, self.murder_data = murder_name, murder_data
        
        self.murderer_statement = choice(self.murder_data["Murderer_Statement"])
        self.murderer_statement = self.murderer_statement.replace("victim_name", self.p1_name)
        self.victim_statement = choice(self.murder_data["Victim_Statement"])
        self.victim_statement = self.victim_statement.replace("murderer_name", self.murder_name)
        
        self.object1 = self.c.create_rectangle(0, 65, 800, 550, fill="#212121") 
        self.object2 = self.c.create_text(40, 70, text=f"[{self.murder_name}]: {self.murderer_statement}", anchor=NW, fill="white", font="Arial 20")
        self.window.update_idletasks() 
        time.sleep(1)
        self.object3 = self.c.create_text(40, 120, text=f"[{self.p1_name}]: {self.victim_statement}", anchor=NW, fill="gray70", font="Arial 20")
        self.window.update_idletasks() 
        time.sleep(1)
        self.object4 = self.c.create_text(40, 170, text=f"[{self.p1_name}]: ...", anchor=NW, fill="gray70", font="Arial 20")
        self.window.update_idletasks() 
        time.sleep(1)
    
    def murder_player(self):
        self.option = self.option_box.get()
        for player in self.players:
            if player["Name"] == self.option:
                self.murdered_player = player
        self.kill_button.config(state=DISABLED)
        self.option_box.config(state=DISABLED)
        
        self.murderer_statement = choice(self.murder_data["Murderer_Statement"])
        self.murderer_statement = self.murderer_statement.replace("victim_name", self.murdered_player["Name"])
        self.victim_statement = choice(self.murder_data["Victim_Statement"])
        self.victim_statement = self.victim_statement.replace("murderer_name", self.p1_name)
        
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121") 
        self.c.create_text(40, 70, text=f"[{self.p1_name}]: {self.murderer_statement}", anchor=NW, fill="white", font="Arial 20")
        self.window.update_idletasks() 
        time.sleep(1)
        self.c.create_text(40, 120, text=f"[{self.murdered_player['Name']}]: {self.victim_statement}", anchor=NW, fill="gray70", font="Arial 20")
        self.window.update_idletasks() 
        time.sleep(1)
        self.c.create_text(40, 170, text=f"[{self.murdered_player['Name']}]: ...", anchor=NW, fill="gray70", font="Arial 20")
        self.window.update_idletasks() 
        time.sleep(1)
        self.c.create_text(40, 220, text=f"You have successfully killed {self.murdered_player['Name']}", anchor=NW, fill="white", font="Arial 20")
        
        for widget in self.activity_frame.winfo_children():
            widget.destroy()
        self.is_button_pressed = False
        Button(self.activity_frame, text="Next", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)
    
    def enable_kill_button(self, event):
        self.kill_button.config(state=NORMAL)
    
    def murderer_action(self, players, murder_data):
        """Function for the murderer"""
        self.players, self.murder_data = players, murder_data
        self.is_button_pressed = False
        self.player_name_list = []
        for player in players:
            self.player_name_list.append(player["Name"])
        self.option_box = ttk.Combobox(self.activity_frame, width=30, font="Arial 20", values=self.player_name_list)
        self.option_box.grid(row=0, column=0, padx=10)
        self.option_box.insert(0, "Select which player to kill:")
        self.option_box.bind("<<ComboboxSelected>>", self.enable_kill_button)
        self.kill_button = Button(self.activity_frame, text="Murder Player", font="Arial 14 bold", bg="#666666", fg="white", command=self.murder_player, state=DISABLED)
        self.kill_button.grid(row=0, column=1, ipadx=10)
    
    def save_player(self):
        self.option = self.option_box.get()
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121") 
        if self.option[-9:-1] == "yourself":
            self.c.create_text(40, 70, text="You chose to save yourself.", anchor=NW, fill="white", font="Arial 20")
        else:
            self.c.create_text(40, 70, text=f"You chose to save {self.option}.", anchor=NW, fill="white", font="Arial 20")
        for widget in self.activity_frame.winfo_children():
            widget.destroy()
        self.is_button_pressed = False
        Button(self.activity_frame, text="Next", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)
    
    def enable_save_button(self, event):
        self.save_button.config(state=NORMAL)
    
    def doctor_action(self, players):   
        """Function for the doctor"""       
        self.is_button_pressed = False
        self.player_name_list = []
        for player in players:
            self.player_name_list.append(player["Name"])
        self.player_name_list.append(f"{self.p1_name} (yourself)")
        self.option_box = ttk.Combobox(self.activity_frame, width=30, font="Arial 20", values=self.player_name_list)
        self.option_box.grid(row=0, column=0, padx=10)
        self.option_box.insert(0, "Select which player to save:")
        self.option_box.bind("<<ComboboxSelected>>", self.enable_save_button)
        self.save_button = Button(self.activity_frame, text="Save Player", font="Arial 14 bold", bg="#666666", fg="white", command=self.save_player, state=DISABLED)
        self.save_button.grid(row=0, column=1, ipadx=10)
        
    def make_statement(self):
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        self.suspicious_player = {"Name" : "Noone"}
        
        if self.suspicion_level == 0:
            self.c.create_text(40, 70, text="You chose to say nothing.", anchor=NW, fill="white", font="Arial 20")            
        else:
            self.authority_points -= self.suspicion_level
            self.suspicious_player = self.option_box.get()
            for player in self.players:
                if player["Name"] == self.suspicious_player:
                    self.suspicious_player = player
            self.c.create_text(40, 70, text=f"You chose to suspect {self.suspicious_player['Name']}.", anchor=NW, fill="white", font="Arial 20")
        self.c.create_text(40, 120, text=f"You now have {self.authority_points} authority points.", anchor=NW, fill="white", font="Arial 20")
        for widget in self.activity_frame.winfo_children():
            widget.destroy()
        self.is_button_pressed = False
        Button(self.activity_frame, text="Next", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)
    
    def detect_player(self):
        self.suspicion_level = int(self.option_box.get()[0])
        for widget in self.activity_frame.winfo_children():
            widget.destroy()
        if self.suspicion_level == 0:
            self.make_statement()
        else:
            self.c.create_rectangle(0, 65, 800, 550, fill="#212121") 
            self.c.create_text(40, 70, text="Now select the suspicious player", anchor=NW, fill="white", font="Arial 20")
            
            self.player_name_list = []
            for player in self.players:
                self.player_name_list.append(player["Name"])
                
            self.option_box = ttk.Combobox(self.activity_frame, width=30, font="Arial 20", values=self.player_name_list)
            self.option_box.grid(row=0, column=0, padx=10)
            self.option_box.insert(0, "Select your option:")
            self.option_box.bind("<<ComboboxSelected>>", self.enable_detective_button)
            self.stat_button = Button(self.activity_frame, text="Select", font="Arial 14 bold", bg="#666666", fg="white", command=self.make_statement, state=DISABLED)
            self.stat_button.grid(row=0, column=1, ipadx=10)
    
    def enable_detective_button(self, event):
        self.stat_button.config(state=NORMAL)
    
    def detective_action(self, players, authority_points):
        self.players, self.authority_points = players, authority_points
        self.is_button_pressed = False
        """Function for the detective"""
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121") 
        self.c.create_text(40, 70, text="You can now choose to say who you think the murderer is.", anchor=NW, fill="white", font="Arial 20")
        self.c.create_text(40, 120, text=f"You have {self.authority_points} authority points.", anchor=NW, fill="white", font="Arial 20")
        self.c.create_text(40, 170, text="You can now choose to say who you think the murderer is.", anchor=NW, fill="white", font="Arial 20")
        
        self.detective_statements = []
        if self.authority_points >= 1:
            self.detective_statements.append('1 point – "I think the murderer is..."')
        if self.authority_points >= 2:
            self.detective_statements.append('2 points – "I am certain that the murderer is..."')
        self.detective_statements.append("0 points – (Say nothing)")
        
        self.option_box = ttk.Combobox(self.activity_frame, width=30, font="Arial 20", values=self.detective_statements)
        self.option_box.grid(row=0, column=0, padx=10)
        self.option_box.insert(0, "Select your option:")
        self.option_box.bind("<<ComboboxSelected>>", self.enable_detective_button)
        self.stat_button = Button(self.activity_frame, text="Select Statement", font="Arial 14 bold", bg="#666666", fg="white", command=self.detect_player, state=DISABLED)
        self.stat_button.grid(row=0, column=1, ipadx=10)
    
    def lights_out_continued(self, is_doctor, is_detective):
        """Display wake up"""
        self.is_doctor, self.is_detective = is_doctor, is_detective
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121") 
        self.c.create_text(200, 100, text="The murderer has done their role", anchor=NW, fill="gray70", font="Arial 20")
        self.window.update_idletasks() 
        time.sleep(2)
        if self.is_doctor == True:
            self.c.create_text(200, 150, text="The doctor has done their role", anchor=NW, fill="gray70", font="Arial 20")
        else:
            self.c.create_text(200, 150, text="There is no doctor", anchor=NW, fill="gray70", font="Arial 20")
        self.window.update_idletasks() 
        time.sleep(2)
        if self.is_detective == True:
            self.c.create_text(200, 200, text="The detective has done their role", anchor=NW, fill="gray70", font="Arial 20")
        else:
            self.c.create_text(200, 200, text="There is no detective", anchor=NW, fill="gray70", font="Arial 20")
        self.window.update_idletasks() 
        time.sleep(2)
        self.c.create_text(40, 300, text="[Narrator]: Wake Up!", anchor=NW, fill="white", font="Arial 20")
        self.is_button_pressed = False
        Button(self.activity_frame, text="Next", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)
        
    def show_events(self, murdered_player, doctor, detective, saved_player, suspicion_level, suspicious_player, players):
        """Show who has been murdered and who has been saved"""
        self.c.itemconfig(self.event_status, text="Update")
        self.players = players
        if murdered_player == saved_player: #if the player has been saved
            self.c.create_text(40, 70, text=self.text_converter(f"[Narrator]: The murderer tried to kill {murdered_player['Name']} but the doctor saved them."), anchor=NW, fill="white", font="Arial 20")
        elif murdered_player != saved_player and saved_player == doctor:
            self.c.create_text(40, 70, text=self.text_converter(f"[Narrator]: {murdered_player['Name']} has been killed by the murderer and the doctor selfishly saved themself."), anchor=NW, fill="white", font="Arial 20")
            self.players.remove(murdered_player)
            self.role_status.config(text=f"{len(players)+1} Players Remaining – Role: {self.role}")
        else: #if not
            self.c.create_text(40, 70, text=self.text_converter(f"[Narrator]: {murdered_player['Name']} has been killed by the murderer and the doctor failed to heal them."), anchor=NW, fill="white", font="Arial 20")
            self.players.remove(murdered_player)
            self.role_status.config(text=f"{len(players)+1} Players Remaining – Role: {self.role}")
            
        if murdered_player == doctor and saved_player != doctor:
            self.c.create_text(40, 170, text=f"{murdered_player['Name']} was the Doctor.", anchor=NW, fill="white", font="Arial 20")
        elif murdered_player == detective and saved_player != detective:
            self.c.create_text(40, 170, text=f"{murdered_player['Name']} was the Detective.", anchor=NW, fill="white", font="Arial 20")
            
        if suspicion_level == 1 and suspicious_player['Name'] != "Noone" and ((murdered_player != detective and saved_player != detective) or (murdered_player == detective and saved_player == detective)):
            self.c.create_text(40, 270, text=self.text_converter(f"The detective thinks {suspicious_player['Name']} is the murderer, but is not certain."), anchor=NW, fill="white", font="Arial 20")
        elif suspicion_level == 2 and suspicious_player['Name'] != "Noone" and ((murdered_player != detective and saved_player != detective) or (murdered_player == detective and saved_player == detective)):
            self.c.create_text(40, 270, text=self.text_converter(f"The detective is certain that {suspicious_player['Name']} is the murderer."), anchor=NW, fill="white", font="Arial 20")     
        self.is_button_pressed = False
        Button(self.activity_frame, text="Next", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)
        
    def show_CPU_reply(self):
        """Shows CPU's reply"""
        self.reply_button.config(state=DISABLED)       
        # Clear reply window
        self.img = PhotoImage(file="images/blank_profile.png")
        self.chat_image2.config(image=self.img)
        self.chat_image3.config(image=self.img)
        self.name_tag2.config(text="\t")
        self.name_tag3.config(text="\t")
        self.text_box2.config(state=NORMAL)
        self.text_box2.delete(1.0, END)
        self.text_box2.config(state=DISABLED)
        self.text_box3.config(state=NORMAL)
        self.text_box3.delete(1.0, END)
        self.text_box3.config(state=DISABLED)
        
        # Configure text
        self.selected_name = self.chat_names.index(self.reply_players.get())
        self.selected_reply = self.reply_options_data[self.reply_options_text.index(self.reply_options.get())]
        self.chat_image1.config(image=self.chat_photo[self.selected_name])
        self.name_tag1.config(text=self.chat_names[self.selected_name])
        self.text_box1.config(state=NORMAL)
        self.text_box1.delete(1.0, END)
        self.text_box1.insert(1.0, self.chat_question[self.selected_name]) 
        self.text_box1.config(state=DISABLED)
        
        self.window.update_idletasks() 
        time.sleep(1)
        self.img2 = PhotoImage(file="images/player1_profile.png")
        self.chat_image2.config(image=self.img2)
        self.name_tag2.config(text=self.p1_name)
        self.text_box2.config(state=NORMAL)
        self.text_box2.delete(1.0, END)
        self.text_box2.insert(1.0, self.selected_reply["Answer"]) 
        self.text_box2.config(state=DISABLED)
        
        self.window.update_idletasks() 
        time.sleep(2)
        self.answer_index = self.chat_names.index(self.reply_players.get())
        if self.selected_reply["Points"] == 20:
            self.reply  = "3"
            self.percentage_change = 0.3
        elif self.selected_reply["Points"] == 10:
            self.reply  = "2"
            self.percentage_change = 0.5
        elif self.selected_reply["Points"] == 5:
            self.reply  = "1"
            self.percentage_change = 0.7
        if random() < self.percentage_change: #Lost suspicion points
            self.reply_text = self.discuss_vote[self.answer_index]["Reply" + self.reply]["Good"]
            if len(self.players) >= 3:
                self.reply_text = self.reply_text.replace("susp_opponent1", self.opponents_list[0])
            if len(self.players) >= 4:
                self.reply_text = self.reply_text.replace("susp_opponent2", self.opponents_list[1])
            
            self.chat_image3.config(image=self.chat_photo[self.selected_name])
            self.name_tag3.config(text=self.chat_names[self.selected_name])
            
            self.text_box3.config(state=NORMAL)
            self.text_box3.delete(1.0, END)
            self.text_box3.insert(1.0, self.reply_text) 
            self.text_box3.config(state=DISABLED)
            
            self.suspicion_points -= self.selected_reply["Points"]
            self.update_suspicion_points(self.suspicion_points)
        else: #Gain suspicion points
            self.reply_text = self.discuss_vote[self.answer_index]["Reply" + self.reply]["Bad"]
            if len(self.players) >= 3:
                self.reply_text = self.reply_text.replace("susp_opponent1", self.opponents_list[0])
            if len(self.players) >= 4:
                self.reply_text = self.reply_text.replace("susp_opponent2", self.opponents_list[1])
            
            self.chat_image3.config(image=self.chat_photo[self.selected_name])
            self.name_tag3.config(text=self.chat_names[self.selected_name])
            
            self.text_box3.config(state=NORMAL)
            self.text_box3.delete(1.0, END)
            self.text_box3.insert(1.0, self.reply_text) 
            self.text_box3.config(state=DISABLED)
            
            self.suspicion_points += self.selected_reply["Points"]
            self.update_suspicion_points(self.suspicion_points)
        self.chat_question[self.answer_index] = "(CONVERSATION COMPLETED)"
    
        self.reply_button.config(state=NORMAL, text="Go back", command = self.prevote_chat_continued)
    
    def chat_reply(self, event):
        """Enabled Reply Button"""
        self.reply_button.config(state=NORMAL, command=self.show_CPU_reply)
    
    def show_chat_option(self, event):
        """Shows reply option for prevote chat"""
        self.reply_button.config(state=DISABLED, text="Reply")   
        self.selected = self.chat_names.index(self.reply_players.get())
        self.reply_options_data,  self.reply_options_text = [], []
        self.reply_choices = [("1", 0), ("1", 1), ("2", 0), ("2", 1), ("3", 0), ("3", 1)]
        for index in range(3):
            shuffle(self.reply_choices)
            self.reply = self.reply_choices.pop(0)
            self.reply_text = self.discuss_vote[self.selected]["Answer" + self.reply[0]]["Answer"][self.reply[1]]
            if len(self.players) >= 3:
                self.reply_text = self.reply_text.replace("susp_opponent1", self.opponents_list[0])
            if len(self.players) >= 4:
                self.reply_text = self.reply_text.replace("susp_opponent2", self.opponents_list[1])
            self.reply_options_data.append({"Answer" : self.reply_text, "Points" : self.discuss_vote[self.selected]["Answer" + self.reply[0]]["Points"]})
            self.reply_options_text.append(self.reply_options_data[index]['Answer'] + " ± " + str(self.reply_options_data[index]['Points']) + " points")
                
        self.reply_players.delete(0, END)
        self.reply_players.insert(0, self.chat_names[self.selected])
        self.reply_options.config(state=NORMAL, values=self.reply_options_text)
        self.reply_options.delete(0, END)
        self.reply_options.insert(0, "Select Reply")
        self.reply_options.bind("<<ComboboxSelected>>", self.chat_reply) 
        
        if self.reply_players.get() == "n/a":
            self.reply_options.delete(0, END)
            self.reply_options.config(state=DISABLED)
            
    def prevote_chat(self, players, suspicion_points, prevote_data, discuss_topics, round_no):
        """CPU players talk with Player 1"""
        self.clean_reply_menu()
        self.c.itemconfig(self.event_status, text="Prevote Chat")
        self.discuss_vote, self.chat_player_list, self.discuss_vote_questions, self.reply_options_data, self.opponents_list = [], [], [], [], []
        self.players, self.suspicion_points, self.prevote_data, self.discuss_topics, self.round_no = players, suspicion_points, prevote_data, discuss_topics, round_no
        
        if len(self.players) >= 3:
            self.chat_num = randint(2,3) #How many people want to talk to you
        else:
            self.chat_num =randint(1,2)
        self.chat_list = self.players.copy()
        shuffle(self.chat_list)
        for _ in range(0, self.chat_num):
            self.chat_player_list.append(self.chat_list.pop(0))
        
        self.chat_names, self.chat_photo, self.chat_question = [], [], [] 
        for index, player, in enumerate(self.chat_player_list):
            if len(self.players) >= 4: #if there are more than 4 CPU players
                self.discuss_topics.append(4)
            else:
                if 4 in self.discuss_topics:
                    self.discuss_topics.remove(4)
            self.percentage_chance = (self.suspicion_points*3)/100
            if self.round_no > 2 and random() < self.percentage_chance:
                self.discuss_vote.append(choice(self.prevote_data[3]))
            else:
                self.discuss_vote.append(self.prevote_data[choice(self.discuss_topics)])
            self.opponents = list.copy(self.players)
            self.opponents.remove(player)
            self.discuss_vote_question = choice(self.discuss_vote[index]['Question'])
            if len(self.players) >= 3:
                self.discuss_vote_question = self.discuss_vote_question.replace("susp_opponent1", self.opponents[-1]["Name"])
            if len(self.players) >= 4:
                self.discuss_vote_question = self.discuss_vote_question.replace("susp_opponent2", self.opponents[-2]["Name"])
            self.discuss_vote_questions.append(self.discuss_vote_question)
            if len(self.players) >= 4:
                self.opponents_list = [self.opponents[-1]["Name"], self.opponents[-2]["Name"]]
            elif len(self.players) >= 3:
                self.opponents_list = [self.opponents[-1]["Name"]]
            self.chat_names.append(player["Name"])
            
            self.chat_photo.append(Image.open(player["Photo"]))
            self.chat_photo[index] = self.chat_photo[index].resize((100, 132))
            self.chat_photo[index] = ImageTk.PhotoImage(self.chat_photo[index])
            
            self.chat_question.append(self.discuss_vote_questions[index])
        self.prevote_chat_continued()
            
    def prevote_chat_continued(self):
        self.clean_reply_menu()
        self.c.create_text(40, 70, text=self.text_converter("[Narrator]: You may now talk in between yourselves to discuss who to vote out.")+"\n\nUse the menu on the right to do so. \t\t\t→", anchor=NW, fill="white", font="Arial 20")
        for index, player in enumerate(self.chat_player_list):           
            self.chat_widgets["Name Tag"][index].config(text=player["Name"])
            self.chat_widgets["Image"][index].config(image=self.chat_photo[index])
            self.chat_widgets["Textbox"][index].config(state=NORMAL)
            self.chat_widgets["Textbox"][index].insert(1.0, self.chat_question[index]) 
            self.chat_widgets["Textbox"][index].config(state=DISABLED)
            
            if self.chat_question[index] == "(CONVERSATION COMPLETED)":
                self.chat_names[index] = "n/a"
                self.chat_widgets["Textbox"][index].insert(END, " - (COMPLETED)")
        
        
        self.reply_players.config(state=NORMAL, values=self.chat_names)
        self.reply_players.delete(0, END)
        self.reply_players.insert(0, "")
        self.reply_players.bind("<<ComboboxSelected>>", self.show_chat_option) 
        self.reply_options.delete(0, END)
        self.reply_options.config(state=DISABLED)
        self.reply_button.config(state=DISABLED)
        
        if set(self.chat_names) == {"n/a"}:
            self.reply_players.config(state=DISABLED)
        
        self.is_button_pressed = False
        if not self.activity_frame.winfo_children():
            Button(self.activity_frame, text="Next", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)  
    
    def confirm_vote(self):
        if self.vote.get() != None:
            self.voting_board[self.vote.get()] += 1
            self.proceed()
            self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
            
            self.top_players = {}
            self.voting_board = {k: v for k, v in sorted(self.voting_board.items(), reverse=True, key=lambda item: item[1])}
                
            for result in list(self.voting_board.keys()): #working out the players with the most votes
                if self.top_players == {}:
                    self.top_players[result] = self.voting_board[result] 
                else:
                    if self.voting_board[result] in list(self.top_players.values()):
                        self.top_players[result] = self.voting_board[result]
                    else:
                        break
            self.top_players = list(self.top_players.keys())
            
            self.c.create_text(40, 70, text=self.text_converter("[Narrator]: Here are the results."), anchor=NW, fill="white", font="Arial 20")
            for index, result in enumerate(list(self.voting_board.keys())): #show results
                self.c.create_text(40, 150+40*index, text=result + " - " + str(self.voting_board[result]), anchor=NW, fill="gray70", font="Arial 20")
            Button(self.activity_frame, text="Next", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)
            
    def enable_confirm_btn(self):
        self.voting_menu.destroy()
        self.next_btn.configure(state=NORMAL)
    
    def open_voting_board(self):
        self.voting_menu = Toplevel()
        self.voting_menu.title("Vote Player")
        self.voting_menu.iconbitmap("images/mafia_icon.ico")
        self.voting_menu.config(bg="#9c9c9c")
        
        self.vote = StringVar()
        self.vote.set(None)
        
        for index, result in enumerate(list(self.voting_board.keys())):
            Radiobutton(self.voting_menu, text=result, font="Arial 20 bold", variable=self.vote, value=result, bg="#666666", fg="white", selectcolor="#666666", relief=RAISED, command=self.enable_confirm_btn).grid(row=index, column=0, pady=5, padx=100, sticky=W, ipadx=10)
        
        self.voting_menu.mainloop()
            
    def show_votes_1(self, voting_board):
        """Show CPU votings"""
        self.is_button_pressed = False
        self.voting_board = voting_board
        self.c.itemconfig(self.event_status, text="Voting")
        self.c.create_text(40, 70, text=self.text_converter("[Narrator]: Voting Time - please vote for the person who you think is the most guilty."), anchor=NW, fill="white", font="Arial 20")
        
        for index, result in enumerate(list(voting_board.keys())): #show results
            self.c.create_text(40, 150+40*index, text=result + " - " + str(voting_board[result]), anchor=NW, fill="gray70", font="Arial 20")
        
        Button(self.activity_frame, text="Open Voting Board", font="Arial 18 bold", bg="#666666", fg="white", command=self.open_voting_board).grid(row=0, column=0, ipadx=10, padx=10)
        self.is_button_pressed = False
        self.next_btn = Button(self.activity_frame, text="Confirm Vote", font="Arial 18 bold", bg="#666666", fg="white", command=self.confirm_vote, state=DISABLED)
        self.next_btn.grid(row=0, column=1, ipadx=10, padx=10)
    
    def show_votes_2(self, text1, text2):
        """Show text after vote"""
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        self.c.create_text(40, 70, text=self.text_converter(text1) + "\n\n" + self.text_converter(text2), anchor=NW, fill="white", font="Arial 20")
        self.is_button_pressed = False
        Button(self.activity_frame, text="Next", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)       
    
    def end_game(self, text, murderer, doctor, detective, p1_name):
        """End of game"""
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        self.c.itemconfig(self.event_status, text="Voting")
        self.c.create_text(40, 70, text=text, anchor=NW, fill="white", font="Arial 20")
        if murderer == p1_name:
            murderer = {"Name" : p1_name}
        elif doctor == p1_name:
            doctor = {"Name" : p1_name}
        elif detective == p1_name:
            detective = {"Name" : p1_name}
        self.c.create_text(40, 150, text=f"The murderer was {murderer['Name']}\nThe doctor was {doctor['Name']}\nThe detective was {detective['Name']}", anchor=NW, fill="white", font="Arial 20")
        for widget in self.activity_frame.winfo_children():
            widget.destroy()
    
    def revote_1(self, top_players, revote_data):
        """If 1 CPU is voted out"""
        self.top_players, self.revote_data = top_players, revote_data
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        for widget in self.activity_frame.winfo_children():
            widget.destroy()
        self.is_button_pressed = False
        self.c.create_text(40, 70, text=self.text_converter(f"[{top_players[0]}]: {choice(revote_data)}"), anchor=NW, fill="white", font="Arial 20")
        Label(self.activity_frame, text=f"Do you think {top_players[0]} is guilty?", font="Arial 16", bg="#9c9c9c", fg="black").grid(row=0, column=0, padx=10, pady=5)
        self.vote = IntVar()
        self.vote.set(2)
        Radiobutton(self.activity_frame, text="Yes", font="Arial 16 bold", variable=self.vote, value=1, bg="gray80", fg="black", indicatoron=0, command=self.proceed).grid(row=0, column=1, pady=5, padx=10, ipadx=10)
        Radiobutton(self.activity_frame, text="No", font="Arial 16 bold", variable=self.vote, value=0, bg="gray80", fg="black", indicatoron=0, command=self.proceed).grid(row=0, column=2, pady=5, padx=10, ipadx=10)
    
    def enable_confirm_btn2(self):
        self.voting_menu.destroy()
        self.next_btn.configure(state=NORMAL)
    
    def open_voting_board2(self):
        self.voting_menu = Toplevel()
        self.voting_menu.title("Vote Player")
        self.voting_menu.iconbitmap("images/mafia_icon.ico")
        self.voting_menu.config(bg="#9c9c9c")
        
        self.vote = StringVar()
        self.vote.set(None)
        
        for index, result in enumerate(self.top_players):
            Radiobutton(self.voting_menu, text=result, font="Arial 20 bold", variable=self.vote, value=result, bg="#666666", fg="white", selectcolor="#666666", relief=RAISED, command=self.enable_confirm_btn2).grid(row=index, column=0, pady=5, padx=100, sticky=W, ipadx=10)
        
        self.voting_menu.mainloop()
    
    
    def revote_2(self, top_players, revote_data):
        """If multiple CPU are voted out"""
        self.top_players, self.revote_data = top_players, revote_data
        self.is_button_pressed = False
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        for widget in self.activity_frame.winfo_children():
            widget.destroy()
        self.c.create_text(40, 70, text="[Narrator]: Multiple people have the highest vote.\nYou will have to choose who to vote out.", anchor=NW, fill="white", font="Arial 20")
        for index, player in enumerate(self.top_players):
            self.c.create_text(40, 170 + 80*index, text=self.text_converter(f"[{player}]: {choice(revote_data)}"), anchor=NW, fill="gray70", font="Arial 20")
        
        Button(self.activity_frame, text="Open Voting Board", font="Arial 18 bold", bg="#666666", fg="white", command=self.open_voting_board2).grid(row=0, column=0, ipadx=10, padx=10)
        self.is_button_pressed = False
        self.next_btn = Button(self.activity_frame, text="Confirm Vote", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed, state=DISABLED)
        self.next_btn.grid(row=0, column=1, ipadx=10, padx=10)
    
    def enable_statement_btn(self, event):
        self.statement_btn.config(state=NORMAL)
    
    def revote_3(self, revote_data):
        """If Player 1 is voted out"""
        self.is_button_pressed = False
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        for widget in self.activity_frame.winfo_children():
            widget.destroy()
        self.c.create_text(40, 70, text="You have been voted as the murderer.\n\nSelect a statement to defend yourself.", anchor=NW, fill="white", font="Arial 20")
        self.all_statements = list.copy(revote_data)
        shuffle(self.all_statements)
        self.statement_options = []
        for index in range(0, 3):
            self.statement_options.append(self.all_statements.pop())
        self.statement_box = ttk.Combobox(self.activity_frame, value=self.statement_options, font="Arial 18", width=30)
        self.statement_box.grid(row=0, column=0, ipadx=10, padx=10)
        self.statement_box.delete(0, END)
        self.statement_box.insert(0, "Select Statement")
        self.statement_box.bind("<<ComboboxSelected>>", self.enable_statement_btn)
        self.statement_btn = Button(self.activity_frame, text="Confirm", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed, state=DISABLED)
        self.statement_btn.grid(row=0, column=1, ipadx=10, padx=10)
    
    def revote_4(self, revote_data, top_players):
        """If Player 1 and at least 1 CPU is voted out"""
        self.is_button_pressed = False
        self.top_CPU_players = top_players.copy()
        self.top_CPU_players.remove(self.p1_name)
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        for widget in self.activity_frame.winfo_children():
            widget.destroy()
        self.c.create_text(40, 70, text="[Narrator]: Multiple people have the highest vote.\nPlayers will have to choose who to vote out.", anchor=NW, fill="white", font="Arial 20")
        for index, player in enumerate(self.top_CPU_players):
            self.c.create_text(40, 170 + 80*index, text=self.text_converter(f"[{player}]: {choice(revote_data)}"), anchor=NW, fill="gray70", font="Arial 20")
        self.all_statements = list.copy(revote_data)
        shuffle(self.all_statements)
        self.statement_options = []
        for index in range(0, 3):
            self.statement_options.append(self.all_statements.pop())
        self.statement_box = ttk.Combobox(self.activity_frame, value=self.statement_options, font="Arial 18", width=30)
        self.statement_box.grid(row=0, column=0, ipadx=10, padx=10)
        self.statement_box.delete(0, END)
        self.statement_box.insert(0, "Select Statement")
        self.statement_box.bind("<<ComboboxSelected>>", self.enable_statement_btn)
        self.statement_btn = Button(self.activity_frame, text="Confirm", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed, state=DISABLED)
        self.statement_btn.grid(row=0, column=1, ipadx=10, padx=10)
        
    def free_time(self):
        """Free time screen"""
        self.is_button_pressed = False
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        self.c.itemconfig(self.event_status, text="Free Time")
        self.c.create_text(40, 70, text="[Narrator]:It's now free time.\n\n" + self.text_converter("During this time, players may ask you questions or tell you things which may help you out next voting round."), anchor=NW, fill="white", font="Arial 20")
        Button(self.activity_frame, text="Next", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)
        
    def correct_name(self):
        self.c.itemconfig(self.guess, text=f"[{self.p1_name}]: It's {self.statement_box.get().title()}")
        if self.statement_box.get().lower() == self.random_player["Name"].lower():
            self.c.create_text(40, 380, text=f"[{self.random_player['Name']}]: You got it right! (-10 suspicion points)", anchor=NW, fill="white", font="Arial 20")
            self.suspicion_points += -10
        else:
            self.c.create_text(40, 380, text=f"[{self.random_player['Name']}]: No, I'm not {self.statement_box.get().title()}. (+10 suspicion points)", anchor=NW, fill="white", font="Arial 20")
            self.suspicion_points += 10
        for widget in self.activity_frame.winfo_children():
            widget.destroy()
        self.update_suspicion_points(self.suspicion_points)
        Button(self.activity_frame, text="Next", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)
    
    def guess_the_name(self, players, suspicion_points):
        """Guess the players name based of their face"""
        self.is_button_pressed = False
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        self.c.itemconfig(self.event_status, text="Free Time - Chat")
        self.players, self.suspicion_points = players, suspicion_points
        self.random_player = choice(self.players)
        self.img = Image.open(self.random_player["Photo"])
        self.img = self.img.resize((137, 180))
        self.img = ImageTk.PhotoImage(self.img)
        self.c.create_image(320, 70, anchor=NW, image=self.img)
        self.c.create_text(40, 280, text="[???]: What is my name?", anchor=NW, fill="white", font="Arial 20")
        self.window.update_idletasks() 
        time.sleep(1)
        self.guess = self.c.create_text(40, 330, text=f"[{self.p1_name}]: It's... ", anchor=NW, fill="gray70", font="Arial 20")

        self.statement_box = Entry(self.activity_frame, font="Arial 18", width=20)
        self.statement_box.grid(row=0, column=0, ipadx=10, padx=10)
        self.statement_box.bind("<Key>", self.enable_statement_btn)
        self.statement_btn = Button(self.activity_frame, text="Confirm", font="Arial 18 bold", bg="#666666", fg="white", command=self.correct_name, state=DISABLED)
        self.statement_btn.grid(row=0, column=1, ipadx=10, padx=10)
        
    def correct_fact(self):
        self.c.itemconfig(self.guess, text=f"[{self.p1_name}]: It's {self.statement_box.get()}")
        if self.statement_box.get() == self.correct_answer:
            self.c.create_text(40, 240, text=f"[{self.random_player['Name']}]: You got it correct! (-10 suspicion points)", anchor=NW, fill="white", font="Arial 20")
            self.suspicion_points += -10
        else:
            self.c.create_text(40, 240, text=f"[{self.random_player['Name']}]: No sorry, it's {self.correct_answer} (-0 suspicion points)", anchor=NW, fill="white", font="Arial 20")
            
        for widget in self.activity_frame.winfo_children():
            widget.destroy()
        self.update_suspicion_points(self.suspicion_points)
        Button(self.activity_frame, text="Next", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)
    
    def guess_the_fact(self, players, suspicion_points, character_data):
        """Guess the player's fact"""
        self.is_button_pressed = False
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        self.c.itemconfig(self.event_status, text="Free Time - Chat")
        self.players, self.suspicion_points, self.character_data = players, suspicion_points, character_data
        
        self.random_player = choice(self.players)
        self.question_determiner = choice(["Fav_Sport", "Fav_Animal", "Fav_Mafia Role"])
        self.answers = []
        self.correct_answer = self.random_player[self.question_determiner]
        self.answers.append(self.correct_answer)
        for player in self.character_data:
            if player[self.question_determiner] not in self.answers:
                self.answers.append(player[self.question_determiner])
            if len(self.answers) == 3:
                break
        shuffle(self.answers) 
            
        self.c.create_text(40, 70, text=f"[{self.random_player['Name']}]: Guess my favourite {self.question_determiner[4:]}.", anchor=NW, fill="white", font="Arial 20")
        self.window.update_idletasks() 
        time.sleep(1)
        self.guess = self.c.create_text(40, 150, text=f"[{self.p1_name}]: It's... ", anchor=NW, fill="gray70", font="Arial 20")
        
        self.statement_box = ttk.Combobox(self.activity_frame, value=self.answers, font="Arial 18", width=30)
        self.statement_box.grid(row=0, column=0, ipadx=10, padx=10)
        self.statement_box.delete(0, END)
        self.statement_box.insert(0, "Choose Answer")
        self.statement_box.bind("<<ComboboxSelected>>", self.enable_statement_btn)
        self.statement_btn = Button(self.activity_frame, text="Confirm", font="Arial 18 bold", bg="#666666", fg="white", command=self.correct_fact, state=DISABLED)
        self.statement_btn.grid(row=0, column=1, ipadx=10, padx=10)
        
    def reveal_correct_answer(self):
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        self.c.create_text(40, 70, text=f"[{self.random_player['Name']}]: That is...", anchor=NW, fill="white", font="Arial 20")
        self.window.update_idletasks() 
        time.sleep(randint(1,3)) 
        if self.statement_box.get() == self.q_info["Answer"]:
            self.c.create_text(40, 120, text=f"[{self.random_player['Name']}]: That is the Correct Answer!", anchor=NW, fill="white", font="Arial 20")
            self.examine_players = True
        else:
            self.c.create_text(40, 120, text=self.text_converter(f"[{self.random_player['Name']}]: I'm sorry, but the correct answer is {self.q_info['Answer']}") + "\n\n" + self.text_converter("You did not earn permission to examine other players this round."), anchor=NW, fill="white", font="Arial 20")
        
        for widget in self.activity_frame.winfo_children():
            widget.destroy()
        Button(self.activity_frame, text="Next", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)
    
    def trivia_question(self, players, df, examine_players):
        """Guess the answer to the question"""
        self.is_button_pressed = False
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        self.c.itemconfig(self.event_status, text="Free Time - Challenge")
        self.players, self.df, self.examine_players = players, df, examine_players
        
        self.q_no = randint(0, 253) #question number
        self.q_options = []
        for x in range(1, 5):
            self.q_options.append(self.df.iloc[self.q_no]["Option " + chr(ord('@')+x)])
        shuffle(self.q_options)
        self.q_info = {"Question" : self.df.iloc[self.q_no]["Question"], "A" : self.q_options[0], "B" : self.q_options[1],
                  "C" : self.q_options[2], "D" : self.q_options[3], "Answer" : self.df.iloc[self.q_no]["Answer"]}
        self.random_player = choice(self.players)
        
        self.c.create_text(40, 70, text=f"[{self.random_player['Name']}]: Triva Round!\n\n" + self.text_converter(self.q_info['Question']), anchor=NW, fill="white", font="Arial 20")
        self.window.update_idletasks() 
        time.sleep(1)        
        for x in range(1, 5):
            self.c.create_text(40, 180+50*x, text=f"{chr(ord('@')+x)} - {self.q_info[chr(ord('@')+x)]}", anchor=NW, fill="gray70", font="Arial 20")
            self.window.update_idletasks() 
            time.sleep(0.75)
         
        self.statement_box = ttk.Combobox(self.activity_frame, value=self.q_options, font="Arial 18", width=30)
        self.statement_box.grid(row=0, column=0, ipadx=10, padx=10)
        self.statement_box.delete(0, END)
        self.statement_box.insert(0, "Choose Answer")
        self.statement_box.bind("<<ComboboxSelected>>", self.enable_statement_btn)
        self.statement_btn = Button(self.activity_frame, text="Confirm", font="Arial 18 bold", bg="#666666", fg="white", command=self.reveal_correct_answer, state=DISABLED)
        self.statement_btn.grid(row=0, column=1, ipadx=10, padx=10)
        
    def correct_shirt(self):
        self.img = Image.open(self.random_player["Photo"])
        self.img = self.img.resize((137, 180))
        self.img = ImageTk.PhotoImage(self.img)
        self.c.create_image(320, 70, anchor=NW, image=self.img)
        self.c.itemconfig(self.guess, text=f"[{self.p1_name}]: It's {self.statement_box.get()}")
        if self.statement_box.get() == self.correct_answer:
            self.c.create_text(40, 400, text=f"[{self.random_player['Name']}]: You got it correct!", anchor=NW, fill="white", font="Arial 20")
            self.examine_players = True
        else:
            self.c.create_text(40, 400, text=f"[{self.random_player['Name']}]: No sorry, it's {self.correct_answer}." + "\n\n" + self.text_converter("You did not earn permission to examine other players this round."), anchor=NW, fill="white", font="Arial 20")
            
        for widget in self.activity_frame.winfo_children():
            widget.destroy()
        Button(self.activity_frame, text="Next", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)
    
    def guess_the_shirt(self, players, character_data, examine_players):
        """Guess what colour shirt is the player wearing"""
        self.is_button_pressed = False
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        self.c.itemconfig(self.event_status, text="Free Time - Challenge")
        self.players, self.character_data, self.examine_players = players, character_data, examine_players
        
        self.random_player = choice(self.players)
        self.answers = []
        self.correct_answer = self.random_player["Colour"]
        self.answers.append(self.correct_answer)
        for player in self.character_data:
            if player["Colour"] not in self.answers:
                self.answers.append(player["Colour"])
            if len(self.answers) == 3:
                break
        shuffle(self.answers)
        
        self.c.create_text(40, 280, text=self.text_converter(f"[{self.random_player['Name']}]: Memory Round - Do you remember what colour shirt I'm wearing?"), anchor=NW, fill="white", font="Arial 20")
        self.window.update_idletasks() 
        time.sleep(1)
        self.guess = self.c.create_text(40, 350, text=f"[{self.p1_name}]: It's... ", anchor=NW, fill="gray70", font="Arial 20")
        
        self.statement_box = ttk.Combobox(self.activity_frame, value=self.answers, font="Arial 18", width=30)
        self.statement_box.grid(row=0, column=0, ipadx=10, padx=10)
        self.statement_box.delete(0, END)
        self.statement_box.insert(0, "Choose Answer")
        self.statement_box.bind("<<ComboboxSelected>>", self.enable_statement_btn)
        self.statement_btn = Button(self.activity_frame, text="Confirm", font="Arial 18 bold", bg="#666666", fg="white", command=self.correct_shirt, state=DISABLED)
        self.statement_btn.grid(row=0, column=1, ipadx=10, padx=10)
        
    def clicked_btn(self):
        if self.counter == 0:
            self.start_time = time.time()
            self.counter = 1
        elif self.counter > 0 and (time.time() - self.start_time <= 5):
            self.counter += 1
        else:
            for widget in self.activity_frame.winfo_children():
                 widget.destroy()
            self.c.create_text(40, 200, text=f"[{self.random_player['Name']}]: Your score was {self.counter}", anchor=NW, fill="white", font="Arial 20")
            if self.counter >= 30:
                self.c.create_text(40, 250, text=f"You did it!", anchor=NW, fill="white", font="Arial 20")
                self.examine_players = True
            else:
                self.c.create_text(40, 250, text=f"Sorry you were not fast enough.", anchor=NW, fill="white", font="Arial 20")
                self.c.create_text(40, 300, text="You did not earn permission to examine other players\nthis round.", anchor=NW, fill="white", font="Arial 20")
            self.window.update_idletasks() 
            time.sleep(2)
            Button(self.activity_frame, text="Next", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)

    def speed_clicker(self, players, examine_players):
        """How fast can Player 1 click in 5 seconds"""
        self.is_button_pressed = False
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        self.c.itemconfig(self.event_status, text="Free Time - Challenge")
        self.players, self.examine_players = players, examine_players
        
        self.random_player = choice(players)
        self.c.create_text(40, 70, text=self.text_converter(f"[{self.random_player['Name']}]: Speed Test - Can you press clicked the button 30 times in 5 seconds?") + "\nPress the button to start the timer.", anchor=NW, fill="white", font="Arial 20")
        self.counter = 0
        
        self.clicker = Button(self.activity_frame, text="Click Me", font="Arial 18 bold", bg="#666666", fg="white", command=self.clicked_btn)
        self.clicker.pack(ipadx=10)
    
    def end_typing(self, event):
        self.end = time.time() - self.start
        self.exclude = set(string.punctuation)
        self.text_typed = ''.join(ch for ch in self.statement_box.get() if ch not in self.exclude)
        self.word = ''.join(ch for ch in self.word if ch not in self.exclude)
        if self.text_typed.lower().replace(" ", "")[:len(self.word)] == self.word.lower().replace(" ", ""):
            self.c.create_text(40, 250, text=f"[{self.random_player['Name']}]: You typed the text correctly.", anchor=NW, fill="white", font="Arial 20")
            if self.end <= self.challenge_text["Time"]:
                self.c.create_text(40, 300, text=f"Your time was {round(self.end, ndigits=3)} seconds, which passes the time!", anchor=NW, fill="white", font="Arial 20")
                self.examine_players = True
            else:
                self.c.create_text(40, 300, text=f"Your time was {round(self.end, ndigits=3)} seconds, which is too slow.", anchor=NW, fill="white", font="Arial 20")
                self.c.create_text(40, 350, text="You did not earn permission to examine other players\nthis round.", anchor=NW, fill="white", font="Arial 20")
        else:
            self.c.create_text(40, 300, text=f"[{self.random_player['Name']}]: You typed the word incorrectly in {round(self.end, ndigits=3)} seconds.", anchor=NW, fill="white", font="Arial 20")
            self.c.create_text(40, 350, text="You did not earn permission to examine other players\nthis round.", anchor=NW, fill="white", font="Arial 20")
        for widget in self.activity_frame.winfo_children():
            widget.destroy()
        Button(self.activity_frame, text="Next", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)

    def start_typing(self):
        for widget in self.activity_frame.winfo_children():
            widget.destroy()
        self.statement_box = Entry(self.activity_frame, font="Arial 12", width=60)
        self.statement_box.pack(ipadx=10, padx=10)
        self.statement_box.bind("<Return>", self.end_typing)
        self.start = time.time()

    def speed_typer(self, players, sample_text, examine_players):
        """How fast can Player 1 type"""
        self.is_button_pressed = False
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        self.c.itemconfig(self.event_status, text="Free Time - Challenge")
        self.players, self.sample_text, self.examine_players = players, sample_text, examine_players
        
        self.random_player = choice(self.players)
        self.challenge_text = choice(self.sample_text)
        self.word = self.challenge_text["Text"]
        self.c.create_text(40, 70, text=f"[{self.random_player['Name']}]: Speed Test - Can you type the following text in less\nthan {self.challenge_text['Time']} seconds?", anchor=NW, fill="white", font="Arial 20")
        self.c.create_text(40, 150, text=self.text_converter(f"Text: {self.word}"), anchor=NW, fill="gray70", font="Arial 20")
        Button(self.activity_frame, text="Click Me", font="Arial 18 bold", bg="#666666", fg="white", command=self.start_typing).pack(ipadx=10)
        
    def estimation_btn(self):
        if self.time_started == False:
            self.start = time.time()
            self.timer_btn.config(text="End Time")
            self.time_started = True
        else:
            self.end = round(time.time() - self.start, ndigits=1)
            if self.end == float(self.seconds):
                self.c.create_text(40, 170, text=f"[{self.random_player['Name']}]: Your time was exactly {self.end} seconds, well done!", anchor=NW, fill="white", font="Arial 20")
                self.examine_players = True
            elif self.seconds-0.5 <= self.end <= self.seconds+0.5:
                self.c.create_text(40, 170, text=f"[{self.random_player['Name']}]: Your time was {self.end} seconds, but we will accept that.", anchor=NW, fill="white", font="Arial 20")
                self.examine_players = True
            else:
                self.c.create_text(40, 170, text=f"[{self.random_player['Name']}]: Sorry, your time was {self.end} seconds.", anchor=NW, fill="white", font="Arial 20")
                self.c.create_text(40, 220, text="You did not earn permission to examine other players\nthis round.", anchor=NW, fill="white", font="Arial 20")
                
            for widget in self.activity_frame.winfo_children():
                widget.destroy()
            Button(self.activity_frame, text="Next", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)

    def time_estimation(self, players, examine_players):
        """Can Player 1 estimate the time"""
        self.is_button_pressed = False
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        self.c.itemconfig(self.event_status, text="Free Time - Challenge")
        self.players, self.examine_players = players, examine_players
        
        self.random_player = choice(self.players)
        self.seconds = randint(5, 10)
        self.time_started = False
        
        self.c.create_text(40, 70, text=self.text_converter(f"[{self.random_player['Name']}]: Estimation Round - Can you estimate exactly {self.seconds} seconds?"), anchor=NW, fill="white", font="Arial 20")
        self.timer_btn = Button(self.activity_frame, text="Start Time", font="Arial 18 bold", bg="#666666", fg="white", command=self.estimation_btn)
        self.timer_btn.pack(ipadx=10)
        
    def reaction_wait(self):
        if self.time_started == False:
            self.timer_btn.config(text="Wait...", bg="#969696", state=DISABLED)
            self.window.update_idletasks() 
            time.sleep(self.waiting_time)
            self.start = time.time()
            self.time_started = True
            self.timer_btn.config(text="Now!", bg="red", state=NORMAL)
        else:
            self.end = time.time() - self.start
            if self.end < 0.3:
                self.c.create_text(40, 170, text=f"[{self.random_player['Name']}]: {round(self.end, ndigits=3)}s - Wow, you were fast", anchor=NW, fill="white", font="Arial 20")
                self.examine_players = True
            elif 0.3 <= self.end < 0.4:
                self.c.create_text(40, 170, text=f"[{self.random_player['Name']}]: {round(self.end, ndigits=3)}s - We will let you win this round.", anchor=NW, fill="white", font="Arial 20")
                self.examine_players = True
            else:
                self.c.create_text(40, 170, text=f"[{self.random_player['Name']}]: {round(self.end, ndigits=3)}s - Sorry, you were too slow.", anchor=NW, fill="white", font="Arial 20")
                self.c.create_text(40, 220, text="You did not earn permission to examine other players\nthis round.", anchor=NW, fill="white", font="Arial 20")
                
            for widget in self.activity_frame.winfo_children():
                widget.destroy()
            Button(self.activity_frame, text="Next", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)

    def reaction_test(self, players, examine_players):
        """How fast is Player 1's reaction speed"""
        self.is_button_pressed = False
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        self.c.itemconfig(self.event_status, text="Free Time - Challenge")
        self.players, self.examine_players = players, examine_players
        
        self.random_player = choice(self.players)
        self.waiting_time = randint(30, 80)/10
        self.time_started = False
        
        self.c.create_text(40, 70, text=self.text_converter(f"[{self.random_player['Name']}]: Reaction Round - How fast is your Reaction Speed?"), anchor=NW, fill="white", font="Arial 20")
        self.timer_btn = Button(self.activity_frame, text="Start", font="Arial 18 bold", bg="#666666", fg="white", command=self.reaction_wait)
        self.timer_btn.pack(ipadx=10)
        
    def reply_to_question(self):
        if self.murderer == self.p1_name:
            self.murderer = {"Name" : self.p1_name}
        self.option = self.question_list.index(self.statement_box.get())
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        self.c.create_text(40, 70, text=self.text_converter(f"[{self.p1_name}]: {self.interrogation['Q and A'][self.option]['Question']}"), anchor=NW, fill="white", font="Arial 20")
        
        for widget in self.activity_frame.winfo_children():
                widget.destroy()
        self.window.update_idletasks() 
        time.sleep(1)
        
        if self.option == 0: #Are you the murderer
            self.determiner = randint(1,3)
            if self.random_player == self.murderer and self.determiner <= 2:
                self.c.create_text(40, 170, text=self.text_converter(f"[{self.random_player['Name']}]: {self.interrogation['Q and A'][self.option]['Murderer']}"), anchor=NW, fill="gray70", font="Arial 20")
            else:
                self.c.create_text(40, 170, text=self.text_converter(f"[{self.random_player['Name']}]: {self.interrogation['Q and A'][self.option]['Innocent'].replace('p1_name', self.p1_name)}"), anchor=NW, fill="gray70", font="Arial 20")
        elif self.option == 1: #Are you the doctor
            if self.random_player == self.doctor:
                self.c.create_text(40, 170, text=self.text_converter(f"[{self.random_player['Name']}]: {self.interrogation['Q and A'][self.option]['Doctor']}"), anchor=NW, fill="gray70", font="Arial 20")
            else:
                self.c.create_text(40, 170, text=self.text_converter(f"[{self.random_player['Name']}]: {self.interrogation['Q and A'][self.option]['Innocent'].replace('p1_name', self.p1_name)}"), anchor=NW, fill="gray70", font="Arial 20")
        elif self.option == 2: #Are you the detective
            if self.random_player == self.detective:
                self.c.create_text(40, 170, text=self.text_converter(f"[{self.random_player['Name']}]: {self.interrogation['Q and A'][self.option]['Detective']}"), anchor=NW, fill="gray70", font="Arial 20")
            else:
                self.c.create_text(40, 170, text=self.text_converter(f"[{self.random_player['Name']}]: {self.interrogation['Q and A'][self.option]['Innocent'].replace('p1_name', self.p1_name)}"), anchor=NW, fill="gray70", font="Arial 20")
        
        elif self.option == 3: #Do you know who is the murderer
            self.not_murderer = []
            for player in self.players:
                if player != self.murderer:
                    self.not_murderer.append(player)
            if self.random_player == self.murderer:
                self.determiner = randint(1,2)
                if self.determiner == 1:
                    self.text = self.interrogation['Q and A'][self.option]['Sure']
                    self.text = self.text.replace("murderer_name", choice(self.not_murderer)["Name"])
                    self.c.create_text(40, 170, text=self.text_converter(f"[{self.random_player['Name']}]: {self.text}"), anchor=NW, fill="gray70", font="Arial 20")
                else:
                    self.text = self.interrogation['Q and A'][self.option]['Unsure']
                    self.text = self.text.replace("p1_name", self.p1_name)
                    self.c.create_text(40, 170, text=self.text_converter(f"[{self.random_player['Name']}]: {self.text}"), anchor=NW, fill="gray70", font="Arial 20")
            else:
                self.determiner = randint(1,6)
                if self.determiner == 1:
                    self.text = self.interrogation['Q and A'][self.option]['Sure']
                    self.text = self.text.replace("murderer_name", choice(self.not_murderer["Name"]))
                    self.c.create_text(40, 170, text=self.text_converter(f"[{self.random_player['Name']}]: {self.text}"), anchor=NW, fill="gray70", font="Arial 20")
                elif 2 <= self.determiner <= 3:
                    self.text = self.interrogation['Q and A'][self.option]['Sure']
                    self.text = self.text.replace("murderer_name", self.murderer["Name"])
                    self.c.create_text(40, 170, text=self.text_converter(f"[{self.random_player['Name']}]: {self.text}"), anchor=NW, fill="gray70", font="Arial 20")
                else:
                    self.text = self.interrogation['Q and A'][self.option]['Unsure']
                    self.text = self.text.replace("p1_name", self.p1_name)
                    self.c.create_text(40, 170, text=self.text_converter(f"[{self.random_player['Name']}]: {self.text}"), anchor=NW, fill="gray70", font="Arial 20")
        
        self.window.update_idletasks() 
        time.sleep(2)
        self.c.create_text(40, 270, text=self.text_converter(f"[{self.p1_name}]: {choice(self.interrogation['Farewell'])}"), anchor=NW, fill="gray70", font="Arial 20")
        if self.murderer["Name"] == self.p1_name:
            self.murderer = self.p1_name
        Button(self.activity_frame, text="Next", font="Arial 18 bold", bg="#666666", fg="white", command=self.proceed).pack(ipadx=10)

    def select_question(self):
        for player in self.players:
            if player["Name"] == self.statement_box.get():
                self.random_player = player

        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        self.text = choice(self.interrogation['Intro'])
        self.speech = self.text['P1']
        self.speech = self.speech.replace("opponent_name", self.random_player["Name"])
        self.c.create_text(40, 70, text=self.text_converter(f"[{self.p1_name}]: {self.speech}"), anchor=NW, fill="white", font="Arial 20")
        self.speech = self.text['CPU']
        self.speech = self.speech.replace("p1_name", self.p1_name)
        for widget in self.activity_frame.winfo_children():
                widget.destroy()
        self.window.update_idletasks() 
        time.sleep(1)
        self.c.create_text(40, 170, text=self.text_converter(f"[{self.random_player['Name']}]: {self.speech}"), anchor=NW, fill="gray70", font="Arial 20")
        
        self.question_list = []
        for index, question in enumerate(self.interrogation["Q and A"]):
            self.question_list.append(question['Question'])
            
        self.statement_box = ttk.Combobox(self.activity_frame, value=self.question_list, font="Arial 18", width=40)
        self.statement_box.grid(row=0, column=0, ipadx=10, padx=10)
        self.statement_box.delete(0, END)
        self.statement_box.insert(0, "Choose Question")
        self.statement_box.bind("<<ComboboxSelected>>", self.enable_statement_btn)
        self.statement_btn = Button(self.activity_frame, text="Confirm", font="Arial 18 bold", bg="#666666", fg="white", command=self.reply_to_question, state=DISABLED)
        self.statement_btn.grid(row=0, column=1, ipadx=10, padx=10)
        

    def interrogation_role(self, players, interrogation, murderer, doctor, detective):
        """Player can ask CPU questions"""
        self.players, self.interrogation, self.murderer, self.doctor, self.detective = players, interrogation, murderer, doctor, detective
        self.is_button_pressed = False
        self.c.create_rectangle(0, 65, 800, 550, fill="#212121")
        self.c.itemconfig(self.event_status, text="Free Time - Interrogation")
        
        self.c.create_text(40, 70, text="You can now choose who you would like to talk with:", anchor=NW, fill="white", font="Arial 20")
        self.player_name_list = []
        if len(self.players) >= 4:
            for index in range(0, 4):
                self.player_name_list.append(self.players[index]["Name"])
        else:
            for player in players:
                self.player_name_list.append(player["Name"])
                
        self.statement_box = ttk.Combobox(self.activity_frame, value=self.player_name_list, font="Arial 18", width=30)
        self.statement_box.grid(row=0, column=0, ipadx=10, padx=10)
        self.statement_box.delete(0, END)
        self.statement_box.insert(0, "Choose Player")
        self.statement_box.bind("<<ComboboxSelected>>", self.enable_statement_btn)
        self.statement_btn = Button(self.activity_frame, text="Confirm", font="Arial 18 bold", bg="#666666", fg="white", command=self.select_question, state=DISABLED)
        self.statement_btn.grid(row=0, column=1, ipadx=10, padx=10)
                
        