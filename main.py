import smtplib
import datetime
import arxiv
import os
import json
from argparse import ArgumentParser
from email.mime.text import MIMEText
from cryptography.fernet import Fernet

def main(hparams):
    # Load the key from the current directory named `filekey.key`
    with open('data/filekey.key', 'rb') as filekey:
        key = filekey.read()
    
    # Use the key
    cipher_suite = Fernet(key)
    
    # Read the encrypted credentials from the file
    with open('data/encrypted_account', 'rb') as encrypted_file:
        encrypted_credentials = encrypted_file.read()
    
    # Decrypt the credentials
    decrypted_credentials = cipher_suite.decrypt(encrypted_credentials)
    
    # Convert the credentials back to a dictionary
    credentials = json.loads(decrypted_credentials.decode('utf-8'))
    
    # Now you can use your credentials
    sender_email = credentials['email']
    receiver_email = credentials['email']
    email_password = credentials['password']


    # Define the filename for storing the last checked date
    last_checked_filename = 'last_checked_date.json'
    
    # Function to send an email
    def send_email(subject, body):
        # Set up the email server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Log in to the email account
        server.login(sender_email, email_password)
        # Create the email message
        message = MIMEText(body)
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        # Send the email
        server.send_message(message)
        # Quit the server
        server.quit()
    
    
    # Try to load the last checked date, if the file exists
    try:
        with open(last_checked_filename, 'r') as f:
            last_checked = datetime.datetime.strptime(json.load(f)['last_checked'], '%Y-%m-%d').date()
    except FileNotFoundError:
        last_checked = datetime.date.today()
    
    # Get today's date
    today = datetime.date.today()
    
    # Search parameters
    search_query = 'ti:"{}" AND cat:cs.*'.format(hparams.query)
    
    # Use the arxiv package to query arxiv
    search = arxiv.Search(
        query=search_query,
        max_results=hparams.num_paper,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    # Fetch the results
    new_papers = []
    for result in search.results():
        # Check if the paper is newer than the last checked date
        if result.published.date() > last_checked:
            new_papers.append(result)
    
    # Update the last checked date
    with open(last_checked_filename, 'w') as f:
        json.dump({'last_checked': str(today)}, f)
    
    # Send an email if there are new papers
    if new_papers:
        body = "New papers on arXiv with hparams.query in the title in Computer Science:\n\n"
        for paper in new_papers:
            body += f"Title: {paper.title}\n"
            body += f"Authors: {', '.join(author.name for author in paper.authors)}\n"
            body += f"Published: {paper.published}\n"
            body += f"URL: {paper.entry_id}\n\n"

        print(body)
        send_email(f"arXiv Daily Update: {hparams.query} Papers", body)
        print("Email sent with new papers.")
    else:
        print("No new papers found since last check.")


if __name__ == '__main__':
    parser = ArgumentParser(add_help=False)
    parser.add_argument("--query", default="sign language", type=str)
    parser.add_argument("--num_paper", default=10, type=int)
    
    hparams = parser.parse_args()
    main(hparams)
