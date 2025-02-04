import requests
from bs4 import BeautifulSoup
import os
import time
import tkinter as tk
from tkinter import ttk


def get_podcast_url():
    def on_submit():
        global podcast_url
        podcast_url = url_entry.get()
        root.quit()
        root.destroy()
    
    root = tk.Tk()
    root.title("skpodcasty podcast downloader")
    
    # Center window
    window_width = 500
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    url_label = ttk.Label(root, text="Zadajte URL adresu podcastu zo skpodcasty.sk:")
    url_label.pack(pady=10)
    
    url_entry = ttk.Entry(root, width=50)
    url_entry.pack(pady=10)
    
    submit_btn = ttk.Button(root, text="Stiahnuť", command=on_submit)
    submit_btn.pack(pady=10)
    
    root.mainloop()
    return podcast_url


def get_page_count(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    page_links = soup.select('a.page-numbers')
    
    if not page_links:
        return 1
        
    page_numbers = []
    for link in page_links:
        try:
            text = link.text.strip()
            if text.isdigit():
                page_numbers.append(int(text))
        except ValueError:
            continue
            
    return max(page_numbers) if page_numbers else 1


def count_total_episodes(base_url, page_count):
    total_episodes = 0
    
    for page in range(1, page_count + 1):
        # Construct the URL for the current page
        url = f"{base_url}/epage/{page}/" if page > 1 else base_url
        print(f"Počítam epizódy na stránke: {url}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all episode links on this page
            episode_links = [
                a['href'] for a in soup.find_all('a', href=True)
                if '/epizoda/' in a['href']
            ]
            
            # Add number of episodes found on this page
            total_episodes += len(episode_links)
            
        except requests.RequestException as e:
            print(f"Chyba pri počítaní epizód na stránke {url}: {e}")
    
    print(f"Celkový počet nájdených epizód: {total_episodes}")
    return total_episodes


def download_audio(url, counter, episode_id, download_folder, total_episodes, base_url):
    try:
        podcast_name = base_url.rstrip('/').split('/')[-1]
        total_digits = len(str(total_episodes))
        counter_str = str(counter).zfill(total_digits)
        
        # Create a filename using podcast name, counter (with leading zeros) and episode identifier
        filename = f"{podcast_name}_{counter_str}_{episode_id}.mp3"
        file_path = os.path.join(download_folder, filename)

        print(f"Sťahovanie: {url} -> {filename}")

        # Fetch the MP3 file and save it to disk
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, 'wb') as f:
            # Download in chunks to avoid memory overload
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Úspešne stiahnuté: {filename}")

    except requests.RequestException as e:
        print(f"Chyba pri sťahovaní {url}: {e}")


def extract_and_download_audio_links(base_url, page_count, download_folder):
    total_episodes = count_total_episodes(base_url, page_count)
    counter = total_episodes

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for page in range(1, page_count + 1):
        # Construct the URL for the current page
        url = f"{base_url}/epage/{page}/" if page > 1 else base_url
        print(f"Získavanie: {url}")

        try:
            # Fetch the page content
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all episode links
            episode_links = [
                a['href'] for a in soup.find_all('a', href=True)
                if '/epizoda/' in a['href']
            ]

            for episode_link in episode_links:
                print(f"Spracovávanie epizódy: {episode_link}")
                try:
                    episode_response = requests.get(episode_link)
                    episode_response.raise_for_status()
                    episode_soup = BeautifulSoup(episode_response.text, 'html.parser')

                    # Extract audio src attributes from <audio> tags
                    audio_tags = episode_soup.find_all('audio')

                    for audio in audio_tags:
                                            
                        # Extract the 'href' attribute from the <a> tag, if present
                        a_tag = audio.find('a')
                        if a_tag and 'href' in a_tag.attrs:
                            audio_href = a_tag['href']
                            print(f"Nájdený MP3 link: {audio_href}")

                            episode_id = episode_link.split("/epizoda/")[1].strip("/")
                            
                            download_audio(audio_href, counter, episode_id, download_folder, total_episodes, base_url)

                            # Decrement counter after each download
                            counter -= 1

                            # Sleep for a short time to avoid server overload
                            time.sleep(1)

                except requests.RequestException as e:
                    print(f"Chyba pri získavaní epizódy {episode_link}: {e}")

        except requests.RequestException as e:
            print(f"Chyba pri získavaní stránky {url}: {e}")


if __name__ == "__main__":
    try:
        base_url = get_podcast_url()
        page_count = get_page_count(base_url)
        
        # Extract podcast name for folder name
        download_folder = base_url.rstrip('/').split('/')[-1]
        
        print(f"Sťahujem podcast z: {base_url}")
        print(f"Počet stránok: {page_count}")
        
        extract_and_download_audio_links(base_url, page_count, download_folder)
        
    except Exception as e:
        print(f"Nastala chyba: {e}")

