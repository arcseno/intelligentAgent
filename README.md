## About me
Hi! I'm a Data Science & AI student at **State University of Londrina (UEL)** and this project was developed for the **Artificial Intelligence** course. It consists of an **Intelligent Agent** capable of playing the Hangman game, featuring autonomous decision-making, environment perception, and continuous learning capabilities.

---

# 🕵️‍♂️ Intelligent Hangman Agent

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)
![AI](https://img.shields.io/badge/Focus-Artificial%20Intelligence-orange?style=for-the-badge)

An autonomous agent designed to play the classic Hangman game. It uses statistical logic to guess letters and **learns new words** every time it loses, storing them in a persistent memory.

## 🧠 How it Works

The agent follows a cognitive cycle to maximize its winning chances:

1.  **Perception:** It asks for the word length and creates a visual mask (e.g., `_ _ _ _`).
2.  **Filtering:** It analyzes its internal database (`conhecimento.txt`) and keeps only the words that fit the current pattern and length.
3.  **Decision Making:**
    * Calculates the frequency of letters in the remaining candidate words.
    * Picks the letter with the highest probability of appearing.
    * If only one word remains, it attempts to solve the whole word immediately ("All-in").
4.  **Learning:** If the agent fails, it asks for the correct word and saves it to its database for future games.

## ✨ Key Features

* **Persistent Memory:** Uses a text file to store knowledge. The more you play, the smarter it gets.
* **Robust Input Handling:** Sanitizes user inputs and prevents crashes from invalid data.
* **Statistical Heuristics:** Doesn't guess randomly; it calculates the best possible move based on letter frequency.
* **Fallback Mechanism:** If the agent doesn't know any word that fits, it uses a fallback strategy based on the most common letters in the Portuguese language (`aeios...`).

## 🚀 How to Run

1.  Clone the repository:
    ```bash
    git clone https://github.com/arcseno/intelligentAgent.git
    ```
2.  Navigate to the folder:
    ```bash
    cd intelligentAgent
    ```
3.  Run the agent:
    ```bash
    python agent.py
    ```

## 🛠️ Technologies

* **Language:** Python 3
* **Concepts:** OOP (Object-Oriented Programming), File Manipulation, Algorithms Optimizations.

