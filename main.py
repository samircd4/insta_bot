import json
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser

# Function for new login
def ig_login(username,password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context()
        page = context.new_page()
        url = 'https://www.instagram.com/'
        page.goto(url)
        page.get_by_label("Phone number, username, or").fill(username)
        page.get_by_label("Password").fill(password)
        page.get_by_role("button", name="Log in", exact=True).click()
        page.wait_for_timeout(5000)
        input('Wait for verification!')
        # page.get_by_role("button", name="Not Now").click()
        state = context.storage_state()
        with open('ig_login.json', 'w') as f:
            f.write(json.dumps(state))
        print(f'Loged in as {username}')
        page.wait_for_timeout(120000)
        browser.close()

def main(username):
    print(f'Checking {username}')
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(storage_state='ig_login.json')
        page = context.new_page()
        url = f'https://instagram.com/{username}'
        page.goto(url)
        page.wait_for_timeout(5000)
        content = page.content()
        html = HTMLParser(content)
        try:
            name = html.css_first('div.x6s0dn4 a h2').text(strip=True)
            with open('valid_name.txt', 'a') as f:
                f.write(f'{name}\n')
            print(f'{name} is valid! ❤️❤️❤️')
            print(url,'\n')
        except AttributeError as e:
            print(f'{username} is not valid! ❌❌❌')
            print(url,'\n')
            
        page.wait_for_timeout(1000)
        browser.close()

# Get the username list from username.txt
def get_username():
    with open('username.txt', 'r') as f:
        return f.readlines()


if __name__ == "__main__":
    is_new_id = input('Add new account? Y/N: ').lower()
    usernames = get_username()
    
    if is_new_id == 'y':
        # username = input('USERNAME: ')
        # password = input('PASSWORD: ')
        username = 'gary_lefevre_2296'
        password = '4Du5fBGzVTY7v7b'
        ig_login(username, password)
    
    for user_name in usernames:
        main(user_name.strip())