import valve.source.a2s

# SERVER_ADDRESS = '37.230.162.41:27017'
# ip_addresses = ['79.143.20.74:26215', '79.143.20.74:26065']


def get_info(address):
    address = [int(x) if x.isdigit() else x for x in address.split(':')]
    with valve.source.a2s.ServerQuerier(address) as server:
        players_online = {}
        players = server.players()
        for player in players["players"]:
            if player['name'] == 'CYBERSHOKE.NET':
                continue
            players_online[player['name']] = player['score']
        players_count = players['player_count']
    return (dict(
        sorted(players_online.items(), key=lambda item: item[1],
               reverse=True)), players_count - 1)


# print(get_players_count(SERVER_ADDRESS))