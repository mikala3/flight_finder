import smtplib    

#start a terminal with this command, setting up a local smtp server
#python3 -m smtpd -c DebuggingServer -n localhost:1025

def send(sender, receiver, mess):
   sender_mail = sender 
   receivers_mail = receiver  
   message = mess
   try:    
      smtpObj = smtplib.SMTP('localhost:1025') 
      smtpObj.sendmail(sender_mail, receivers_mail, message)    
      print("Successfully sent email")    
   except Exception:    
      print("Error: unable to send email")   