# M101 SSH Botnet Framework

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.6%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)

A powerful SSH-based botnet framework for educational purposes and authorized penetration testing. This tool allows for the management of multiple SSH connections to create a distributed network of systems for various security testing scenarios.

## ⚠️ Disclaimer

This tool is provided for **EDUCATIONAL PURPOSES ONLY**. The authors and contributors are not responsible for any misuse or damage caused by this program. Only use this on systems you own or have explicit permission to test.

**Unauthorized use of this tool against systems without proper authorization is illegal and unethical.**

## 🔍 Features

- Manage multiple SSH connections as "bots"
- Execute commands across all connected systems simultaneously
- Interactive bash shell access to all bots
- Persistent botnet management (save/load functionality)
- Distributed Denial of Service (DDoS) attack capabilities
- Colorized interface for better usability

## 📋 Requirements

- Python 3.6+
- Dependencies:
  - colorama (0.4.6)
  - pexpect (4.9.0)
  - scapy (2.6.1)

## 🔧 Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/M101_Botnet.git
   cd M101_Botnet/SSH-Botnets
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## 🚀 Usage

Run the script:
```
python ssh_botnet.py
```

### Main Menu Options

1. **List Bots** - Display all connected bots in the botnet
2. **Run Command** - Execute a command on all connected bots
3. **Bash** - Enter interactive bash mode to run commands on all bots
4. **Add Bot** - Add a new bot to the botnet by providing SSH credentials
5. **DDOS** - Initiate a DDoS attack using all connected bots
6. **Stop DDOS** - Stop any ongoing DDoS attacks
7. **Exit** - Save the botnet configuration and exit the program

### Adding Bots

To add a new bot to your botnet:
1. Select option 4 from the main menu
2. Enter the target's IP address
3. Enter the SSH port (usually 22)
4. Enter the username
5. Enter the password

The bot will be automatically saved to `botnet.json` for future sessions.

### Running Commands

Select option 2 from the main menu and enter the command you wish to execute on all bots. The output from each bot will be displayed with the corresponding host information.

### DDoS Attack

The DDoS functionality creates a TCP flood attack against a specified target:
1. Select option 5 from the main menu
2. Enter the target IP address
3. Enter the target port (default: 80)
4. Enter the attack duration in seconds (default: 60)

To stop an ongoing attack, select option 6 from the main menu.

## 📁 File Structure

- `ssh_botnet.py` - Main script containing all botnet functionality
- `requirements.txt` - List of required Python packages
- `botnet.json` - Automatically generated file that stores botnet configuration

## 🔄 Persistence

The botnet configuration is automatically saved to `botnet.json` when:
- Adding a new bot
- Exiting the program

When the script is started, it automatically attempts to load and reconnect to all bots from the saved configuration.

## 🛡️ Security Considerations

- All bot credentials are stored in plaintext in the `botnet.json` file
- No encryption is used for command transmission
- The tool is designed for educational purposes and controlled environments only

## 🔧 Technical Details

### DDoS Implementation

The DDoS attack works by creating a Python script on each bot that:
1. Opens multiple TCP connections to the target
2. Sends HTTP GET requests with large payloads
3. Uses multithreading to maximize impact
4. Runs for a specified duration

### SSH Connection

The tool uses the `pxssh` module from `pexpect` to establish and maintain SSH connections to each bot.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

For questions or feedback, please open an issue in the GitHub repository.

---

**Remember**: This tool should only be used for educational purposes or on systems you have permission to test.