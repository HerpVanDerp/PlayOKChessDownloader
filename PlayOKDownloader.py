import tkinter as tki
from bs4 import BeautifulSoup
import requests



def downloadGames():
    username = app.getUsername()
    links = []
    i = 1  # Seitenvariable
    findGames = True
    while findGames is True:
        app.root.update()
        site = 'https://www.playok.com/de/stat.phtml?gid=ch&uid=' + username + '&sk=2&page=' + str(i)
        page = requests.get(site)
        soup = BeautifulSoup(page.content, 'lxml')
        result = soup.find_all('span', class_='gr')
        if not result:
            findGames = False
            if i == 1:
                app.writeLog("ERROR: Could not find User!")
                return
        else:
            if i == 1:
                app.writeLog("Found user. Download games.")
            app.writeLog("Check page " + str(i))
            for res in result:
                href = res.find('a').attrs['href']
                links.append(href)
            i += 1
    pgn = []
    progress = 1
    for game in links:
        site = 'https://www.playok.com' + game
        game = requests.get(site)
        soup = BeautifulSoup(game.content, 'lxml')
        pgn.append(soup.get_text())
        app.writeLog(str(progress) + '/' + str(len(links)) + ' Games')
        app.root.update()
        progress += 1
    try:
        app.writeLog("Write to .pgn")
        f = open(username + '.pgn', 'w')
        app.root.update_idletasks()
        for game in pgn:
            f.write(str(game))
        f.close()
    except:
        app.writeLog("ERRROR: Could not write to .pgn!")
    app.writeLog("SUCCESS: " + username + '.pgn with ' + str(progress-1) + ' games created.')




class GUI(object):

    def __init__(self):
        self.root = tki.Tk()

        self.root.title("PlayOK Chess Downloader")

        #Frame
        frm = tki.Frame(self.root, width=600, height=300)
        frm.pack(fill="both", expand=True)
        frm.grid_propagate(True)
        frm.grid_rowconfigure(0, weight=0)
        frm.grid_rowconfigure(2, weight=1)
        frm.grid_columnconfigure(0, weight=1)

        #Input Username
        tki.Label(frm, text="Username:", font="none 12").grid(row=0, column=0, sticky="W")
        self.username = tki.Entry(frm, width=50)
        self.username.grid(row=0, column=1, sticky="W")

        #Get Button
        self.downloadButton = tki.Button(frm, text="Get Games", width=15, command=self.CallDownloader)
        self.downloadButton.grid(row=1, column=1, sticky="E")

        #Log Window
        self.log = tki.Text(frm, width=50, height=15, background="white", state='disabled', wrap="word")
        self.log.grid(row=2, column=0, columnspan=2, sticky=tki.N+tki.S+tki.E+tki.W)
        self.scroll_log = tki.Scrollbar(frm, command=self.log.yview)
        self.scroll_log.grid(row=2, column=2, sticky="nsew")
        self.log['yscrollcommand'] = self.scroll_log.set

        self.root.update()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())

    def writeLog(self, string):
        self.log.configure(state='normal')
        self.log.insert(tki.END, string + '\n')
        self.log.configure(state='disabled')
        self.log.yview(tki.END)

    def getUsername(self):
        return self.username.get()

    def CallDownloader(self):
        self.downloadButton.configure(state="disabled")
        downloadGames()
        self.downloadButton.configure(state='normal')

app = GUI()
app.root.mainloop()
