export type Test = {

};

export type game = {
  week: number;
  id: number;
  map: string;
  score: number;
  enemy_score: number;
}

export type match = {
  week: number;
  score: number;
  enemy: string;
  enemy_score: number;
}

export type team = {
  id: number;
  captain: string;
  name: string;
}

export type player = {
  id: number;
  name: string;
  aliases: string[];
  round: number;
}

export type teamInfo = {
  team_name: string;
  captain: string;
  matches: match[];
  games: game[];
  players: player[];
}
