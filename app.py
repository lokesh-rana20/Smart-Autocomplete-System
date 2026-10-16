
from flask import Flask, jsonify, render_template, request
from trie import Trie
from database import (
    get_all_words,
    add_word_to_db,
    increment_search_count,
    get_popular_words
)


app = Flask(__name__)
trie = Trie()

try:
    words = get_all_words()
    for word in words:
        trie.insert(word)
    print(f"Successfully loaded {len(words)} words from MySQL!", flush=True)
except Exception as e:
    print("Database error:", repr(e), flush=True)


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/suggest/<path:prefix>")
def suggest(prefix):
    try:
        suggestions = trie.get_suggestions(prefix)

        counts = {
            word.lower(): count
            for word, count in get_popular_words()
        }

        results = [
            {
                "word": word,
                "count": counts.get(word.lower(), 0)
            }
            for word in suggestions
        ]

        results.sort(key=lambda item: item["count"], reverse=True)

        return jsonify({
            "prefix": prefix,
            "suggestions": results
        })

    except Exception as e:
        print("Suggestion error:", repr(e), flush=True)
        return jsonify({"error": str(e)}), 500


@app.route("/select_word", methods=["POST"])
def select_word():
    data = request.get_json(silent=True) or {}
    word = data.get("word", "")

    if not isinstance(word, str) or not word.strip():
        return jsonify({"message": "Invalid word."}), 400

    word = word.strip()
    print("Received selection:", word, flush=True)

    try:
        increment_search_count(word)
        print("Search count updated:", word, flush=True)
        return jsonify({"message": "Popularity updated."}), 200
    except Exception as e:
        print("Popularity update error:", repr(e), flush=True)
        return jsonify({"message": "Could not update popularity."}), 500


@app.route("/add_word", methods=["POST"])
def add_word():
    data = request.get_json(silent=True) or {}
    word = data.get("word", "")

    if not isinstance(word, str):
        return jsonify({"message": "Invalid word."}), 400

    word = word.strip()

    if not word:
        return jsonify({"message": "Please enter a word."}), 400

    if len(word) > 100:
        return jsonify({"message": "Maximum length is 100 characters."}), 400

    try:
        saved = add_word_to_db(word)

        if not saved:
            return jsonify({"message": "This word already exists!"}), 409

        trie.insert(word)
        return jsonify({"message": f"'{word}' added successfully!"}), 201

    except Exception as e:
        print("Add word error:", repr(e), flush=True)
        return jsonify({
            "message": "Could not save word. Check MySQL connection and table."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
