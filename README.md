# 🎉 CheckEasy: The Lightning-Fast LLM Detector 🕵️‍♀️

**CheckEasy** is your trusty sidekick for sniffing out AI-written homework, essays, or Slack messages. Powered by a multi-agent OpenAI-based system, CheckEasy doesn’t just give you a score—it hands you the juicy evidence behind every verdict. Perfect for professors, TAs, or curious humans who want to check if their colleague really wrote that email. 😉

---

## 🚀 Features

* **LLM Score (0–100)**: How likely is this text an AI spin-off? 100 = *definitely* ChatGPT, 0 = *definitely* Shakespeare.
* **Evidence Extractor**: Bullet-list justification for each score. No more “because I said so.” 📋
* **Batch Processing**: Upload entire XLSX/CSV files of student responses and questions; get back detailed reports & pivot tables.
* **Streamlit UI**: Slick sidebar config, progress bars, and expandable result cards. Look, Ma—no console! 💅
* **Downloadable Reports**: Grab CSVs for detailed & summary results—shareable in meetings or with academic integrity committees.

---

## 🔧 Installation

1. Clone this repo:

   ```bash
   git clone https://github.com/Subhagatoadak/LLMChecker.git
   cd checkeasy
   ```
2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```


---

## 🏃 Usage

1. Launch the app:

   ```bash
   streamlit run app.py
   ```
2. In the sidebar:

   * Enter your **OpenAI API Key**
   * Paste your **Detection Instructions** (system prompt)
3. Upload:

   * **Student responses** (XLSX or CSV)
   * **Questions** file (XLSX or CSV)
4. Hit **Run LLM Checker** and watch the magic happen:

   * Progress bar to track multi-agent detective work
   * Expand each student’s results for scores & evidence
   * Download detailed & pivoted CSV reports

---

## 🤔 FAQ & Pro Tips

* **Q**: I keep getting `Mismatch: number of answers does not match number of questions.`
  **A**: Make sure your responses file’s first column is the student name, followed by answers in the exact same order as your questions file.

* **Q**: How do I tune sensitivity?
  **A**: Tweak your system prompt (detection instructions)! More aggressive wording = higher chance to flag AI.

* **Tip**: Use a low temperature (`temperature=0`) for deterministic scores, or experiment with `0.2`–`0.5` for a fuzzy “gut feeling.”

---

## 🤝 Contributing

1. Fork it!
2. Create a branch: `git checkout -b feature/cool-new-check`
3. Commit your changes: `git commit -am 'Add detective hat emoji'`
4. Push to the branch: `git push origin feature/cool-new-check`
5. Open a Pull Request—bonus points for GIFs. 🦄

---

## 📜 License

MIT © \[Subhagato Adak]

---

> “With CheckEasy, every homework assignment is a game of Clue—and AI is always Colonel Mustard in the lounge.” 💼🔍
