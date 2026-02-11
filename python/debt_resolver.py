"""
Calculate who should pay who when caching out a poker game
"""


from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def main():
    count = int(input("How many players? "))
    players: list[tuple[str, int]] = []
    for i in range(count):
        name = input(f"Player {i+1} name: ")
        balance = int(input(f"Player {i+1} final balance: "))
        players.append((name, balance))
    
    #players = [("P1", -50),("P5",-30), ("P2", 25), ("P3", 40), ("P4", 15)]
    
    balance_sum = sum(balance for _, balance in players)
    if balance_sum != 0:
        print("balances do not sum to zero, the mistake's size:", balance_sum)
        cont = input("Continue Anyway? (THIS MEANS THAT NOT ALL DEBT ARE RESOLVED) (y/n) ")
        if cont != "y":
            return
        print("Continuing....")
    
    players.sort(key=lambda x: x[1])
    # sort players by balance, lowest first
    transfers: list[tuple[str, str, int]] = [] # list of (from, to, amount) (Ideally should be a struct but this is python)
    poor_index = 0
    rich_index = count - 1
    while poor_index < rich_index:
        poor_name, poor_balance = players[poor_index]
        rich_name, rich_balance = players[rich_index]
        transfer_amount = min(-poor_balance, rich_balance)
        transfers.append((poor_name, rich_name, transfer_amount))
        players[poor_index] = (poor_name, poor_balance + transfer_amount) # Tuples are immutable so we have to create new ones
        players[rich_index] = (rich_name, rich_balance - transfer_amount)
        if players[poor_index][1] == 0: # poor player pain all his debt
            poor_index += 1
        if players[rich_index][1] == 0: # rich player got all his money
            rich_index -= 1
    
    transfers = [t for t in transfers if t[2] > 0]
    
    print("Transfers:")
    for from_player, to_player, amount in transfers:
        print(f"{from_player} pays {to_player} ${amount}")
    if balance_sum:
        print("Again, this is missing - ", abs(balance_sum))


if __name__ == "__main__":
    app.run(debug=True)