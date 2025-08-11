#!/usr/bin/env python3
"""
LinkedIn Group Invitation Automator
====================================

This script automates the process of inviting people to your LinkedIn group.
It includes safety features to avoid detection and account restrictions.

IMPORTANT DISCLAIMER:
- Use this script at your own risk
- LinkedIn prohibits automated activities
- Your account could be restricted or banned
- Use responsibly and sparingly

Requirements:
- selenium
- Chrome browser
- ChromeDriver (will be installed automatically)
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import sys

class LinkedInGroupInviter:
    def __init__(self):
        self.driver = None
        self.wait = None
        
    
    def setup_driver(self):
        """Setup Chrome driver to connect to existing Chrome session"""
        print("Setting up Chrome driver to connect to your existing Chrome session...")
        print("\n📋 IMPORTANT: You need to start Chrome with a special debug command.")
        print("\n🔧 STEP 1: Close Chrome completely. All windows.")
        print("🔧 STEP 2: Open Terminal and run this EXACT command:")
        
        # Using a dedicated user data dir is more reliable
        debug_command = f'/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222 --user-data-dir="/Users/abuhuraira/chrome-debug-session" &'
        print(f'   {debug_command}')
        
        print("\n🔧 STEP 3: A new Chrome window will open. Use THIS window.")
        print("🔧 STEP 4: In that window, log into LinkedIn and go to your group's invitation page.")
        print("🔧 STEP 5: Once you see the checkboxes, come back here and press ENTER.")
        
        input("\nPress ENTER when you are ready...")
        
        print("\n⏳ Searching for the debug Chrome session...")
        max_attempts = 5
        for i in range(max_attempts):
            print(f"   Attempt {i+1}/{max_attempts}...")
            if self._is_debug_chrome_running():
                print("   ✅ Found running Chrome with debug port!")
                try:
                    if self._connect_to_existing_chrome():
                        print("   ✅ Successfully connected to your Chrome session!")
                        # Check if we can get the URL to confirm connection
                        print(f"   ✅ Current page: {self.driver.current_url}")
                        return True
                except Exception as e:
                    print(f"   ❌ Found Chrome, but connection failed: {e}")
                    break # Don't retry if connection fails
            
            if i < max_attempts - 1:
                time.sleep(2) # Wait 2 seconds before retrying

        print("\n❌ FAILED TO CONNECT.")
        print("Please check the following:")
        print("1. Did you close all other Chrome windows first?")
        print("2. Did you run the EXACT command provided?")
        print("3. Is the special Chrome window still open?")
        return False
    
    def _is_debug_chrome_running(self):
        """Check if Chrome is running with debug port"""
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', 9222))
            sock.close()
            return result == 0
        except:
            return False
    
    def _connect_to_existing_chrome(self):
        """Try to connect to an existing Chrome browser"""
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 10)
            print("✅ Connected to existing Chrome browser!")
            return True
        except Exception as e:
            raise e
    
    def _start_new_chrome_with_debug(self):
        """This method is no longer used - we only connect to existing Chrome"""
        print("❌ This method should not be called anymore.")
        return False
    
    def _fallback_chrome_setup(self):
        """Fallback setup - will not open new Chrome, just connect to existing"""
        print("❌ Could not connect to existing Chrome session.")
        print("\n🚀 SOLUTION: Please start Chrome with debug mode manually:")
        print("1. Close all Chrome windows")
        print("2. Run this command in Terminal:")
        print('   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &')
        print("3. Navigate to LinkedIn in the opened Chrome window")
        print("4. Run this script again")
        return False
    
    def check_linkedin_page(self):
        """Quickly verify we're on a LinkedIn page."""
        current_url = self.driver.current_url
        if "linkedin.com" in current_url:
            print(f"\n✅ Verification successful. On page: {current_url}")
            print("   Ready to start selecting checkboxes.")
            return True
        else:
            print(f"\n❌ NOT ON LINKEDIN! Current page: {current_url}")
            print("   Please navigate to your LinkedIn group invitation page in the debug Chrome window and run the tool again.")
            return False
    
    def random_delay(self, min_seconds=1, max_seconds=3):
        """Add random delay to appear more human-like"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def find_checkboxes(self):
        """Find all available checkboxes for inviting people"""
        possible_selectors = [
            "input[type='checkbox']",
            "input[data-control-name*='invite']",
            "input[data-test-id*='checkbox']",
            ".artdeco-checkbox__input",
            "[role='checkbox']",
            "input.checkbox"
        ]
        
        checkboxes = []
        for selector in possible_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    checkboxes.extend(elements)
                    print(f"✅ Found {len(elements)} checkboxes with selector: {selector}")
            except Exception as e:
                continue
        
        # Remove duplicates
        unique_checkboxes = []
        for checkbox in checkboxes:
            if checkbox not in unique_checkboxes:
                unique_checkboxes.append(checkbox)
        
        return unique_checkboxes
    
    def find_invite_button(self):
        """Find the invite button"""
        possible_selectors = [
            "button[data-control-name*='invite']",
            "button:contains('Invite')",
            "button[aria-label*='Invite']",
            "button.artdeco-button--primary",
            "[data-test-id*='invite-button']"
        ]
        
        for selector in possible_selectors:
            try:
                if ":contains" in selector:
                    # Use XPath for text-based selection
                    button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Invite') or contains(text(), 'Send') or contains(text(), 'Add')]")
                else:
                    button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                if button and button.is_enabled():
                    return button
            except Exception:
                continue
        
        return None
    
    def select_checkboxes(self, max_selections):
        """Main function to select checkboxes only - no invite button clicking"""
        print(f"\n📋 Starting to select up to {max_selections} checkboxes...")
        
        total_selected = 0
        batch_size = min(10, max_selections)  # Process in bigger batches for speed
        
        while total_selected < max_selections:
            print(f"\n📊 Progress: {total_selected}/{max_selections} checkboxes selected")
            
            # Find available checkboxes
            checkboxes = self.find_checkboxes()
            if not checkboxes:
                print("❌ No checkboxes found. Please make sure you're on the correct page.")
                break
            
            # Filter out already selected checkboxes
            unselected_checkboxes = [cb for cb in checkboxes if not cb.is_selected()]
            print(f"Found {len(checkboxes)} total checkboxes, {len(unselected_checkboxes)} unselected")
            
            if not unselected_checkboxes:
                print("✅ All available checkboxes are already selected!")
                break
            
            # Select checkboxes for this batch
            remaining_selections = max_selections - total_selected
            batch_count = min(batch_size, remaining_selections, len(unselected_checkboxes))
            
            selected_count = 0
            for i in range(batch_count):
                try:
                    checkbox = unselected_checkboxes[i]
                    
                    # Scroll to checkbox and click (faster, no delays)
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                    
                    # Use JavaScript click for speed
                    self.driver.execute_script("arguments[0].click();", checkbox)
                    
                    selected_count += 1
                    print(f"✅ Selected checkbox {selected_count} (Total: {total_selected + selected_count})")
                    
                    # Very short delay for speed (0.1-0.2 seconds)
                    time.sleep(random.uniform(0.1, 0.2))
                    
                except Exception as e:
                    print(f"⚠️  Could not select checkbox {i+1}: {e}")
                    continue
            
            if selected_count == 0:
                print("❌ No checkboxes were selected in this batch. Stopping.")
                break
            
            total_selected += selected_count
            print(f"✅ Selected {selected_count} checkboxes in this batch")
            
            # Much shorter delay between batches for speed
            if total_selected < max_selections and total_selected < len(unselected_checkboxes):
                delay_time = random.uniform(0.5, 1.0)  # Very short break
                print(f"⚡ Quick {delay_time:.1f}s break before next batch...")
                time.sleep(delay_time)
            else:
                break
        
        print(f"\n🎉 Checkbox selection complete! Total checkboxes selected: {total_selected}")
        print("\n👆 Now you can manually click the 'Invite' or 'Send' button when you're ready!")
        return total_selected
    
    def run(self):
        """Main execution function"""
        print("🤖 LinkedIn Group Invitation Automator")
        print("="*40)
        
        # Get user input
        try:
            max_invites = int(input("How many people would you like to invite? "))
            if max_invites <= 0:
                print("❌ Please enter a positive number")
                return
        except ValueError:
            print("❌ Please enter a valid number")
            return
        
        # Safety warning
        if max_invites > 50:
            print(f"\n⚠️  WARNING: Selecting {max_invites} checkboxes at once might be too many!")
            print("Recommendation: Maximum is 50 checkboxes.")
            confirm = input("Do you want to continue? (y/N): ").lower()
            if confirm != 'y':
                print("Cancelled by user")
                return
        
        # Setup driver
        if not self.setup_driver():
            return
        
        try:
            # Check LinkedIn page
            if not self.check_linkedin_page():
                return
            
            # Start selecting checkboxes
            total_selected = self.select_checkboxes(max_invites)
            
            if total_selected > 0:
                print(f"\n✅ Success! Selected {total_selected} checkboxes")
                print("👆 You can now manually click the 'Invite' button to send the invitations!")
            else:
                print("\n❌ No checkboxes were selected")
        
        except KeyboardInterrupt:
            print("\n\n⏹️  Automation stopped by user")
        
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
        
        finally:
            # Never close browser or driver connection
            print("\n✅ Checkbox selection complete! Browser remains open.")
            print("👋 You can now click 'Invite' manually and continue using LinkedIn normally.")
            # Don't quit driver or close browser
            pass
    
    def __del__(self):
        # Never close browser or quit driver - let user keep their session
        if hasattr(self, 'driver') and self.driver:
            try:
                # Don't quit the driver - this would close the browser
                pass
            except:
                pass

def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("⚠️  IMPORTANT DISCLAIMER")
    print("="*60)
    print("This tool automates LinkedIn interactions, which may violate")
    print("LinkedIn's Terms of Service. Use at your own risk.")
    print("Your account could be restricted or banned.")
    print("The author is not responsible for any consequences.")
    print("="*60)
    
    confirm = input("\nDo you understand and accept the risks? (y/N): ").lower()
    if confirm != 'y':
        print("Exiting...")
        return
    
    inviter = LinkedInGroupInviter()
    inviter.run()

if __name__ == "__main__":
    main()
