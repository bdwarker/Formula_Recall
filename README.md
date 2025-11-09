# 📐 Formula Recall

A lightweight Flask web app that takes the **name of a mathematical formula**, queries the **Ollama model (gemma3:4b)**, and returns the **LaTeX representation** of the formula. The result is displayed both as raw LaTeX and as a beautifully rendered formula using MathJax.

---

## 🚀 Features
- Input a formula name (e.g., *Quadratic Formula*).
- Model responds with JSON containing the LaTeX expression.
- App extracts and displays:
  - Raw LaTeX
  - Rendered formula
- Debug-friendly: saves raw model output to `gemma_raw_response.txt`.

---

## 🛠 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/formula-renderer.git
   cd formula-renderer
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows

   pip install -r requirements.txt
   ```

3. Install [Ollama](https://ollama.ai) and pull the model:

   ```bash
   ollama pull gemma3:4b
   ```

---

## ▶️ Usage

Run the app:

```bash
python app.py
```

Open in your browser:
👉 [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## ⚠️ Notes

* Raw responses from Gemma are saved to `gemma_raw_response.txt` for debugging.
* If parsing fails, check that file to inspect the model output.

---

## 🧑‍💻 Author

Made with ❤️ by Mohammed Shaan

---
