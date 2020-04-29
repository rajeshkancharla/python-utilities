import os
import win32com.client as win32

def send_email(
    to =<email_id>
    ,subject = <email_subject>
    ,body =<email_body>
    ,attachment_path = <fully_qualified_path_name_to_attachment>
):

    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = to
    mail.Subject = subject
    mail.Body = body
    #mail.HTMLBody = '<h2>TESTING HTML</h2>' #this field is optional

    # To attach a file to the email (optional):
    attachment  = attachment_path
    mail.Attachments.Add(attachment)

    mail.Send()
