# LinkedIn Checkbox Selector

This script automates the process of selecting checkboxes for LinkedIn group invitations, saving you from manually clicking checkboxes one by one. You'll still click the 'Invite' button manually for better safety.

## ⚠️ Important Warning

**USE AT YOUR OWN RISK!** This tool may violate LinkedIn's Terms of Service. Your account could be restricted or banned. The author is not responsible for any consequences.

## Requirements

- Python 3.6+
- Chrome browser installed on your Mac
- Active LinkedIn account with group admin privileges

## Installation

The script will automatically install ChromeDriver when you first run it. You already have Python and Selenium installed.

## How to Use

1. **Open Chrome and navigate to LinkedIn:**
   - Open Chrome browser manually
   - Log in to your LinkedIn account
   - Navigate to your group's invitation page
   - Go to "Manage" → "Members" → "Invite" or similar section
   - Make sure the list of people with checkboxes is visible

2. **Run the script:**
   ```bash
   cd /Users/abuhuraira/Coding/"linkedin checkbox folder"
   python3 linkedin_group_inviter.py
   ```

3. **Accept the risk warning** by typing 'y'

4. **Enter how many checkboxes you want to select** (recommended: start with 5-10)

5. **The tool will connect to your existing Chrome session:**
   - No new browser window will open
   - It uses your existing LinkedIn session
   - Press ENTER when you're ready to start

6. **Automation will begin:**
   - The script will automatically select checkboxes only
   - YOU manually click the 'Invite' button when ready
   - Process selections in small batches with delays
   - Browser stays open when you close the tool

## Safety Features

- **Checkbox selection only:** Only selects checkboxes - you click 'Invite' manually
- **Uses existing browser:** Connects to your current Chrome session, no new windows
- **Batch processing:** Selects checkboxes in small groups (max 5 at a time)
- **Random delays:** Mimics human behavior to avoid detection
- **Rate limiting:** Takes breaks between batches
- **Browser stays open:** Never closes your browser when tool exits
- **Manual control:** You decide when to actually send invitations

## Tips for Safe Usage

1. **Start small:** Begin with 5-10 invitations to test
2. **Spread over time:** Don't invite hundreds of people in one session
3. **Monitor your account:** Watch for any warnings from LinkedIn
4. **Use sparingly:** Don't run this script daily or frequently
5. **Check LinkedIn policies:** Make sure you comply with their current terms

## Troubleshooting

- **Chrome not found:** Make sure Chrome browser is installed
- **No checkboxes found:** Verify you're on the correct LinkedIn page
- **Script stuck:** Press Ctrl+C to stop and restart
- **Login issues:** Clear browser data and try again

## How It Works

1. Connects to your existing Chrome browser session
2. Detects your current LinkedIn page
3. Searches for checkboxes using multiple selectors
4. Selects checkboxes in batches with human-like delays
5. Leaves the 'Invite' button for you to click manually
6. Keeps your browser open when finished

Remember: Use responsibly and at your own risk!
