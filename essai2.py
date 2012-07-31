# -*- coding: iso-8859-1 -*-
 
import pycurl, Tkinter, sys, os, threading
 
class var:
    size = 0
    time = 0
    speed = 0
    TR_speed = 0
    status_HTTP = 0
 
class gui(threading.Thread):
    def __init__(self, root):
        threading.Thread.__init__(self)
    def run(self):
        try:
            download("headers")
            download("body")
        except:
            lab1.configure(text = "Impossible de se connecter au site ou au proxy")
            if os.path.isfile("C:/Python24/Freeze/body.txt"):
                os.remove("C:/Python24/Freeze/body.txt")
            if os.path.isfile("C:/Python24/Freeze/body.txt.old"):
                os.rename('C:/Python24/Freeze/body.txt.old', 'C:/Python24/Freeze/body.txt')
 
        if var.status_HTTP == 404:
            lab1.configure(text = "Téléchargement impossible : page non trouvée, veuillez verifier que l'adresse est correcte ou que le message est bien présent dans la boite aux lettres")
            lab2.destroy()
            os.remove('C:/Python24/Freeze/body.txt')
            if os.path.isfile("C:/Python24/Freeze/body.txt.old"):
                os.rename('C:/Python24/Freeze/body.txt.old', 'C:/Python24/Freeze/body.txt')
        if var.status_HTTP == 401:    
            lab1.configure(text = "Les logins de la messagerie sont incorrects")  
            lab2.destroy()
            os.remove('C:/Python24/Freeze/body.txt')
            if os.path.isfile("C:/Python24/Freeze/body.txt.old"):
                os.rename('C:/Python24/Freeze/body.txt.old', 'C:/Python24/Freeze/body.txt')
        elif var.status_HTTP == 200:
            Tkinter.Label(root, text = "Temps : " + str(var.time) + " sec").pack()
            Tkinter.Label(root, text = "Vitesse : %.2f Ko/s" % var.speed).pack()
            if os.path.isfile('body.txt.old'):
                os.remove('body.txt.old')
 
 
def download(action):
    url = "http://www.someserver.fr"
 
    f = open("body.txt", "wb")
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    #c.setopt(c.PROXYPORT, 8080)
    #c.setopt(c.PROXY, '10.0.0.30')
 
    if action == "headers":
        c.setopt(c.NOBODY, 1)
    elif action== "body":
        c.setopt(c.WRITEDATA, f)
        c.setopt(c.NOPROGRESS, 0)
        c.setopt(c.PROGRESSFUNCTION, progress)
 
    c.setopt(c.SSLVERSION, 3)
    c.setopt(c.SSL_VERIFYPEER, 0) 
    c.setopt(c.HTTPAUTH,c.HTTPAUTH_BASIC);
    c.setopt(c.USERPWD,"user:passwd"); 
    c.setopt(c.WRITEDATA, f)
    c.setopt(c.NOPROGRESS, 0)
    c.setopt(c.PROGRESSFUNCTION, progress)
    c.setopt(c.FOLLOWLOCATION, 1)
    c.setopt(c.MAXREDIRS, 5)
    c.setopt(c.OPT_FILETIME, 1)
    try:
        c.perform()
        if action == "headers":
            var.size = c.getinfo(c.CONTENT_LENGTH_DOWNLOAD)
        elif action == "body":
            var.time = c.getinfo(c.TOTAL_TIME)
            var.speed = c.getinfo(c.SPEED_DOWNLOAD)/1000
 
        var.status_HTTP = c.getinfo(c.HTTP_CODE)
    finally:
        c.close()
        f.close()
 
        #print "Total-time:", c.getinfo(c.TOTAL_TIME)
        #print "Download speed: %.2f bytes/second" % c.getinfo(c.SPEED_DOWNLOAD)
        #print "Document size: %d bytes" % c.getinfo(c.SIZE_DOWNLOAD)
 
## Callback function invoked when progress information is updated
def progress(download_t, download_d, upload_t, upload_d):
    if var.status_HTTP != 200:
        pass
    else:
        canevas.pack()
        canevas.coords(rect, 1, 1, int(download_d/var.size*100)*2.5, 40)
        canevas.itemconfig(pourcentage, text = str(int(download_d/var.size*100)) + '%')
        lab1.configure(text='%s' % int(download_d/1000) + "Ko sur " + str(int(var.size/1000)) + " Ko")
        lab2.configure(text='%s' % int((download_d-var.TR_speed)/1000) + " Ko/s")
 
        if var.size == download_d:
            canevas.configure(height=0, width=0)
            lab1.configure(text='Téléchargement terminé')
            lab2.configure(text = "Taille : %s Ko" % int(var.size/1000))
 
        var.TR_speed = download_d    
 
if __name__ == "__main__":
    if os.path.isfile('body.txt.old'):
        os.remove('body.txt.old');
    if os.path.isfile('body.txt'):
        os.rename('body.txt', 'body.txt.old')
 
    root = Tkinter.Tk()
 
    canevas = Tkinter.Canvas(root, height=40, width=250, bg="white")
    canevas.place(x=1, y=1)
    canevas.pack()
    canevas.pack_forget()
    rect = canevas.create_rectangle(1, 1, 0, 40, fill='red')
    pourcentage = canevas.create_text(125,20,text='')
 
    lab1 = Tkinter.Label(root, text = 'Début du téléchargement')
    lab1.pack()
    lab2 = Tkinter.Label(root, text = '')
    lab2.pack()
    ihm = gui(root)
    ihm.start()
    root.mainloop()
