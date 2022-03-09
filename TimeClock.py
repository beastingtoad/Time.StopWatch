'''
Deloper: James McHenry
Use for:ELE 408 -Extra credit
'''
import tkinter as tk
import time as Tm
import math
from tkinter.filedialog import asksaveasfile
hr24 = True
Start = True
pause = False
Reset = False
bg='#adc123'
timerL=0
timerS=0
laps=[]
SaveLaps=[]
BestLap=0
WorstLap=0
starttime=0
root = tk.Tk()
root.geometry("600x300")
root.title('Clock & StopWatch')
root.iconbitmap("stopwatch.ico")
root.overrideredirect(0)
ClockParts = tk.Frame(root,width=500, height=500)
lapInfo =  tk.Frame(root,width=500, height=100,bg='black')
oldlaps =  tk.Frame(root,width=160, height=100,bg='black')
lapsmiddle =  tk.Frame(root,width=160, height=100,bg='black')
TimerParts = tk.Frame(root,width=500, height=500,bg='black')

def clickStartButton()-> None:
    '''
    sets the text from the proper state and starts the timer or starts a new lap timer
    :return: None
    '''
    global Start,starttime,laps,pause,Reset,BestLap,WorstLap
    if Start and not pause:
        StartLapBut.config(text='Lap')
        StopBut.config(text='Stop')
        Reset = False
        Start = False
        starttime = Tm.time()
        laps.append(Tm.time())
    elif pause:
        Start = False
        pause = False
        StartLapBut.config(text='Lap')
        StopBut.config(text='Stop')
        Reset = False
    else:
        laps[len(laps)-1]=Tm.time()-laps[len(laps)-1]
        if (laps[len(laps)-1]<=BestLap or BestLap==0):
            BestLap=laps[len(laps)-1]
        if (laps[len(laps)-1]>=WorstLap):
            WorstLap=laps[len(laps) - 1]
        laps.append(Tm.time())
        oldLaps()

        
def clickStopButton()-> None:
    '''
    stops the timer when running or resets the timer if the timer is not 0

    :return: None
    '''
    global pause,Start,starttime,Reset,BestLap,WorstLap
    if not Start:
        pause = True
        Start = True
        StartLapBut.config(text='Start')
        StopBut.config(text='Reset')
    else:
        pause = False
        Reset = True
        Start = True
        StopBut.config(text='Stop')
        BestLap = 0
        WorstLap = 0

def BgColorUpdate()-> None:
    '''
    sets the Background color for all clock elements to a lighter color of blue the closer it is to 12:00(noon)

    :return: None
    '''
    global bg
    Rmax=79
    Gmax=167
    Bmax=255
    hour = Tm.strftime('%H')
    min =Tm.strftime('%M')
    min =int(min)
    hour=(int(hour)*60)
    total_Time= min+hour
    Deg_Sun=total_Time/8
    How_Sunny=math.sin(math.radians(Deg_Sun))
    bg = '#%02x%02x%02x' % (int(Rmax*How_Sunny), int(Gmax*How_Sunny), int(Bmax*How_Sunny))
    Date.config(bg = bg)
    root.config(bg = bg)
    Clock.config(bg = bg)
    ClockParts.config(bg=bg)
    root.after(60000, BgColorUpdate)

def convertTime(timein: float)->str:
    '''
    takes time in Sec and converts it to hr min sec and milisec

    :param timein: this is a float that is in secondes and shows milisecs in decimals

    :return: a string that is in the fromat of hr:min:sec:milisec
    '''
    curhr = str(int((int(timein) - (int(timein) % 3600)) / 3600))
    curmin = str(int(((int(timein) % 3600) - ((int(timein) % 3600) % 60)) / 60))
    cursec = str(int((int(timein) % 3600) % 60))
    curmil = str(int(((timein % 1) - (timein % 1) % .001) / .001))
    return(curhr.zfill(2) + ":" + curmin.zfill(2) + ":" + cursec.zfill(2) + "." + curmil.zfill(3))

def oldLaps():
    '''
    updates display with the last 3 lap times

    :return:
    '''
    global laps,WorstLap,BestLap
    OldLap1.config(text=convertTime(laps[len(laps)-2]) + " Lap: " + str(len(laps)-1))
    if(laps[len(laps)-2] == BestLap):
        OldLap1.config(fg='green')
    elif(laps[len(laps) - 2] == WorstLap):
        OldLap1.config(fg='red')
    else:
        OldLap1.config(fg='grey')
    if(len(laps)>2):
        OldLap2.config(text=convertTime(laps[len(laps) - 3]) + " Lap: " + str(len(laps) - 2))
        if (laps[len(laps) - 3] == BestLap):
            OldLap2.config(fg='green')
        elif (laps[len(laps) - 3] == WorstLap):
            OldLap2.config(fg='red')
        else:
            OldLap2.config(fg='grey')
    if (len(laps) > 3):
        updateLapsInfo()
        OldLap3.config(text=convertTime(laps[len(laps) - 4]) + " Lap: " + str(len(laps) - 3))
        if (laps[len(laps) - 4] == BestLap):
            OldLap3.config(fg='green')
        elif (laps[len(laps) - 4] == WorstLap):
            OldLap3.config(fg='red')
        else:
            OldLap3.config(fg='grey')


def LapTimeUpdate()-> None:
    '''
    controls the updating  of the lap timer with the current state and then calls to StopWatchUpdate every 1 ms

    :return: None
    '''
    global starttime,Start,pause,timerL,Reset,laps,pop,BestLap,WorstLap
    if Start and not pause and not Reset:
        currenttime=0

    else:
        currenttime = Tm.time()
        if not Reset:
            pop = False
    if(len(laps)>0):
        if pause:
            laps[len(laps) - 1] = (currenttime -  timerL)
        timerL = (currenttime - laps[len(laps)-1])
        Lap.config(text=convertTime(timerL)+" Lap: "+str(len(laps)))
        if(BestLap!=0):
            if(timerL<=BestLap):
                Lap.config(fg='Green')
            if (timerL >= WorstLap):
                Lap.config(fg='Red')
            if(timerL>BestLap and timerL < WorstLap):
                Lap.config(fg='yellow')
    if Reset:
        if (len(laps)>1 and not pop):
            laps[len(laps) - 1] = timerL
            Prompt(laps)
            restText()
            laps = []
            pop = True
        else:
            restText()
            laps = []
    Lap.after(1,StopWatchUpdate)

def updateLapsInfo():
    '''
    This is going to update best lap worst lap and avg lap on the window

    :return:
    '''
    global WorstLap,BestLap,laps
    BLap.config(text="Best Lap Time: "+ convertTime(BestLap))
    WLap.config(text="Wosrt Lap Time: "+convertTime(WorstLap))
    total=0
    for x in range(0, len(laps)-1):
        total+=laps[x]
    avg=(total/(len(laps)-1))
    ALap.config(text="Average Lap Time: "+convertTime(avg))


def restText():
    '''
    To update all info about laps to blank

    :return:
    '''
    Lap.config(text="")
    OldLap1.config(text="")
    OldLap2.config(text="")
    OldLap3.config(text="")
    BLap.config(text="")
    WLap.config(text="")
    ALap.config(text="")

def Prompt(lapdata: list)->None:
    '''
    This makes a window to ask the user if they want to save there lap data

    :return: None
    '''
    global SaveLaps
    SaveLaps = lapdata
    def yes():
        global SaveLaps
        laps = SaveLaps
        data = [('All tyes(*.*)', '*.*'),('.csv', '*.csv*')]
        f = asksaveasfile(mode='w', defaultextension='.csv',filetypes=data)
        f.writelines("Time , Lap number"+ '\n')
        if f is not None:
            for x in range(0, len(laps)):
                f.writelines(convertTime(laps[x])+","+str(x+1)+'\n')
            f.close()
        SaveLaps = []
        Prompt.destroy()
    def no():
        global SaveLaps
        SaveLaps=[]
        Prompt.destroy()
    Prompt = tk.Tk()
    Prompt.title('Save Laps')
    Prompt.iconbitmap("stopwatch.ico")
    Prompt.geometry("200x200")
    Prompt.config(bg='white')
    PromptText = tk.Label(Prompt, font=('8514oem', 10, 'bold'), wraplength='200', text="Save Lap times?", fg='black',
                          bg='white')
    yesbut = tk.Button(Prompt, font = ('8514oem', 10, 'bold'),text="Yes", command=yes,bg='grey',width=10)
    nobut = tk.Button(Prompt, font=('8514oem', 10, 'bold'), text="No", command=(no), bg='grey', width=10)
    PromptText.pack(anchor='center', pady='50')
    yesbut.pack(side='right',anchor='se')
    nobut.pack(side='left',anchor='sw')

def StopWatchUpdate()-> None:
    '''
    controls the updating  of the stopwatch timer with the current state and then calls to LapTimeUpdate every 1 ms

    :return: None
    '''
    global starttime,Start,timerS,Reset
    if Start and not pause:
        currenttime=0
    else:
        currenttime = Tm.time()
    if pause:
        starttime =(currenttime - timerS)
    if Reset:
        starttime = currenttime
    timerS = (currenttime - starttime)
    StopWatch.config(text=convertTime(timerS))
    StopWatch.after(1,LapTimeUpdate)

def Dateupdate()-> None:
    '''
    Pulls Todays date and displayes it

    :return: None
    '''
    string = Tm.strftime('%m/%d/%Y')
    Date.config(text = "Todays Date :"+string)
    Date.after(1000, Dateupdate)
def Clockupdate()-> None:
    '''
    figures out if we want 24hr or 12 display then grabs the time every 1s.

    :return: None
    '''
    global hr24
    if hr24 == True:
        string = Tm.strftime('%H:%M:%S')
    else:
        string = Tm.strftime('%I:%M:%S %p')
    Clock.config(text = string)
    Clock.after(1000, Clockupdate)
def switch()-> None:
    '''
    this is called when the button in the top right is pressed this chages a global varible that tells if to display 24 or 12 hr time.

    :return: None
    '''
    global hr24
    if hr24:
        hr24button.config(text = '12hr')
        hr24 = False
    else:
        hr24button.config(text = '24hr')
        hr24 = True

def Mainloop():
    '''
    used to run all the windows in tk loop and to pack all frames in the correct order
    '''
    ClockParts.pack(side='top', fill='x')
    TimerParts.pack(side='bottom', fill='x')
    lapInfo.pack(side='bottom', fill='x')
    hr24button.pack(in_=ClockParts, side='right', anchor='ne')
    Date.pack(in_=ClockParts, side='top', anchor='center')
    Clock.pack(in_=ClockParts, side='top', anchor='center')
    StopBut.pack(in_=TimerParts, side='right', anchor='se', fill='y', padx='1')
    StartLapBut.pack(in_=TimerParts, side='right', anchor='sw', fill='y', padx='1')
    Lap.pack(in_=TimerParts, side='top')
    StopWatch.pack(in_=TimerParts, side='top')
    oldlaps.pack(in_=lapInfo, side='right')
    lapsmiddle.pack(in_=lapInfo, side='right', padx='25')
    OldLap1.pack(in_=oldlaps, side='top')
    OldLap2.pack(in_=oldlaps, side='top')
    OldLap3.pack(in_=oldlaps, side='top')
    BLap.pack(in_=lapsmiddle, side='top')
    WLap.pack(in_=lapsmiddle, side='top')
    ALap.pack(in_=lapsmiddle, side='top')
    Clockupdate()
    Dateupdate()
    BgColorUpdate()
    StopWatchUpdate()
    LapTimeUpdate()
    tk.mainloop()

Date = tk.Label(root, font = ('8514oem', 20, 'bold'),bd=0,fg = 'white')
Clock = tk.Label(root, font = ('8514oem', 40, 'bold'),bd=0,fg = 'white')
hr24button = tk.Button(root,font = ('8514oem', 20, 'bold'), text = '24hr', bd = 1,command = switch,bg='grey')

OldLap1= tk.Label(root, font = ('8514oem', 8, 'bold'),bd=0,fg = 'grey',bg='black')
OldLap2= tk.Label(root, font = ('8514oem', 8, 'bold'),bd=0,fg = 'grey',bg='black')
OldLap3= tk.Label(root, font = ('8514oem', 8, 'bold'),bd=0,fg = 'grey',bg='black')

BLap = tk.Label(root, font = ('8514oem', 10, 'bold'),bd=0,fg = 'green',bg='black')
WLap = tk.Label(root, font = ('8514oem', 10, 'bold'),bd=0,fg = 'red',bg='black')
ALap = tk.Label(root, font = ('8514oem', 10, 'bold'),bd=0,fg = 'yellow',bg='black')

Lap = tk.Label(root, font = ('8514oem', 10, 'bold'),bd=0,fg = 'grey',bg='black')
StopWatch = tk.Label(root, font = ('8514oem', 35, 'bold'),bd=0,fg = 'white',bg='black')
StartLapBut = tk.Button(root, font = ('8514oem', 10, 'bold'),text="Start", command=clickStartButton,bg='grey',width=10)
StopBut = tk.Button(root, font = ('8514oem', 10, 'bold'),text="Stop", command=clickStopButton,bg='grey',width=10)
if __name__ == '__main__':
    try:
        Mainloop()
    except KeyboardInterrupt:
        pass
