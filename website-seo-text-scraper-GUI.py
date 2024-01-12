#Offensive Programming - week 5 - SEO WORD SCRAPER 
import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def count_words(text):
    word_list = text.split()
    return len(word_list)

def count_words_in_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    return count_words(text)

def display_visible_words(soup):
    visible_words = []
    for tag in soup.find_all(string=True):
        if tag.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            visible_words.extend(tag.split())
    return visible_words

def display_invisible_words(soup):
    invisible_words = []
    for tag in soup.find_all(string=True):
        if tag.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            invisible_words.extend(tag.split())
    return invisible_words

def write_words_to_txt(file_name, words):
    with open(file_name, 'w') as file:
        for word in words:
            file.write(word + '\n')

def fetch_and_analyze():
    url = url_entry.get()
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    visible_words = display_visible_words(soup)
    invisible_words = display_invisible_words(soup)
    
    results_text.delete(1.0, tk.END)
    results_text.insert(tk.END, f"Visible Words: {len(visible_words)}\n")
    results_text.insert(tk.END, f"Invisible Words: {len(invisible_words)}\n")

def get_visible_text(soup):
    visible_text = []
    for tag in soup.find_all(string=True):
        if tag.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            visible_text.append(tag.strip())
    return '\n'.join(filter(None, visible_text))

def export_results():
    url = url_entry.get()
    domain = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    visible_words = display_visible_words(soup)
    invisible_words = display_invisible_words(soup)
    visible_text = get_visible_text(soup)

    with open(f'{domain}-visible-words.txt', 'w') as file:
        file.write(f"Number of Visible Words: {len(visible_words)}\n")
        file.writelines([word + '\n' for word in visible_words])
    
    with open(f'{domain}-invisible-words.txt', 'w') as file:
        file.write(f"Number of Invisible Words: {len(invisible_words)}\n")
        file.writelines([word + '\n' for word in invisible_words])

    with open(f'{domain}-visible-text.txt', 'w') as file:
        file.write(visible_text)
    
    messagebox.showinfo("Export Successful", f"Visible words: {len(visible_words)}, Invisible words: {len(invisible_words)}, and Visible text exported to files for {domain}")

root = tk.Tk()
root.title("Word & Text Extractor")

tk.Label(root, text="Enter URL:").pack(padx=10, pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(padx=10)

fetch_button = tk.Button(root, text="Fetch and Analyze", command=fetch_and_analyze)
fetch_button.pack(pady=5)

results_text = scrolledtext.ScrolledText(root, width=70, height=15, wrap=tk.WORD)
results_text.pack(padx=10, pady=5)

export_button = tk.Button(root, text="Export Results", command=export_results)
export_button.pack(pady=5)

copyright_label = tk.Label(root, text="\u00A9 2024 DutchJinn.com", font="Play 16 bold", fg="darkorange")
copyright_label.pack(side=tk.BOTTOM, pady=5)

root.mainloop()

print("\n\033[95mCopyright 2024 DutchJinn.com\033[0m\n")
