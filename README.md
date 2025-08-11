# LinkedIn Checkbox Selector 🤖

A Python automation tool that selects checkboxes for LinkedIn group invitations, saving you time from manually clicking each checkbox. The tool connects to your existing Chrome browser session and only selects checkboxes - you maintain full control over sending invitations.

## ⚠️ Important Disclaimer

**USE AT YOUR OWN RISK!** This tool may violate LinkedIn's Terms of Service. Your account could be restricted or banned. The author is not responsible for any consequences. Use responsibly and sparingly.

## ✨ Features

- 🎯 **Smart Checkbox Selection**: Automatically finds and selects LinkedIn invitation checkboxes
- 🔗 **Existing Browser Integration**: Connects to your current Chrome session (no new windows)
- ⚡ **High Speed**: Selects up to 50 checkboxes in ~10 seconds
- 🛡️ **Safe Control**: Only selects checkboxes - you manually click "Invite" button
- 🔄 **Reusable Session**: Use multiple times without re-logging in
- 🚫 **No Browser Closing**: Your browser stays open when tool exits

## 📋 Requirements

- **macOS** (tested on macOS)
- **Python 3.6+**
- **Google Chrome** browser
- **Active LinkedIn account** with group admin privileges

## 🚀 Installation

1. **Clone this repository:**
```bash
git clone https://github.com/abuhuraira-73/Linkedin-checkbox-selector.git
cd Linkedin-checkbox-selector
```

2. **Install Python dependencies:**
```bash
pip install selenium webdriver-manager
```

3. **Make sure Chrome is installed:**
   - The script automatically installs ChromeDriver
   - Ensure Google Chrome is in `/Applications/` (default location)

## 📖 Usage Instructions

### 🔧 **FIRST TIME SETUP (One-time only)**

#### Step 1: Close All Chrome Windows
Close every Chrome window completely to avoid conflicts.

#### Step 2: Start Chrome in Debug Mode
Open Terminal and run this **exact command**:
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/Users/$(whoami)/chrome-debug-session" &
```

#### Step 3: Navigate to LinkedIn
In the new Chrome window that opened:
1. Go to LinkedIn.com and log in
2. Navigate to your group
3. Go to the invitation page (usually "Manage" → "Members" → "Invite")
4. Make sure you can see the list of people with checkboxes
5. **Keep this Chrome window open**

#### Step 4: Run the Tool
Open a new Terminal window and run:
```bash
cd path/to/Linkedin-checkbox-selector
python3 linkedin_group_inviter.py
```

#### Step 5: Follow Tool Instructions
1. Accept the risk warning by typing `y`
2. Enter number of checkboxes to select (max 50)
3. Press ENTER when ready
4. Tool will connect to your Chrome and start selecting checkboxes
5. When done, manually click the "Invite" button in Chrome

### 🔄 **SUBSEQUENT USES (Super Easy!)**

After the first setup, you can use it multiple times:

1. **Keep the debug Chrome window open** (from first setup)
2. Navigate to any LinkedIn group invitation page in that same window
3. Run the tool again:
```bash
python3 linkedin_group_inviter.py
```
4. Tool connects instantly - no login needed!

## ⚡ Performance

- **Speed**: 50 checkboxes in ~10 seconds
- **Batch Size**: Processes 10 checkboxes at a time
- **Delay**: 0.1-0.2 seconds between selections
- **Break Time**: 0.5-1 second between batches

## 🛡️ Safety Features

- ✅ **Checkbox Only**: Never clicks invite buttons automatically
- ✅ **Session Preservation**: Uses your existing Chrome session
- ✅ **No New Windows**: Connects to current browser
- ✅ **Manual Control**: You decide when to send invitations
- ✅ **Error Handling**: Graceful failure recovery
- ✅ **Browser Protection**: Never closes your browser

## 🔧 Troubleshooting

### Connection Issues
```bash
# Check if debug port is active:
lsof -i :9222

# If nothing shows up, restart Chrome with debug command
```

### Common Problems
- **"Chrome debug mode not detected"**: Restart Chrome with the debug command
- **"No checkboxes found"**: Make sure you're on LinkedIn invitation page
- **Tool freezes**: Press Ctrl+C to stop, tool won't close your browser
- **Connection fails**: Close Chrome completely and restart with debug command

### Testing Connection
After starting debug Chrome, verify it's working:
```bash
curl http://localhost:9222/json/version
```
Should return Chrome version info.

## 📁 Project Structure

```
Linkedin-checkbox-selector/
├── linkedin_group_inviter.py    # Main Python script
├── README.md                    # This file
└── requirements.txt             # Python dependencies (optional)
```

## 🔄 Workflow Example

```bash
# One-time setup
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/Users/$(whoami)/chrome-debug-session" &

# Use for Group A
python3 linkedin_group_inviter.py
# Select 10 checkboxes → manually click Invite

# Navigate to Group B in same Chrome window
# Use again immediately
python3 linkedin_group_inviter.py
# Select 15 checkboxes → manually click Invite

# And so on...
```

## ⚖️ Legal & Ethics

- This tool is for **educational purposes**
- **Respect LinkedIn's Terms of Service**
- **Use sparingly** to avoid account restrictions
- **Monitor your account** for any warnings
- **Author is not liable** for any consequences

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is provided as-is for educational purposes. Use at your own risk.

## 📞 Support

- Open an issue in this repository
- Make sure to include error messages and Chrome version
- Describe your setup and what went wrong

## 🎯 Tips for Best Results

1. **Start Small**: Begin with 5-10 invitations to test
2. **Spread Usage**: Don't use daily or frequently  
3. **Monitor Account**: Watch for LinkedIn warnings
4. **Respect Limits**: Don't exceed 50 selections per session
5. **Multiple Sessions**: Restart Chrome debug session daily

---

**Made with ❤️ for automation enthusiasts. Use responsibly!**
