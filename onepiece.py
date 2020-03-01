import requests
from bs4 import BeautifulSoup
import re
import os
import smtplib
from email.mime.text import MIMEText
import time

url = 'https://dytt8.net/html/dongman/new/20150111/47110.html'

mail_addr = 'woodhfut@hotmail.com'
pswd = os.environ['MAIL_PASSWORD']

#TODO: using winreg to get the thunder path? 
thunder_path = r'C:\Program Files (x86)\Thunder Network\Thunder\Program\ThunderStart.exe'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}
s = requests.Session()
r = s.get(url,headers =headers)
#print(r.headers.get('content-type'))

if r.encoding =='ISO-8859-1' and not 'ISO-8859-1' in r.headers.get('Content-Type',''):
    r.encoding = r.apparent_encoding
    print(r.encoding)
#r.encoding = None
#print(r.text)
bs = BeautifulSoup(r.text,'html.parser')

links = bs.find_all('a',text=re.compile(r'ftp:.+海贼王.+\.[mp4|rmvb]'))

if not links:
    print('failed to get download page links, exit.')
    exit()

print(links[-1])


# with open('onepiece.txt','w',encoding='utf-8') as dl:
#     for link in links:
#         print(link.get_text())
#         dl.write(link.get_text()+'\r\n')

download = []
with open('onepiece.txt','r',encoding='utf-8') as dl:
    dlst = dl.read()
    links.reverse()
    for link in links:
        
        if link.get_text() not in dlst:
            print('{} has not been downloaded, start to download it.'.format(link.get_text()))
            
            cmd = '"{}" -startType:DesktopIcon "{}"'.format(thunder_path,link.get_text())
            #print('cmd {}'.format(cmd))
            r = os.system('"{}"'.format(cmd))
            if r == 0:
                download.append(link.get_text())
            else:
                print('error {} occurred.'.format(r))
            #when multiple episodes exists, sometimes ThunderStart hangs or not able to handle new download request
            time.sleep(5)    
        else:
            #print('{} has already been downloaded, ignore.'.format(link.get_text()))
            break

if len(download) > 0:
    body = ''
    with open('onepiece.txt','a', encoding='utf-8') as dl:
        if(len(download)>1):
            download.reverse()
        for itm in download:
            dl.write(itm+'\r\n')
            body += itm + '\n'
    
    #send email to notify me. 
    
    conn = smtplib.SMTP('smtp.live.com',587)
    conn.ehlo()
    conn.starttls()
    conn.ehlo()
    conn.login(mail_addr,pswd)
    msg = MIMEText(_text=body,_subtype='plain',_charset='utf-8')
    msg['Subject'] = 'new one piece is ready.'
    msg['To'] = mail_addr#';'.join(usr_to)
    msg['From'] = mail_addr

    conn.sendmail(mail_addr,mail_addr,msg.as_string())
    conn.quit()
    
else:
    print('all has been downloaded.')
