from tkinter import *
from random import shuffle, randint, choice, random
import pandas as pd
import time, json, threading
import sys

sys.path.append("modules")

from gui import Mafia

s = "Tnzr znqr ol Nyrknaqre Furznyl"

def start_game():
    """Run main code"""
    global root
    root = Toplevel()
    root.geometry("1325x700+10+10")
    root.title("Mafia in Python")
    root.iconbitmap("images/mafia_icon.ico")
    root.config(bg="#9c9c9c")
    
    threading.Thread(target=main).start()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    
def show_rules():
    rules_window = Toplevel()
    rules_window.title("Mafia Rules")
    rules_window.geometry("723x750+10+10")
    rules_window.config(bg="black")
    rules_window.iconbitmap("images/mafia_icon.ico")
    rules = PhotoImage(file="images/mafia_rules.png")
    Label(rules_window, bg="black", image=rules).pack()
    rules_window.mainloop()

def wait_for_response():
    """Function for stopping program until user meets required conditions"""
    global is_button_pressed
    while User_GUI.is_button_pressed == False: # Updates every 0.1 seconds
        root.update()
        time.sleep(0.1)
    is_button_pressed = False
    
def on_closing():
    if messagebox.askokcancel("Quit", "Are you sure you want to quit? The game is still in progress."):
        root.destroy()
    
def end_game():
    global User_GUI, murderer, doctor, detective, p1_name
    User_GUI.end_game("[Narrator]: Sorry you lost the game.", murderer, doctor, detective, p1_name)
    
def win_game():
    global User_GUI, murderer, doctor, detective, p1_name
    User_GUI.end_game("[Narrator]: Congratulations, you win!", murderer, doctor, detective, p1_name)
    
def main():
    global User_GUI, murderer, doctor, detective, p1_name
    players, chat_list, convo_topics, introductions, round_no = [], [], [0, 1, 2, 3, 4], [], 1
    suspicion_points, authority_points, discuss_topics, discuss_vote = 0, 4, [0, 1, 2], []
    is_button_pressed = False
    
    #Importing data
    with open("data\character_data.json", "r") as f:
        character_data = json.load(f)
    shuffle(character_data)
    
    with open("data\mingle_data.json", "r") as f:
        script_data = json.load(f)
        mingle_data = script_data[0]
        prevote_data = script_data[1]
        murder_data = script_data[2]
        revote_data = script_data[3]
        sample_text = script_data[4]
        interrogation = script_data[5]
    
    df = pd.read_csv(r"data\250 General Knowledge Questions.csv") 
    
    #Generating 9 CPU players
    for _ in range(0,9):
        players.append(character_data.pop(0))
        
    p1_name = enter_name.get().title().strip()
    if p1_name == "":
        p1_name = "Player 1"
    shuffle(players)
    
    User_GUI = Mafia(root)
    User_GUI.introduction(players)
    wait_for_response()
    
    chat_num = randint(2,3) #How many people want to talk to you
    chat_player_list = players.copy()
    shuffle(chat_player_list)
    for _ in range(0, chat_num):
        chat_list.append([chat_player_list.pop(0)])
    for index, player, in enumerate(chat_list):
        convo_topic = choice(convo_topics)
        convo_topics.remove(convo_topic)
        chat_list[index].append(choice(mingle_data[convo_topic][0]))
        chat_list[index][1] = chat_list[index][1].replace("player_name", p1_name)
        chat_list[index][1] = chat_list[index][1].replace("opponent_name", chat_player_list[-1]["Name"])
        for x in range(1,5):
            chat_list[index].append(mingle_data[convo_topic][x])
        introductions.append(chat_list[index][1])
        
    User_GUI.mingle(introductions, chat_list, chat_num, chat_player_list, p1_name)
    wait_for_response()
    # assignning roles
    determiner = randint(1,5)
    if determiner == 1:
        murderer = p1_name
        doctor = players[0]
        detective = players[1]
        innocent = players[2:]
        User_GUI.assign_roles("You got assigned as the murderer - Your job is to kill the other players at night without being caught.", "Murderer")
    elif determiner == 2:
        doctor = p1_name
        murderer = players[0]
        detective = players[1]
        innocent = players[2:]
        User_GUI.assign_roles("You got assigned as the doctor - Your job is to heal players that are about to be killed.", "Doctor")
    elif determiner == 3:
        detective = p1_name
        murderer = players[0]
        doctor = players[1]
        innocent = players[2:]
        User_GUI.assign_roles("You got assigned as the detective - Your job is to find out who the murderer is and arrest them.", "Detective")
    else:  
        murderer = players[0]
        doctor = players[1]
        detective = players[2]
        innocent = players[3:]
        User_GUI.assign_roles("You got assigned as an innocent - Your job is to survive and vote out who the murderer.", "Innocent")
    wait_for_response()
    
    while True:
        with open(r"data\mingle_data.json", "r") as f:
            script_data = json.load(f)
            mingle_data = script_data[0]
            prevote_data = script_data[1]
            murder_data = script_data[2]
            revote_data = script_data[3]
            sample_text = script_data[4]    
            interrogation = script_data[5]
        User_GUI.lights_out()
        
        if murderer == p1_name: #if player1 is the murderer:
            User_GUI.murderer_action(players, murder_data)
            wait_for_response()
            murdered_player = User_GUI.murdered_player
            if len(players) == 1:
                win_game()
                break
        else: #if player 1 is not the murderer
            if round_no <= 2:
                percentage_chance = 0
            else: #applicable on round 3 and after
                percentage_chance = (1 / len(players)) + (suspicion_points/100)
                if percentage_chance > 0.95:
                    percentage_change = 0.95
                elif percentage_chance < 0.05:
                    percentage_change = 0.05
            if random() < percentage_chance:
                User_GUI.murder_player1(murderer["Name"], murder_data)
                end_game()
                break
            else:
                murder_list = list.copy(players)
                murder_list.remove(murderer)
                shuffle(murder_list)
                murdered_player = murder_list.pop(0)
        
        is_doctor = True
        if doctor == p1_name: #if player1 is the doctor:
            User_GUI.doctor_action(players)
            wait_for_response()
            if User_GUI.option[-9:-1] == "yourself":
                saved_player = p1_name
            else:
                for player in players:
                    if player["Name"] == User_GUI.option:
                        saved_player = player
        elif doctor in players: #if player1 is not the doctor
            percentage_chance = (1 / (len(players) + 1)) + (-1*suspicion_points/100)
            if percentage_chance > 0.95:
                percentage_change = 0.95
            elif percentage_chance < 0.05:
                percentage_change = 0.05
            if random() < percentage_chance: #chance of being saved
                saved_player = {"Name" : p1_name}
            else:
                saved_player = choice(players)
        else: #if the doctor has been murdered
            saved_player = {"Name" : "Noone"}
            is_doctor = False
            
        is_detective = True
        if detective == p1_name: #if player1 is the detective:
            User_GUI.detective_action(players, authority_points)
            wait_for_response()
            suspicious_player = User_GUI.suspicious_player
            authority_points = User_GUI.authority_points
            suspicion_level = User_GUI.suspicion_level
            
        elif detective in players: #if player1 is not the detective
            suspicion_level = 0
            suspicion_determinter = 0.2*round_no
            if suspicion_determinter > 0.9:
                suspicion_determinter = 0.9
            if random() < suspicion_determinter: #if true, then the detective will make a statement
                if random() < 0.33:
                    suspicion_level = 2
                else:
                    suspicion_level = 1
            percentage_chance = (1 / (len(players) + 1)) + (suspicion_points/100)
            if percentage_chance > 0.95:
                percentage_change = 0.95
            elif percentage_chance < 0.05:
                percentage_change = 0.05
            if random() < percentage_chance: #chance of being selected as suspicious
                suspicious_player = {"Name" : p1_name}
            else:
                suspicious_players = list.copy(players)
                suspicious_players.remove(detective)
                suspicious_player = choice(suspicious_players)
                
        else: # if the detective has been killed
            suspicion_level, suspicious_player = 0, {"Name" : "Noone"}
            is_detective = False
            
        User_GUI.lights_out_continued(is_doctor, is_detective)
        wait_for_response()
        User_GUI.show_events(murdered_player, doctor, detective, saved_player, 
                             suspicion_level, suspicious_player, players)
        wait_for_response()
        players = User_GUI.players
        if len(players) < 2:
            User_GUI.show_votes_2("The are not enough people for a voting round.", "")
            wait_for_response()
            if murderer == p1_name:
                win_game()
            else:
                end_game()
            break
        if len(players) >= 4:
            User_GUI.prevote_chat(players, suspicion_points, prevote_data, discuss_topics, round_no)
        wait_for_response()
        suspicion_points = User_GUI.suspicion_points
        
        # Voting
        if murderer == p1_name:
            murderer = {"Name" : p1_name}
        voting_board, top_players = {}, {}
        for player in players:
            voting_board[player["Name"]] = 0
        voting_board[p1_name] = 0
        percentage_chance1 = (round_no*0.1) + (suspicion_points/100) #chance of someone voting you
        percentage_chance2 = (suspicion_level/100)*3 #chance of someone voting the suspicious player
        if suspicious_player["Name"] == p1_name:
            percentage_chance1 = percentage_chance2
        elif percentage_chance1 < 0.05:
            percentage_chance1 = 0.05
        elif percentage_chance1 > 0.95:
            percentage_chance1 = 0.95
        for player in players:
            if random() < percentage_chance1: #then vote for player 1
                voting_board[p1_name] += 1
            else:
                if random() < percentage_chance2: #then vote for the suspicious player
                    voting_board[suspicious_player["Name"]] += 1
                else:
                    determiner = randint(0, len(list(voting_board.keys()))-2)
                    voting_board[list(voting_board.keys())[determiner]] += 1
        
        voting_board = {k: v for k, v in sorted(voting_board.items(), reverse=True, key=lambda item: item[1])}
        User_GUI.show_votes_1(voting_board)
        wait_for_response()
        top_players = User_GUI.top_players
        # Revotes
        if len(top_players) == 1 and p1_name not in top_players: #if only 1 CPU is voted out
            User_GUI.revote_1(top_players, revote_data)
            wait_for_response()
            fate = User_GUI.vote.get()
            determiner = choice([1, 2, 3])
            if determiner == 1 or (determiner == 3 and fate == 1): #the player goes out
                for player in players:
                    if player["Name"] == top_players[0]:
                        players.remove(player)
                        User_GUI.update_players(players)
                if murderer["Name"] == top_players[0]:
                    User_GUI.show_votes_2(f"[Narrator]: The majority of the players have voted {top_players[0]} out.", f"You have successfully voted out the murderer!")
                    win_game()
                    break
                else:
                    User_GUI.show_votes_2(f"[Narrator]: The majority of the players have voted {top_players[0]} out.", f"{top_players[0]} was not the murderer.")
            elif determiner == 2 or (determiner == 3 and fate == 2): #the player stays
                User_GUI.show_votes_2(f"[Narrator]: The majority of the players have chosen to not vote {top_players[0]} out.", "")   
        
        elif len(top_players) > 1 and p1_name not in top_players: #if multiple CPU are voted out
            User_GUI.revote_2(top_players, revote_data)
            wait_for_response()
            fate = User_GUI.vote.get()
            if random() < 0.6: #random choice
                shuffle(top_players)
                voted_out = top_players.pop(0)
                for player in players: #removes player from list
                    if player["Name"] == voted_out:
                        players.remove(player)
                        User_GUI.update_players(players)
                if murderer["Name"] == voted_out:
                    User_GUI.show_votes_2("[Narrator]: The majority of the players have voted " + voted_out + " out.", "")
                    win_game()
                    break
                else:
                    User_GUI.show_votes_2("[Narrator]: The majority of the players have voted " + voted_out + " out.", voted_out + " was not the murderer.")
            else:
                if (((len(players)+1)-len(top_players)) % len(top_players) == 0) and random() < 0.1:
                    User_GUI.show_votes_2("[Narrator]: The votes were a tie, so no players will be voted out this round.", "")
                else:
                    voted_out = fate
                    for player in players: #removes player from list
                        if player["Name"] == voted_out:
                            players.remove(player)
                            User_GUI.update_players(players)
                    if murderer["Name"] == voted_out:
                        User_GUI.show_votes_2("[Narrator]: The majority of the players have voted " + voted_out + " out.", "")
                        win_game()
                        break
                    else:
                        User_GUI.show_votes_2("[Narrator]: The majority of the players have voted " + voted_out + " out.", voted_out + " was not the murderer.")
        elif len(top_players) == 1 and p1_name in top_players: #if player 1 is voted out
            User_GUI.revote_3(revote_data)
            wait_for_response()
            percentage_chance = (round_no*0.1) + (suspicion_points/100)
            if random() < percentage_chance:
                User_GUI.show_votes_2("The players are deciding your fate.", "[Narrator]: The majority of the players have voted " + p1_name + " out.")
                wait_for_response()
                end_game()
                break
            else:
                User_GUI.show_votes_2("The players are deciding your fate.", "The majority of the players have chosen to not vote " + p1_name + " out.")
        
        elif len(top_players) > 1 and p1_name in top_players: #if player 1 is voted out and at least 1 CPU
            User_GUI.revote_4(revote_data, top_players)
            wait_for_response()
            percentage_chance = (round_no*0.1) + (suspicion_points/100)
            if random() < percentage_chance:
                User_GUI.show_votes_2("The players are deciding your fate.", "[Narrator]: The majority of the players have voted " + p1_name + " out.")
                wait_for_response()
                end_game()
                break
            else:
                if (((len(players)+1)-len(top_players)) % len(top_players) == 0) and random() < 0.1:
                    User_GUI.show_votes_2("[Narrator]: The votes were a tie, so no players will be voted out this round.", "")
                else:
                    top_players.remove(p1_name)                  
                    voted_out = choice(top_players)
                    
                    for player in players: #removes player from list
                        if player["Name"] == voted_out:
                            players.remove(player)
                            User_GUI.update_players(players)
                    
                    if murderer["Name"] == voted_out:
                        User_GUI.show_votes_2("[Narrator]: The majority of the players have voted " + voted_out + " out.", "You have successfully voted out the murderer!")
                        wait_for_response()
                        win_game()
                        break
                    else:
                        User_GUI.show_votes_2("[Narrator]: The majority of the players have voted " + voted_out + " out.", voted_out + " was not the murderer.")           
        wait_for_response()
        User_GUI.free_time()
        wait_for_response()
        
        if murderer["Name"] == p1_name:
            murderer = p1_name
        
        determiner = randint(1,2) #Free time - Chat (Gain or lose points)
        if determiner == 1: #Suspicion check
            User_GUI.guess_the_name(players, suspicion_points)
        else: # Guess the fact
            User_GUI.guess_the_fact(players, suspicion_points, character_data)
        
        wait_for_response()
        suspicion_points = User_GUI.suspicion_points
        
        determiner = randint(1,40) #Free time - Challenge
        examine_players = False
        
        if 1 <= determiner <= 12: #30% chance of trivia question
            User_GUI.trivia_question(players, df, examine_players)
        elif 13 <= determiner <= 20: #20% chance of guessing shirt colours
            User_GUI.guess_the_shirt(players, character_data, examine_players)
        elif 21 <= determiner <= 25: #12.5% chance of rapid button presses
            User_GUI.speed_clicker(players, examine_players)
        elif 26 <= determiner <= 30: #12.5% chance of speed typing
            User_GUI.speed_typer(players, sample_text, examine_players)
        elif 31 <= determiner <= 35: #12.5% chance of time estimation
            User_GUI.time_estimation(players, examine_players)
        elif 36 <= determiner <= 40: #12.5% chance of reaction speed test
            User_GUI.reaction_test(players, examine_players)
            
        wait_for_response()
        examine_players = User_GUI.examine_players
        
        if examine_players == True:
            User_GUI.interrogation_role(players, interrogation, murderer, doctor, detective)
            
        wait_for_response()
            #Reduce suspicion points
        if suspicion_points < 10:
            suspicion_points += 5
        elif suspicion_points > 10:
            suspicion_points -= 5           
        User_GUI.update_suspicion_points(suspicion_points)
        
        round_no += 1
        User_GUI.update_round_number(round_no)
        

if __name__ == "__main__":
    welcome_window = Tk()
    welcome_window.title("Welcome")
    welcome_window.geometry("600x500+10+10")
    welcome_window.config(bg="black")
    welcome_window.iconbitmap("images/mafia_icon.ico")
    logo = PhotoImage(file="images/logo.gif")
    Label(welcome_window, image=logo, bg="black").grid(row=0, column=0, columnspan=2, pady=10, padx=80)
    d = {}
    for c in (65, 97):
        for i in range(26):
            d[chr(i+c)] = chr((i+13) % 26 + c)
    Label(welcome_window, text="".join([d.get(c, c) for c in s]), font="Ariel 14", bg="black", fg="white").grid(row=1, column=0, pady=10, columnspan=2)
    Label(welcome_window, text="Enter Name:", font="Ariel 18 bold", bg="black", fg="white").grid(row=2, column=0, pady=10)
    enter_name = Entry(welcome_window, font="Ariel 18 bold")
    enter_name.grid(row=2, column=1, pady=10)
    Button(welcome_window, text="Play Game", command=start_game, bg="gray35", fg="white", font="Ariel 16 bold").grid(row=3, column=0, columnspan=2, pady=(30, 5), ipadx=40)
    Button(welcome_window, text="View Rules", command=show_rules, bg="gray35", fg="white", font="Ariel 16 bold").grid(row=4, column=0, columnspan=2, pady=5, ipadx=40)
    Button(welcome_window, text="Quit", command=welcome_window.destroy, bg="gray35", fg="white", font="Ariel 16 bold").grid(row=5, column=0, columnspan=2, pady=5, ipadx=73)
    welcome_window.mainloop()

