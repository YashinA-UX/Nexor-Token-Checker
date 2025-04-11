import discord
import asyncio
from termcolor import colored
import os

BANNER = colored("""
███╗   ██╗███████╗██╗  ██╗ ██████╗ ██████╗
████╗  ██║██╔════╝╚██╗██╔╝██╔═══██╗██╔══██╗
██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║██████╔╝
██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║██╔══██╗
██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝██║  ██║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
""", 'magenta', attrs=['bold'])

AUTHOR_INFO = colored("Made by Zeynix / discord.gg/AMGcrbwv", 'grey')

MENU = colored("""
[1] Token Checker
""", 'cyan') + colored("""

[ << x Exit ] [ EXITS ]
""", 'grey')

async def check_token(token):
    try:
        client = discord.Client()
        await client.login(token)
        await client.close()
        return colored("Valid", 'green')
    except discord.errors.LoginFailure:
        return colored("Invalid token: Authentication failed (incorrect token).", 'red')
    except discord.errors.HTTPException as e:
        if e.status == 401:
            return colored("Invalid token: Authentication failed (unauthorized).", 'red')
        elif e.status == 403:
            return colored("Invalid token: Account/token is limited or forbidden.", 'yellow')
        else:
            return colored(f"Invalid token: Discord API error ({e}).", 'yellow')
    except TypeError:
        return colored("Invalid token: Not a valid Discord token format.", 'red')
    except Exception as e:
        return colored(f"Invalid token: An unexpected error occurred ({e}).", 'yellow')

async def token_checker():
    print(colored("\n--- Token Checker ---", 'cyan'))
    try:
        with open("tokens.txt", "r") as f:
            tokens = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(colored("Error: tokens.txt not found.", 'red'))
        return

    if not tokens:
        print(colored("You do not have discord tokens in the tokens.txt!", 'yellow'))
        return

    print("Checking tokens...\n")
    for token in tokens:
        status = await check_token(token)
        print(f"Token: {token}...  Status: {status}")
    print(colored("\nToken checking complete.", 'cyan'))
    input(colored("Press Enter to return to the menu...", 'grey')) # Keep console open

async def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear') # Clear the console
        print(BANNER)
        print(AUTHOR_INFO)
        print(MENU)
        option = input(colored("Select an option: ", 'cyan')).strip().lower()
        if option == "1" or option == "token checker":
            await token_checker()
        elif option == "<< x exit" or option == "exit":
            break
        else:
            print(colored("Invalid option. Please select a valid option.", 'red'))
            input(colored("Press Enter to continue...", 'grey'))

if __name__ == "__main__":
    asyncio.run(main())