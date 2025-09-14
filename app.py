from flask import Flask, request, render_template_string
import subprocess
import json
import re

app = Flask(__name__)

# HTML Template with a clean look
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Formula Renderer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h2 { color: #2c3e50; }
        form { margin-bottom: 20px; }
        input[type="text"] {
            padding: 8px;
            width: 300px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            padding: 8px 16px;
            background: #2c3e50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover { background: #34495e; }
        .result {
            margin-top: 20px;
            padding: 15px;
            border-left: 4px solid #2c3e50;
            background: #f9f9f9;
        }
        code { background: #eee; padding: 2px 4px; }
    </style>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async
      src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
    <h2>Formula Renderer</h2>
    <p>Enter a formula name and get its LaTeX form, rendered beautifully.</p>
    <form method="POST">
        <input type="text" name="formula_name" placeholder="e.g. Quadratic Formula" required>
        <button type="submit">Generate</button>
    </form>
    
    {% if latex %}
    <div class="result">
        <h3>Result:</h3>
        <p><strong>LaTeX:</strong> <code>{{ latex }}</code></p>
        <p><strong>Rendered:</strong></p>
        <p>$$ {{ latex }} $$</p>
    </div>
    {% endif %}
</body>
</html>
"""

def query_ollama(prompt: str) -> str:
    """
    Queries the Ollama model and saves raw response for debugging.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", "gemma3:4b"],
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="ignore"
        )
        raw_response = result.stdout.strip()

        # Save raw response for debugging
        with open("gemma_raw_response.txt", "w", encoding="utf-8") as f:
            f.write(raw_response)

        return raw_response
    except Exception as e:
        return json.dumps({"error": str(e)})

def extract_json(text: str) -> dict:
    """
    Extracts the first valid JSON object from text.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format"}
    return {"error": "No JSON found"}

@app.route("/", methods=["GET", "POST"])
def index():
    latex_formula = None
    if request.method == "POST":
        formula_name = request.form.get("formula_name")

        # Strict prompt for Gemma
        prompt = f"""
You are an API. Respond with ONLY valid JSON.
The JSON must have exactly one key: "latex".

Example:
{{"latex": "x = \\\\frac{{-b \\\\pm \\\\sqrt{{b^2 - 4ac}}}}{{2a}}" }}

Now return the formula '{formula_name}' in JSON.
"""

        response = query_ollama(prompt)
        data = extract_json(response)

        if "latex" in data:
            latex_formula = data["latex"]
        else:
            latex_formula = f"Error: Could not parse JSON. See gemma_raw_response.txt."

    return render_template_string(HTML_TEMPLATE, latex=latex_formula)

if __name__ == "__main__":
    app.run(debug=True)
