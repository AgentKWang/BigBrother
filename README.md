# BigBrother

### What is moderated mail list?
   WPI's own email system, which is developed by 1980s tech, lacks of most modern functions and full of bugs. The best way to filter unwanted email is created a "moderated mail list", which holds all the incomming mails. If the list owner wants to release a mail, s/he has to logged in the UNIX mail server (Not the exchange one) and reply to it.

### They don't give you a whitelist to automatically release emails from those addresses? 
  Unbelivable but true indeed! They don't have such a thing. The IT service staff don't even quite understand the differences between the UNIX mail server and the Exchange server. So how could I be mad enough to believe that they will add such a reseanable function to the system? 

### You have to rely only on yourself!
  Yes, this python script can automatically check emails and release them if they come from someone in the whitelist. The check frequence is every 10 min by default. 

### How to run this?
1. Upload this to a server, which can run 24/7. I recommend WPI's UNIX service, they gave you a account to access one of the campus's unix server.
2. Create an input file to indicate the mail list account, password, imap and smtp server. I will give a sample in this reporsitory.
3. Create your whitelist.txt file. It uses python's regex to match. An example is also included.
3. Use nohup to run the python script so it won't be terminated after you logged out the server.
    nohup python releaser.py input.txt &
4. To-da! The emails will be automatically released now! Good luck!
