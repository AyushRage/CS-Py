from enum import Enum

class GameStateCode(Enum):
    INVALID = -1
    ENDGAME = 0
    VALID = 1

class Payload:

    def __init__(self, payload):
        self.map = payload['map']
        self.player = payload['player']
        self.client = payload['provider']
        self.round = payload['round']
        self.previous = payload['previously']
        self.gamestate_code = self.check_payload()


    def check_payload(self):
        try:
            if self.player['activity'] == 'playing' and self.map['mode'] == 'competitive':
                map_phase = self.map['phase']
                if map_phase == 'live' or map_phase == 'intermission' or map_phase == 'gameover':
                    round_phase = self.round['phase']
                    prev_round_phase = self.previous['round']['phase']
                    user_id = self.client['steamid']
                    curr_player_id = self.player['steamid']

                    if user_id == curr_player_id:
                        if round_phase == 'over' and prev_round_phase == 'live':
                            return GameStateCode.VALID
                        elif (round_phase == 'live' and self.player['state']['health'] == 0
                              and self.previous['player']['state']['health'] > 0):
                            return GameStateCode.VALID

                    else:
                        if (map_phase == 'gameover' and round_phase == 'over'
                            and prev_round_phase == 'live'):
                            return GameStateCode.ENDGAME

            return GameStateCode.INVALID
        except(TypeError, ValueError):
            return GameStateCode.INVALID


    def insert_data_to_db(self, player_db):
        if self.gamestate_code == GameStateCode.INVALID:
            return -1
        elif self.gamestate_code == GameStateCode.VALID:
            player_team = None if 'team' not in self.player else self.player['team']
            match_stats = self.player['match_stats']
            player_state = self.player['state']

            data_entry = (int(self.client['timestamp']),
                                 self.map['name'], self.map['phase'],
                                 self.player['name'], player_team,
                                 int(match_stats['kills']),
                                 int(match_stats['assists']),
                                 int(match_stats['deaths']),
                                 int(match_stats['mvps']),
                                 int(match_stats['score']),
                                 int(player_state['equip_value']),
                                 int(player_state['round_kills']),
                                 int(player_state['round_killhs']))

            sql_insert = ''' INSERT INTO per_round_data(Time, Map, "Map Status", "Player Name", "Player Team", 
                                                              Kills, Assists, Deaths, MVPs, Score, "Current Equip. Value", 
                                                              "Round Kills", "Round HS Kills") 
                                                              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
            # TODO: Refactor to include checks about previous entries, look in main.py for reference.

        else:
            data_entry = (int(self.client['timestamp']),
                                 self.map['name'], self.map['phase'])

            sql_insert = ''' INSERT INTO per_round_data(Time, Map, "Map Status") VALUES(?, ?, ?) '''

            # TODO: Refactor to include checks about previous entries, look in main.py for reference.

        player_db.cursor().execute(sql_insert, data_entry)
        return 0

