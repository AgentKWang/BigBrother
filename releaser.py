'''
Created on Jan 30, 2015

@author: kehan_wang
'''
import imaplib
import smtplib
import re
import datetime
import threading
import sys

class releaser:
    RELEASE_MSG = "Release"
    debug = False
    CHECK_FREQUENCE = 600
    WHITE_LIST_UPDATE_FREQUENCE = 7200
    def __init__(self, account, pswd, imap_server, smtp_server):
        self.account = account
        self.pswd = pswd
        self.imap_server = imap_server
        self.smtp_server = smtp_server
        self.getwhitelist()
        
    def getwhitelist(self):
        try:
            wf = open("white_list.txt")
            self.whitelist = wf.read().splitlines()
            wf.close()
        except:
            self.whitelist = []
            self.log("Read White List File Error: " + sys.exc_info()[0])
        if self.debug:
            print self.whitelist
        
    def checknewemail(self):
        num_released = 0
        self.log("Starting Checking Emails...")
        i_s = imaplib.IMAP4(self.imap_server)
        i_s.login(self.account, self.pswd)
        rt_code, rt_data = i_s.select()
        if re.findall(rt_code, "OK", re.I) is not None: new_email_num = rt_data[0]
        else: 
            self.log("Error during mailbox selection" + rt_code)
            return
        for mail_no in range(int(new_email_num), 0, -1):
            rt_code, raw_email = i_s.fetch(mail_no, "(FLAGS RFC822.HEADER.LINES (From) RFC822.HEADER.LINES (reply-to) RFC822.HEADER.LINES (subject) RFC822.HEADER.LINES (date))")
            if self.debug: print raw_email
            e_flags = raw_email[0][0]
            if len(re.findall("seen", e_flags, re.IGNORECASE))>0: continue
            e_sender = re.findall("from:\s*(.*)\r?\n", raw_email[0][1], re.IGNORECASE)
            e_readdr = re.findall("reply-to:\s*(.*)\r?\n", raw_email[0][1], re.IGNORECASE)
            if len(e_sender)>0 and len(e_readdr)>0: 
                e_sender = e_sender[0]
                e_readdr = e_readdr[0]
                print e_sender
                print e_readdr
            else: continue
            for sender in self.whitelist:
                if len(re.findall(sender, e_sender))>0:
                    self.release_email(e_readdr)
                    typ = i_s.store(mail_no, "+FLAGS", "\\Deleted")
                    if re.match("ok", typ[0], re.IGNORECASE) is not None:
                        e_subject = re.findall("subject:\s*(.*)\r\n", raw_email[0][1], re.IGNORECASE)
                        e_date = re.findall("date:\s*(.*)\r\n", raw_email[0][1], re.IGNORECASE)
                        if len(e_subject) == 0 : e_subject=["No subject"]
                        if len(e_date) == 0 : e_date = ["unknown"]
                        self.log("Delete email: " + e_subject[0] + "\n" + "From: " + e_sender + "\n" + "Time: " + e_date[0])
                        num_released += 1
                    else:
                        self.log("Err When Delete Email: " + typ.__str__())
                    break
        i_s.expunge()
        i_s.close()
        i_s.logout()
        self.log("Finished Checking New Email: " + str(num_released) + " released")
    
    def release_email(self, addr):
        if self.debug:
            addr = "kwang3@wpi.edu"
            self.RELEASE_MSG = 'From: "cssa@wpi.edu" <cssa@wpi.edu>\r\nTo: "' + addr + '" <'+ addr +'>\r\nRelease\r\n\r\n' + addr
        s_s = smtplib.SMTP(self.smtp_server)
        s_s.login(self.account, self.pswd)
        sender = self.account + "@" + self.smtp_server.split(".")[-2] + "." + self.smtp_server.split(".")[-1]
        s_s.sendmail(sender, addr, 'From: "cssa@wpi.edu" <cssa@wpi.edu>\r\nTo: "' + addr + '" <'+ addr +'>\r\nRelease\r\n\r\n' + self.RELEASE_MSG)
        s_s.close()

    def log(self, logdata):
        err_str = datetime.datetime.today().ctime() + ": " + logdata + "\r\n\r\n"
        logfile = open("log.txt", "a")
        logfile.write(err_str)
        logfile.close()
        
    def white_list_update_daemon(self):
        self.getwhitelist()
        threading.Timer(self.WHITE_LIST_UPDATE_FREQUENCE, self.white_list_update_daemon).start()
    
    def check_email_release_daemon(self):
        self.checknewemail()
        threading.Timer(self.CHECK_FREQUENCE, self.check_email_release_daemon).start()
    
    def starts(self):
        self.white_list_update_daemon()
        self.check_email_release_daemon()
        
if __name__ == '__main__':
    account = raw_input("Input maillist account (default is \"cssa\")")
    if account == "": account = "cssa"
    pswd = raw_input("Password:")
    i_server = raw_input("IMAP Server: (default \"imap.wpi.edu\")")
    if i_server == "": i_server = "imap.wpi.edu"
    s_server = raw_input("SMTP server: (default \"submission.wpi.edu\")")
    if s_server == "": s_server = "submission.wpi.edu"
    wpi_releaser = releaser(account, pswd, i_server, s_server)
    wpi_releaser.starts()
    
