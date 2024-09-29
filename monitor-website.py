import smtplib
import requests 
import os
import paramiko
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv(".env\\.env")  # take environment variables

subscription_id     = os.getenv('AZURE_SUBSCRIPTION_ID')
resource_group_name = 'VmResources'             #Can be set as env.variable if you want
vm_name             = "LinuxVm"

# Initialize the Azure credentials and Compute Management Client
credential     = DefaultAzureCredential()
compute_client = ComputeManagementClient(credential, subscription_id)

sender_email    = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_EMAIL_PWD')                                  #Set an app password on gmail
receiver_email  = os.getenv('RECEIVER_EMAIL')
url_to_check    = "http://mohibzahid.eastus.cloudapp.azure.com:8080/"           #Can set as an env.var as well


def send_email(subject, message):
  with smtplib.SMTP('smtp.gmail.com', 587) as server:           #Access Google domain and port
    server.starttls()                                           #Encryption enabled (Necessary)
    server.ehlo                                                 #A handshake to make server aware (Optional)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message.as_string())


def restart_container():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname="mohibzahid.eastus.cloudapp.azure.com", username="azureuser", key_filename="C:/Users/mohib/.ssh/id_rsa")
    stdin, stdout, stderr = ssh.exec_command('docker start 0358ccc9930f')
    print(stdout.readlines())
    ssh.close()
    print("Application restarted")


try:
  # Send a GET request to the health check URL
  response = requests.get(url_to_check)

  if response.status_code == 200:
    # Application is running
    print("Application running successfully")
    message = MIMEText(f"Application is running! Response code: {response.status_code}")        #Email message
    message['Subject'] = "Application Status: Running"                                          #Email Subject
    send_email(message['Subject'], message)
  else:
    # Application is not running
    print("Application not running")
    message = MIMEText(f"Application is not running! Response code: {response.status_code}")
    message['Subject'] = "Application Status: Not Running"
    send_email(message['Subject'], message)
    restart_container()

except Exception as e:
  # Error occurred such as connection failure
  print("Error Occured")
  message = MIMEText(f"An error occurred: {str(e)}")
  message['Subject'] = "Application Status: Error"
  send_email(message['Subject'], message)

  print("Rebooting server")
  compute_client.virtual_machines.begin_restart(resource_group_name, vm_name)
  restart_container()                 #You can also use 'docker update --restart unless-stopped <container-id>' cmd on server to automate container restart when server restart


