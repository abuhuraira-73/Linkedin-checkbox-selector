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
            # Try to hide webdriver property, ignore if already defined
            try:
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            except:
                pass  # Property already defined, continue anyway
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
    
    def find_checkboxes(self, silent=False):
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
                    if not silent:
                        print(f"✅ Found {len(elements)} checkboxes with selector: {selector}")
            except Exception as e:
                continue
        
        # Remove duplicates
        unique_checkboxes = []
        for checkbox in checkboxes:
            if checkbox not in unique_checkboxes:
                unique_checkboxes.append(checkbox)
        
        return unique_checkboxes
    
    def fast_scroll_to_load_profiles(self, target_checkboxes="max"):
        """BLAZING FAST LinkedIn scroll - optimized for thousands of profiles"""
        print(f"\n🚀 BLAZING FAST SCROLL MODE: Racing through thousands of profiles!")
        print("⚡ ZERO delays, maximum speed - watch the page FLY!")
        
        total_found = 0
        total_selected = 0
        scroll_count = 0
        consecutive_no_new = 0
        
        # Track page changes
        initial_height = self.driver.execute_script("return document.body.scrollHeight;")
        print(f"🏁 Starting: {initial_height}px height")
        
        while True:
            scroll_count += 1
            
            # Get current state quickly
            current_height = self.driver.execute_script("return document.body.scrollHeight;")
            
            # ULTRA AGGRESSIVE MULTI-STRATEGY SCROLLING!
            
            # Strategy 1: Massive pixel jumps (100,000px each!)
            for jump in range(10):  
                self.driver.execute_script("window.scrollBy(0, 100000);")  # HUGE 100,000px jumps!
            
            # Strategy 2: Jump to bottom multiple times
            for bottom_jump in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight + 50000);") 
            
            # Strategy 3: Try to scroll to maximum possible values
            self.driver.execute_script("window.scrollTo(0, 999999999);")  # Scroll to huge number
            
            # Strategy 4: Force refresh scroll calculations
            self.driver.execute_script("""
                document.body.scrollTop = document.body.scrollHeight;
                document.documentElement.scrollTop = document.documentElement.scrollHeight;
                window.pageYOffset = document.body.scrollHeight;
            """) 
            
            # Strategy 5: Trigger LinkedIn-specific loading events
            self.driver.execute_script("""
                // Trigger intersection observer events
                window.dispatchEvent(new Event('scroll'));
                window.dispatchEvent(new Event('resize'));
                document.dispatchEvent(new Event('scroll'));
                document.dispatchEvent(new Event('DOMContentLoaded'));
                
                // Force focus and blur to trigger lazy loading
                window.focus();
                window.blur();
                window.focus();
                
                // Trigger viewport events
                window.dispatchEvent(new Event('orientationchange'));
            """)
            
            # Trigger all scroll events instantly
            self.driver.execute_script("""
                window.dispatchEvent(new Event('scroll'));
                window.dispatchEvent(new Event('resize')); 
                document.dispatchEvent(new Event('scroll'));
            """)
            
            # Look for load buttons and click them instantly (no delay)
            try:
                load_buttons = self.driver.find_elements(By.CSS_SELECTOR, 
                    "button[aria-label*='more'], button[aria-label*='Show'], [data-control-name*='load'], .scaffold-finite-scroll__load-button")
                for button in load_buttons:
                    try:
                        if button.is_displayed():
                            self.driver.execute_script("arguments[0].click();", button)
                    except:
                        pass
            except:
                pass
            
            # Only minimal wait for LinkedIn to respond (reduced from 3s to 0.2s)
            time.sleep(0.2)  
            
            # Check results quickly
            new_height = self.driver.execute_script("return document.body.scrollHeight;")
            height_changed = new_height > current_height
            
            # Count checkboxes quickly - handle stale elements
            try:
                all_checkboxes = self.find_checkboxes(silent=True)
                unselected_checkboxes = []
                for cb in all_checkboxes:
                    try:
                        if not cb.is_selected():
                            unselected_checkboxes.append(cb)
                    except Exception:
                        # Skip stale elements
                        continue
                current_available = len(unselected_checkboxes)
            except Exception:
                current_available = 0
                unselected_checkboxes = []
            
            # Progress update every 10 scrolls (not every scroll)
            if scroll_count % 10 == 0:
                height_increase = new_height - initial_height if height_changed else 0
                print(f"⚡ Scroll #{scroll_count}: Height +{height_increase}px, {current_available} checkboxes found")
            
            # If we found new checkboxes, select them FAST
            if current_available > total_found:
                new_checkboxes = current_available - total_found
                print(f"🎉 FOUND {new_checkboxes} NEW! Selecting instantly...")
                
                # LIGHTNING FAST SELECTION - mass select with single JavaScript execution
                checkboxes_to_select = unselected_checkboxes[total_found:current_available]
                selected_in_batch = 0
                
                # Method 1: Instant mass selection with stale element protection
                try:
                    # Re-find fresh elements to avoid stale references
                    fresh_checkboxes = self.find_checkboxes(silent=True)
                    fresh_unselected = []
                    for cb in fresh_checkboxes:
                        try:
                            if not cb.is_selected():
                                fresh_unselected.append(cb)
                        except Exception:
                            continue
                    
                    # Only select new ones we haven't selected yet
                    checkboxes_to_select = fresh_unselected[total_found:] if len(fresh_unselected) > total_found else []
                    
                    # Build JavaScript to click all checkboxes at once
                    if checkboxes_to_select:
                        js_clicks = []
                        for i, checkbox in enumerate(checkboxes_to_select):
                            js_clicks.append(f"arguments[{i}].click();")
                        
                        # Execute all clicks in one JavaScript call (FASTEST METHOD)
                        js_code = " ".join(js_clicks)
                        self.driver.execute_script(js_code, *checkboxes_to_select)
                        selected_in_batch = len(checkboxes_to_select)
                        total_selected += selected_in_batch
                        
                        if target_checkboxes != "max" and total_selected >= target_checkboxes:
                            print(f"🎯 TARGET {target_checkboxes} REACHED! Selected {total_selected}!")
                            return total_selected
                            
                except Exception as e:
                    print(f"⚠️ Batch method failed: {e}, using individual clicks...")
                    # Fallback: Individual ultra-fast clicks with stale element protection
                    fresh_checkboxes = self.find_checkboxes(silent=True)
                    for checkbox in fresh_checkboxes:
                        try:
                            # Check if already selected
                            if checkbox.is_selected():
                                continue
                                
                            self.driver.execute_script("arguments[0].click();", checkbox)
                            selected_in_batch += 1
                            total_selected += 1
                            
                            if target_checkboxes != "max" and total_selected >= target_checkboxes:
                                print(f"🎯 TARGET {target_checkboxes} REACHED! Selected {total_selected}!")
                                return total_selected
                        except Exception as stale_e:
                            # Skip stale elements
                            continue
                
                print(f"✅ Selected {selected_in_batch} instantly! Total: {total_selected}")
                total_found = current_available
                consecutive_no_new = 0
                continue
                
            else:
                consecutive_no_new += 1
                # Only show status every 5 attempts (reduce spam)
                if consecutive_no_new % 5 == 0:
                    print(f"🔍 Still searching... {consecutive_no_new}/20 attempts, {total_selected} selected so far")
            
            # INFINITE MODE - Only stop if user presses Ctrl+C or finds checkboxes!
            # Remove the 20 attempt limit completely for unlimited scrolling
            
            # Only give status updates, never stop automatically
            if consecutive_no_new >= 50:  # Much higher threshold for status
                height_increase = new_height - initial_height
                print(f"\n📊 STATUS UPDATE after {scroll_count} scrolls:")
                print(f"   - Height increased: +{height_increase}px")
                print(f"   - Checkboxes found so far: {total_selected}")
                print(f"   - Consecutive attempts without new checkboxes: {consecutive_no_new}")
                print(f"   - Still searching... (This could take hundreds of scrolls!)")
                print(f"   - Press Ctrl+C if you want to stop\n")
                
                # Reset counter to continue indefinitely
                consecutive_no_new = 0
                
                # Don't break - keep going infinitely!
            
            # For max mode, continue at maximum speed
            if target_checkboxes == "max":
                continue
                
        print(f"\n⚡ BLAZING FAST SCROLL COMPLETE! {total_selected} checkboxes selected in {scroll_count} attempts")
        return total_selected
    
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
        # First, find all available checkboxes to get the total count
        all_checkboxes = self.find_checkboxes()
        unselected_checkboxes = [cb for cb in all_checkboxes if not cb.is_selected()]
        total_available = len(unselected_checkboxes)
        
        # If max_selections is "max" or greater than available, select all
        if max_selections == "max" or max_selections >= total_available:
            actual_max = total_available
            print(f"\n📋 Selecting ALL {actual_max} available checkboxes...")
        else:
            actual_max = max_selections
            print(f"\n📋 Starting to select up to {actual_max} checkboxes out of {total_available} available...")
        
        total_selected = 0
        batch_size = min(10, actual_max)  # Process in bigger batches for speed
        
        while total_selected < actual_max:
            if max_selections == "max":
                print(f"\n📊 Progress: {total_selected} checkboxes selected (selecting all available)")
            else:
                print(f"\n📊 Progress: {total_selected}/{actual_max} checkboxes selected")
            
            # Find available checkboxes
            checkboxes = self.find_checkboxes()
            if not checkboxes:
                print("❌ No checkboxes found. Please make sure you're on the correct page.")
                break
            
            # Filter out already selected checkboxes with stale element protection
            unselected_checkboxes = []
            for cb in checkboxes:
                try:
                    if not cb.is_selected():
                        unselected_checkboxes.append(cb)
                except Exception:
                    # Skip stale elements
                    continue
            print(f"Found {len(checkboxes)} total checkboxes, {len(unselected_checkboxes)} unselected")
            
            if not unselected_checkboxes:
                print("✅ All available checkboxes are already selected!")
                break
            
            # Select checkboxes for this batch  
            if max_selections == "max":
                remaining_selections = actual_max - total_selected
            else:
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
            if total_selected < actual_max and total_selected < len(unselected_checkboxes):
                delay_time = random.uniform(0.5, 1.0)  # Very short break
                print(f"⚡ Quick {delay_time:.1f}s break before next batch...")
                time.sleep(delay_time)
            else:
                break
        
        print(f"\n🎉 Checkbox selection complete! Total checkboxes selected: {total_selected}")
        print("\n👆 Now you can manually click the 'Invite' or 'Send' button when you're ready!")
        return total_selected
    
    def run(self):
        """Main execution function with enhanced workflow"""
        print("🤖 LinkedIn Group Invitation Automator")
        print("="*40)
        
        # Setup driver first
        if not self.setup_driver():
            return
        
        try:
            # Check LinkedIn page
            if not self.check_linkedin_page():
                return
            
            # STEP 1: Initial scan for checkboxes
            print("\n🔍 Scanning current page for checkboxes...")
            all_checkboxes = self.find_checkboxes()
            unselected_checkboxes = []
            for cb in all_checkboxes:
                try:
                    if not cb.is_selected():
                        unselected_checkboxes.append(cb)
                except Exception:
                    # Skip stale elements
                    continue
            current_available = len(unselected_checkboxes)
            
            print(f"📊 Found {current_available} checkboxes currently visible")
            
            # STEP 2: Decision based on available checkboxes
            if current_available >= 100:  # Enough checkboxes available
                print(f"✅ Good! {current_available} checkboxes are available for selection.")
                
                # Get user input for selection
                user_input = input(f"How many would you like to select? (Enter number or 'max' for all {current_available}): ").strip().lower()
                
                if user_input == "max":
                    max_invites = "max"
                    print(f"✅ Will select ALL {current_available} visible checkboxes!")
                else:
                    try:
                        max_invites = int(user_input)
                        if max_invites <= 0:
                            print("❌ Please enter a positive number or 'max'")
                            return
                        if max_invites > current_available:
                            max_invites = current_available
                            print(f"⚠️  Only {current_available} available, selecting all of them.")
                    except ValueError:
                        print("❌ Please enter a valid number or 'max'")
                        return
                
                # Safety warning
                if max_invites == "max" or max_invites > 50:
                    warning_text = "ALL checkboxes" if max_invites == "max" else f"{max_invites} checkboxes"
                    print(f"\n⚠️  WARNING: Selecting {warning_text} at once might be many!")
                    confirm = input("Do you want to continue? (y/N): ").lower()
                    if confirm != 'y':
                        print("Cancelled by user")
                        return
                
                # Select from currently visible checkboxes
                total_selected = self.select_checkboxes(max_invites)
                
            else:  # Few or no checkboxes available (< 100)
                if current_available == 0:
                    print("❌ No checkboxes found on current page.")
                else:
                    print(f"⚠️  Only {current_available} checkboxes found (less than 100).")
                
                print("This usually means people above have already been invited.")
                print("I can scroll down to load more profiles and find more checkboxes!")
                
                # Ask for scroll and select mode
                scroll_input = input("\nHow many checkboxes should I scroll and find? (Enter number or 'max' for unlimited): ").strip().lower()
                
                if scroll_input == "max":
                    print("✅ Unlimited scrolling mode activated!")
                    print("⚡ I will keep scrolling and selecting until you press Ctrl+C or no more profiles are found.")
                    confirm = input("\nReady to start unlimited scrolling? (y/N): ").lower()
                    if confirm != 'y':
                        print("Cancelled by user")
                        return
                    
                    # Start unlimited scroll mode
                    try:
                        total_selected = self.fast_scroll_to_load_profiles("max")
                    except KeyboardInterrupt:
                        print("\n\n⏹️  Scrolling stopped by user (Ctrl+C)")
                        return
                        
                else:
                    try:
                        target_checkboxes = int(scroll_input)
                        if target_checkboxes <= 0:
                            print("❌ Please enter a positive number or 'max'")
                            return
                    except ValueError:
                        print("❌ Please enter a valid number or 'max'")
                        return
                    
                    print(f"✅ Will scroll and find {target_checkboxes} checkboxes")
                    
                    # Safety warning for large numbers
                    if target_checkboxes > 100:
                        print(f"\n⚠️  WARNING: Scrolling to find {target_checkboxes} checkboxes might take a while!")
                        confirm = input("Do you want to continue? (y/N): ").lower()
                        if confirm != 'y':
                            print("Cancelled by user")
                            return
                    
                    # Start targeted scroll mode
                    total_selected = self.fast_scroll_to_load_profiles(target_checkboxes)
            
            # Final result
            if total_selected > 0:
                print(f"\n🎉 SUCCESS! Selected {total_selected} checkboxes total")
                print("👆 You can now manually click the 'Invite' button to send the invitations!")
            else:
                print("\n❌ No checkboxes were selected")
        
        except KeyboardInterrupt:
            print("\n\n⏹️  Automation stopped by user")
        
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
        
        finally:
            # Never close browser or driver connection
            print("\n✅ Tool completed! Browser remains open.")
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
