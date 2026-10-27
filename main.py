from tkinter import *
from tkinter.font import Font
import json
from os.path import exists
from os import remove
from random import randrange
from time import sleep
from os import system
from os import getcwd

print("\n###################################################################")
print("#  _   _ _ _ _       _____        __ _                            #")
print("# | \\ | (_|_) |     / ____|      / _| |                           #")
print("# |  \\| |_ _| | __ | (___   ___ | |_| |___      ____ _ _ __ ___   #")
print("# | . ` | | | |/ /  \\___ \\ / _ \\|  _| __\\ \\ /\\ / / _` | '__/ _ \\  #")
print("# | |\\  | | |   <   ____) | (_) | | | |_ \ V  V / (_| | | |  __/  #")
print("# |_| \\_|_|_|_|\\_\ |_____/ \\___/|_|  \\__| \\_/\\_/ \\__,_|_|  \\___|  #")
print("#                                                                 #")
print("###################################################################\n")

# onnea lukemiseen mä lopetin kommentoinnin puolessa välissä

audio_enabled=True
try:
    from playsound3 import playsound
except ImportError:
    print("Huom! playsound3 ei ole asennettu. Asenna nyt? [k/e]")
    print("https://pypi.org/project/playsound3/")
          
    if input()=="k":
        system("pip install playsound3")
        try:
            from playsound3 import playsound
            print("Asennus onnistui!. Jatketaan")
        except:
            print("Asennus epäonnistui\nJatketaan ilman ääniä")
            audio_enabled=False
            sleep(2)
    else:
        print("Jatketaan ilman ääniä")
        audio_enabled=False
        sleep(2)

print("T4 Hedelmäpeli v1.0")
print("By: Niik Software | https://niiksoftware.com")

def close():
    global running
    running=False
    root.destroy()

def insert_coin(ev):
    global v_money
    global v_m_money
    global t_money
    global t_m_money
    if v_money>0:
        if v_audio: playsound(getcwd()+"/res/coin_insert.wav",block=False)
        v_money-=1
        v_m_money+=1
        t_money.config(text=f"Rahaa: {v_money}")
        t_m_money.config(text=str(v_m_money))

def win(amount):
    global v_m_money
    global v_wins
    global t_m_money
    global t_m_wins

    v_m_money+=amount
    v_wins+=amount
    t_m_money.config(text=v_m_money)
    t_m_wins.config(text=v_wins)


def save():
    global v_wins
    global v_money
    with open("save.json","w") as f:
        f.write("{"+f'"money":{v_money},"winnings":{v_wins},"audio":{str(v_audio).lower()}'+"}")

def lever(ev):
    global b_lever
    global v_m_money
    global t_m_money
    global v_spinning

    global v_slot1_y_remain
    global v_slot2_y_remain
    global v_slot3_y_remain

    global v_lock_1
    global v_lock_2
    global v_lock_3

    global v_audio

    if v_m_money>0 and not v_spinning:
        if v_audio: playsound(getcwd()+"/res/crank.wav",block=False)
        v_m_money-=1
        v_spinning=True
        b_lever.config(image=img_lever_on)
        t_m_money.config(text=str(v_m_money))

        # 20-40 on montako ruutua menee alaspäin, 100 on ruudun pituus
        # ruudut menee yhden pixelin alas tickillä ja v_slotX_y_remain on montako pixeliä menee alas
        if not v_lock_1:
            v_slot1_y_remain=randrange(20,40)*100
        if not v_lock_2:
            v_slot2_y_remain=randrange(20,40)*100
        if not v_lock_3:
            v_slot3_y_remain=randrange(20,40)*100

def payout():
    global b_payout
    global v_m_money
    global v_money

    global t_m_money
    global t_money
    global v_spinning
    if b_payout["background"]==col_payout_on and not v_spinning:

        if v_audio: 
            playsound(getcwd()+"/res/switch.wav",block=False)
            playsound(getcwd()+"/res/coins.wav",block=False)
        b_payout.config(bg=col_payout_off)
        v_money+=v_m_money
        v_m_money=0
        t_m_money.config(text=str(v_m_money))
        t_money.config(text=f"Rahaa: {v_money}")

        save()

def restart_game(ev):
    global v_money
    global v_wins
    global f_gameover
    global t_money
    global t_m_wins

    v_money=10
    v_wins=0
    f_gameover.place(x=0,y=-10000)
    t_money.config(text=f"Rahaa: {v_money}")
    t_m_wins.config(text=str(v_wins))
    
    save()

def keypress(ev):
    global running
    if ev.keycode==81:   # Q
        running=False
    elif ev.keycode==49: # 1
        lock(1)
    elif ev.keycode==50: # 2
        lock(2)
    elif ev.keycode==51: # 3
        lock(3)
    elif ev.keycode==32: # Space
        payout()
    elif ev.keycode==8: # Backspace
        insert_coin(None)
    elif ev.keycode==13: # Enter
        lever(None)

def toggle_audio(ev):
    global v_audio
    global b_audio
    global as_music

    if v_audio:
        b_audio.config(image=img_audio_off)
        v_audio=False
        as_music.stop()
    else:
        b_audio.config(image=img_audio_on)
        v_audio=True
        as_music=playsound(getcwd()+"/res/music.wav",block=False)
    save()

def lock(slot):
    global v_can_lock
    global b_lock_1
    global b_lock_2
    global b_lock_3

    global v_lock_1
    global v_lock_2
    global v_lock_3
    global v_spinning

    if v_can_lock and not v_spinning:
        if slot==0:
            b_lock_1.config(bg=col_lock_off)
            v_lock_1=False
            b_lock_2.config(bg=col_lock_off)
            v_lock_2=False
            b_lock_3.config(bg=col_lock_off)
            v_lock_3=False
            v_can_lock=False
        elif slot==1:
            if v_audio: playsound(getcwd()+"/res/switch.wav",block=False)
            if v_lock_1:
                b_lock_1.config(bg=col_lock_off) 
                v_lock_1=False
            else:
                b_lock_1.config(bg=col_lock_on)
                v_lock_1=True
        elif slot==2:
            if v_audio: playsound(getcwd()+"/res/switch.wav",block=False)
            if v_lock_2:
                b_lock_2.config(bg=col_lock_off) 
                v_lock_2=False
            else:
                b_lock_2.config(bg=col_lock_on)
                v_lock_2=True
        elif slot==3:
            if v_audio: playsound(getcwd()+"/res/switch.wav",block=False)
            if v_lock_3:
                b_lock_3.config(bg=col_lock_off) 
                v_lock_3=False
            else:
                b_lock_3.config(bg=col_lock_on)
                v_lock_3=True

col_bg="#570e1c"
col_lock_off="#6B0000"
col_lock_on="#ff0000"
col_payout_off="#692700"
col_payout_on="#f75b01"
v_money=0 # Variable Money
v_m_money=0 # Machine Money
v_wins=0 # Winnings
v_audio=True

v_spinning=False # Machine spinning
v_can_lock=False
v_lock_1=False
v_lock_2=False
v_lock_3=False

root = Tk()
root.title("T4 Hedelmäpeli")
root.geometry("854x480")
root.configure(background="#570e1c")
root.protocol("WM_DELETE_WINDOW", close)
root.bind("<Key>", keypress)
root.resizable(width=False, height=False)

# Ensimmäinen käynnistys
if not exists("save.json"):
    with open("save.json","w") as f:
        f.write('{"money":10,"winnings":0,"audio":true}')

# Lataa tiedot
with open("save.json") as f:
    try:
        _=json.loads(f.read())
        v_money=_["money"]
        v_wins=_["winnings"]
        v_audio=_["audio"]
        if v_money==0:
            v_money=10
            v_wins=0
    except:
        print("Tallennuksen lataus epäonnistui!")
        sleep(2)
        v_money=10
        v_wins=0
        v_audio=audio_enabled
if not audio_enabled: v_audio=False



if v_audio:
    as_music=playsound(getcwd()+"/res/music.wav",block=False)


# Lataa kuvat
img_logo=PhotoImage(file=r"res/logo.png")
img_coin_slot=PhotoImage(file=r"res/coinslot.png")
img_lever_off=PhotoImage(file=r"res/lever_off.png")
img_lever_on=PhotoImage(file=r"res/lever_on.png")
img_slots=PhotoImage(file=r"res/slots.png")
img_lock=PhotoImage(file=r"res/lock_button.png")
img_payout=PhotoImage(file=r"res/payout_button.png")
img_scores=PhotoImage(file=r"res/scores.png")
img_audio_off=PhotoImage(file=r"res/audio_off.png")
img_audio_on=PhotoImage(file=r"res/audio_on.png")

# Fontit
font_courier=Font(family="Courier New",size=16,weight="bold")


# Logo
_=Label(root,borderwidth=0,bg=col_bg,image=img_logo,highlightthickness=0) 
_.place(x=10,y=10)

# Ääni nappi
if audio_enabled:
    if v_audio:
        b_audio=Button(root,borderwidth=0,bg=col_bg,image=img_audio_on,highlightthickness=0,cursor="hand2",activebackground=col_bg) 
    else:
        b_audio=Button(root,borderwidth=0,bg=col_bg,image=img_audio_off,highlightthickness=0,cursor="hand2",activebackground=col_bg) 
    b_audio.place(x=447,y=10)
    b_audio.bind("<ButtonPress>", toggle_audio)

# Kolikko reikä
b_coinslot=Button(root,borderwidth=0,bg=col_bg,image=img_coin_slot,highlightthickness=0,cursor="hand2",activebackground=col_bg) 
b_coinslot.place(x=740,y=10)
b_coinslot.bind("<ButtonPress>", insert_coin)

# Rullat
_=Frame(root,bg="#000000",width=368,height=254)
_.place(x=245,y=120)
f_slots=Canvas(root,bg="#000000",width=364,height=250,borderwidth=0,highlightthickness=0)
f_slots.place(x=247,y=122)

f_slot1=f_slots.create_image((60,-25),image=img_slots)
f_slot2=f_slots.create_image((182,-25),image=img_slots)
f_slot3=f_slots.create_image((304,-25),image=img_slots)

# Peli loppu ikkuna
f_gameover=Frame(root,bg="#270000",width=364,height=250)
#f_gameover.place(x=247,y=122)
f_gameover.pack_propagate(False)
_=Label(f_gameover,bg="#270000",fg="#ffffff",text="Rahat loppu",font=font_courier)
_.pack(pady=15, padx=0,anchor=N)
_=Button(f_gameover,bg="#ffffff",highlightthickness=0,height=2,width=20,borderwidth=0,text="Aloita alusta",cursor="hand2",activebackground="#dddddd")
_.pack(pady=50, padx=0,anchor=N)
_.bind("<ButtonPress>", restart_game)


# Lukitse napit
b_lock_1=Button(root,bg=col_lock_off,highlightthickness=0,borderwidth=0,cursor="hand2",image=img_lock,activebackground=col_lock_off,command=lambda: lock(1))
b_lock_1.place(x=255,y=400)

b_lock_2=Button(root,bg=col_lock_off,highlightthickness=0,borderwidth=0,cursor="hand2",image=img_lock,activebackground=col_lock_off,command=lambda: lock(2))
b_lock_2.place(x=379,y=400)

b_lock_3=Button(root,bg=col_lock_off,highlightthickness=0,borderwidth=0,cursor="hand2",image=img_lock,activebackground=col_lock_off,command=lambda: lock(3))
b_lock_3.place(x=503,y=400)

# Voiton Maksu
b_payout=Button(root,bg=col_payout_off,highlightthickness=0,borderwidth=0,cursor="hand2",image=img_payout,activebackground=col_payout_off,command=lambda: payout())
b_payout.place(x=740,y=400)


# Vipu
b_lever=Button(root,borderwidth=0,bg=col_bg,image=img_lever_off,highlightthickness=0,cursor="hand2",activebackground=col_bg) 
b_lever.place(x=740,y=120)
b_lever.bind("<ButtonPress>", lever)


# Piste ohje
_=Label(root,borderwidth=0,bg=col_bg,image=img_scores,highlightthickness=0) 
_.place(x=10,y=142)

# Piste ruutu
f_score=Frame(root,bg="#000000",width=224,height=106)
f_score.place(x=10,y=364)


# Peliraha
_=Frame(f_score,bg="#1a130b",width=130,height=50)
_.place(x=2,y=2)
_=Label(_,bg="#1a130b",text=f"Peliraha",fg="#ffbb00",font=font_courier)
_.place(x=10,y=10)

_=Frame(f_score,bg="#1a130b",width=88,height=50)
_.place(x=134,y=2)
t_m_money=Label(_,bg="#1a130b",text=f"{v_m_money}",fg="#ffbb00",font=font_courier)
t_m_money.place(x=10,y=10)

# Voitot
_=Frame(f_score,bg="#1a130b",width=130,height=50)
_.place(x=2,y=54)
_=Label(_,bg="#1a130b",text=f"Voitot",fg="#ffbb00",font=font_courier)
_.place(x=10,y=10)

_=Frame(f_score,bg="#1a130b",width=88,height=50)
_.place(x=134,y=54)
t_m_wins=Label(_,bg="#1a130b",text=f"{v_wins}",fg="#ffbb00",font=font_courier)
t_m_wins.place(x=10,y=10)



# Rahat teksti
t_money=Label(root,bg=col_bg,text=f"Rahaa: {v_money}",fg="#ffffff",font=font_courier)
t_money.pack(pady=15, padx=123,side=RIGHT,anchor=NE)


# Rullien pyörimis muuttujat
v_slot1_y=-425
v_slot2_y=-425
v_slot3_y=-425

v_slot1_y_remain=0
v_slot2_y_remain=0
v_slot3_y_remain=0


running=True
while running:

    if v_audio:
        if not as_music.is_alive(): as_music=playsound(getcwd()+"/res/music.wav",block=False)

    if v_spinning:
        if v_slot1_y_remain>0:
            v_slot1_y_remain-=1
            v_slot1_y+=1
            f_slots.move(1,0,1)
        if v_slot2_y_remain>0:
            v_slot2_y_remain-=1
            v_slot2_y+=1
            f_slots.move(2,0,1)
        if v_slot3_y_remain>0:
            v_slot3_y_remain-=1
            v_slot3_y+=1
            f_slots.move(3,0,1)

        if v_audio:
            if v_slot1_y_remain==0:
                playsound(getcwd()+"/res/slot.wav",block=False)
                v_slot1_y_remain=-1
            if v_slot2_y_remain==0:
                playsound(getcwd()+"/res/slot.wav",block=False)
                v_slot2_y_remain=-1
            if v_slot3_y_remain==0:
                playsound(getcwd()+"/res/slot.wav",block=False)
                v_slot3_y_remain=-1


        if v_slot1_y==0:
            v_slot1_y=-500
            f_slots.move(1,0,-500)
        if v_slot2_y==0:
            v_slot2_y=-500
            f_slots.move(2,0,-500)
        if v_slot3_y==0:
            v_slot3_y=-500
            f_slots.move(3,0,-500)

        if v_slot1_y_remain<=0 and v_slot2_y_remain<=0 and v_slot3_y_remain<=0:
            v_spinning=False
            b_lever.config(image=img_lever_off)

            # Prosessoi voitot
            if v_slot1_y==v_slot2_y and v_slot1_y==v_slot3_y: # Kolme samaa
                if v_slot1_y  ==-325: win(5)  # Kirsikka
                elif v_slot1_y==-425: win(10) # Sitruuna
                elif v_slot1_y==-225: win(15) # Päärynä
                elif v_slot1_y==-25:  win(20) # Melooni
                elif v_slot1_y==-125: win(50) # Seiska
                lock(0)
                if v_m_money>0:
                    b_payout.config(bg=col_payout_on)

                if v_audio: playsound(getcwd()+"/res/big_win.wav",block=False)

            elif v_slot1_y==-125 or v_slot3_y==-125: # Ensimmäinen tai viimeinen on 7
                win(2)
                lock(0)
                if v_m_money>0:
                    b_payout.config(bg=col_payout_on)

                if v_audio: playsound(getcwd()+"/res/small_win.wav",block=False)
            elif v_can_lock:
                if v_lock_1 or v_lock_2 or v_lock_3:
                    lock(0)
            else:
                v_can_lock=True

            
            if v_m_money==0:
                b_payout.config(bg=col_payout_off)
            save()
            if v_m_money==0 and v_money==0:
                sleep(1) # Anna aikaa nähdä mikä tulos
                f_gameover.place(x=247,y=122)
                with open("save.json","w") as f:
                        f.write('{"money":10,"winnings":0,"audio":'+str(v_audio).lower()+'}')



                



    try:
        root.update()
    except:
        break
print("Kiitos kun pelasit!")