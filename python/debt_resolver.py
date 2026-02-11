"""
Calculate who should pay who when cashing out a poker game
"""

import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# -----------------------
# Poker calculation logic
# -----------------------
def calculate_transfers(players):
    # players is a list of (name, balance) tuples
    balance_sum = sum(balance for _, balance in players)

    players = sorted(players, key=lambda x: x[1])
    transfers = []  # list of (from, to, amount) (should be a struct but this is python)

    poor_index = 0
    rich_index = len(players) - 1

    while poor_index < rich_index:
        poor_name, poor_balance = players[poor_index]
        rich_name, rich_balance = players[rich_index]

        transfer_amount = min(-poor_balance, rich_balance)
        transfers.append((poor_name, rich_name, transfer_amount))
        players[poor_index] = (poor_name, poor_balance + transfer_amount)
        players[rich_index] = (rich_name, rich_balance - transfer_amount)

        if players[poor_index][1] == 0:
            poor_index += 1
        if players[rich_index][1] == 0:
            rich_index -= 1

    # Filter out zero transfers
    transfers = [t for t in transfers if t[2] > 0]

    return {
        "transfers": transfers,
        "balance_sum": balance_sum
    }

# -----------------------
# HTML template with dynamic form
# -----------------------
HTML_TEMPLATE = """
<!doctype html>
<title>Poker Cashout Calculator</title>
<h1>Poker Cashout Calculator</h1>

<form method="POST" id="playerForm">
    Number of players: <input type="number" id="playerCount" name="count" min="2" value="{{ count }}"><br><br>

    <div id="playersInputs">
    {% for i in range(count) %}
        Player {{ i+1 }} Name: <input type="text" name="name{{i}}" value="{{ names[i] if names else '' }}">
        Balance: <input type="number" name="balance{{i}}" value="{{ balances[i] if balances else '' }}"><br><br>
    {% endfor %}
    </div>

    <input type="submit" value="Calculate">
</form>

{% if result %}
<h2>Transfers:</h2>
<ul>
{% for from_player, to_player, amount in result['transfers'] %}
    <li>{{ from_player }} pays {{ to_player }} ${{ amount }}</li>
{% endfor %}
</ul>
{% if result['balance_sum'] != 0 %}
<p><strong>Warning:</strong> balances do not sum to zero (sum = {{ result['balance_sum'] }})</p>
{% endif %}
{% endif %}

<script>
// Dynamically update player input fields when the count changes
const countInput = document.getElementById("playerCount");
const playersDiv = document.getElementById("playersInputs");

countInput.addEventListener("change", () => {
    const count = parseInt(countInput.value);
    let html = "";
    for (let i = 0; i < count; i++) {
        html += `Player ${i+1} Name: <input type="text" name="name${i}"> `;
        html += `Balance: <input type="number" name="balance${i}"><br><br>`;
    }
    playersDiv.innerHTML = html;
});
</script>
"""

# -----------------------
# Flask main route
# -----------------------
@app.route("/", methods=["GET", "POST"])
def main():
    result = None
    count = 3  # default number of players
    names = []
    balances = []

    if request.method == "POST":
        count = int(request.form["count"])
        players = []
        for i in range(count):
            name = request.form.get(f"name{i}", f"Player{i+1}")
            balance = int(request.form.get(f"balance{i}", 0))
            names.append(name)
            balances.append(balance)
            players.append((name, balance))
        # Calculate transfers using the function
        result = calculate_transfers(players)

    return render_template_string(
        HTML_TEMPLATE, result=result, count=count, names=names, balances=balances
    )

# -----------------------
# Run Flask app
# -----------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
