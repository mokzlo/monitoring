# -*- coding: utf-8 -*-
import urllib
import re
import string

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
###Fill variables
fromaddr = "[From_mail]"
pass_email = "[Pass_from_mail]"
smtp_server = "[serveur_SMTP_Foom_Email]"

toaddr = "[To_mail]"
subject = "[Subject of the email alert]"
url_base = "[URL_to_check]"
###

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = subject


lien = 0
tablo_error = []

class Recherche :

    "sortir un tableau d'une page html"
    def __init__(self, masque='', page=''):
        self.masque = masque
        self.page = page

    def sortir_tablo(self):
        regexp = re.compile(self.masque,re.I | re.S)
        tablo = regexp.findall(self.page)
        return tablo


page_depart = urllib.urlopen(url_base).read()


###Tweak the links and images who need to monitor
#instagram links
masque_liens_instagram = '<a class="instagram" href="(.*?)" target="_blank">'
liens_instagram = Recherche(masque_liens_instagram, page_depart)
tablo_liens = liens_instagram.sortir_tablo()
#instagram images
masque_image_instagram = '<img src="https://scontent.cdninstagram.com/(.*?)"'
image_instagram = Recherche(masque_image_instagram, page_depart)
tablo_image_instagram = image_instagram.sortir_tablo()
for images in tablo_image_instagram :
    tablo_liens.append("https://scontent.cdninstagram.com/"+images)              

#facebook links
masque_liens_facebook = '<a class="facebook" href="(.*?)" target="_blank">'
liens_facebook = Recherche(masque_liens_facebook, page_depart)
tablo_liens.extend(liens_facebook.sortir_tablo())
#facebook images
masque_image_facebook = '<img src="https://scontent.xx.fbcdn.net/(.*?)"'
image_facebook = Recherche(masque_image_facebook, page_depart)
tablo_image_facebook = image_facebook.sortir_tablo()
for images in tablo_image_facebook :
    tablo_liens.append("https://scontent.xx.fbcdn.net/"+images) 
#facebookArch images 
masque_image_facebookArch = '<img src="https://scontent-cdg2-1.xx.fbcdn.net/(.*?)"'
image_facebook = Recherche(masque_image_facebookArch, page_depart)
tablo_image_facebook = image_facebook.sortir_tablo()
for images in tablo_image_facebook :
    tablo_liens.append("https://scontent-cdg2-1.xx.fbcdn.net/"+images) 
#facebook video
masque_video_facebook = '<img src="https://video.xx.fbcdn.net/(.*?)"'
video_facebook = Recherche(masque_video_facebook, page_depart)
tablo_video_facebook = video_facebook.sortir_tablo()
for videos in tablo_video_facebook :
    tablo_error.append("https://video.xx.fbcdn.net/"+videos) 


while lien < len(tablo_liens):
    reponse_urlexterne = urllib.urlopen(tablo_liens[lien]).getcode()
    
    if(reponse_urlexterne != 200):
        tablo_liens[lien]
        tablo_error.append(tablo_liens[lien])
    lien = lien + 1

if len(tablo_error) > 0 :
    erreur = 0
    body = ""
    while erreur < len(tablo_error):
        body = body + tablo_error[erreur]+"\n"
        erreur = erreur + 1
    msg.attach(MIMEText(body, 'plain'))
else :
    msg.attach(MIMEText(url_base+" as no external dead link", 'plain'))
                             
server = smtplib.SMTP(smtp_server, 587)
server.starttls()
server.login(fromaddr, pass_email)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
