import requests
import threading
import subprocess
import time

try:
    import colorama
    import pyfiglet
except ImportError:
    subprocess.check_call(["python", '-m', 'pip', 'install', 'colorama', 'pyfiglet'])
    import colorama
    import pyfiglet

colorama.init()

ascii_art = pyfiglet.figlet_format("Welcome to BDIX tester")
print(colorama.Fore.GREEN + ascii_art + colorama.Style.RESET_ALL)

def check_link(link, processed, total):
    try:
        response = requests.get(link, timeout=5)
        if response.status_code == 200:
            with open('alive.txt', 'a') as f:
                f.write(link + '\n')
        else:
            with open('dead.txt', 'a') as f:
                f.write(link + '\n')
    except:
        with open('dead.txt', 'a') as f:
            f.write(link + '\n')

    processed.append(link)
    print(colorama.Fore.RED + f"{len(processed)}/{total} links processed." + colorama.Style.RESET_ALL)

filename = input('Enter the filename : ')

try:
    with open(filename, 'r') as f:
        links = f.read().splitlines()
except FileNotFoundError:
    print("Please input a valid text file")
    exit()

num_threads = int(input('Enter the number of threads to use: '))

total_links = len(links)
processed_links = []

start_time = time.time()

for i in range(0, total_links, num_threads):
    threads = []
    for j in range(i, min(i+num_threads, total_links)):
        link = links[j]
        thread = threading.Thread(target=check_link, args=(link, processed_links, total_links))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

end_time = time.time()

print(f'All links processed in {end_time-start_time:.2f} seconds.')
