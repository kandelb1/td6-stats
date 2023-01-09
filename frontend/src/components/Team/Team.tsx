import './Team.scss';
import { useNavigate, useParams, useLoaderData } from "react-router-dom"
import { team, teamInfo, player } from '../../Types';
import { useState, useEffect } from "react";
import axios from 'axios';

interface IProps {

}

export default function Team(props: IProps) {

  const { teamId } = useParams();
  const [teamInfo, setTeamInfo] = useState<teamInfo>();
  const navigate = useNavigate();

  useEffect(() => {
    // we have a teamid, need to grab the team from that
    fetchTeamInfo();
  }, []);

  async function fetchTeamInfo(): Promise<void> {
    if(teamId != undefined) {
      let res = await axios.get(`http://localhost:3001/teams/${teamId}`);
      console.log(res.data);
      setTeamInfo(res.data);
    }
  }
  
  function getScoreText(score: number, opponentScore: number): JSX.Element {
    let className = 'primary';
    let winText = 'tie';
    if(score > opponentScore) {
      className = 'ql2';
      winText = 'win';
    }else if (score < opponentScore) {
      className = 'ql1';
      winText = 'loss';
    }

    let answer = 
    <p>
      <span className={className}>{score} </span>
      to
      <span> {opponentScore} </span>
      <span className={className}>({winText})</span>
    </p>
    return answer;
  }

  function handleClick(gameId: number): void {
    navigate(`/game/${gameId}`);
  }

  return (
    <>
    {
      (teamInfo == undefined)
      ? <p><span className='error'>Error</span> loading data for team id {teamId}</p>
      :
      <div className='team'>
        <div className='header'>
          <h1 className='primary'><span style={{color: '#E8E9ED'}}>Rank #4.</span> {teamInfo.team_name}</h1>
          <p>Captain <span className='secondary'>{teamInfo.captain}</span></p>
          <p>Overall W/L: <span className='ql2'>35/28</span></p>
        </div>
        <div className='split'>
          <div className='roster'>
            <h1>Roster</h1>
            <p>ADD BOOTSRAP SO I CAN PUT COOL OVERLAYS THAT APPEAR WHEN YOU HOVER OVER A PLAYER'S NAME</p>
            <ul>
              {teamInfo.players.map(player => {
                return (
                  <li>{(player.round == 0) ? 'Cap' : player.round}. <span dangerouslySetInnerHTML={{ __html: player.name }}></span></li>
                  // <li>
                  //   <select>
                  //     {player.aliases.map(alias => {
                  //       return (
                  //         <option><span dangerouslySetInnerHTML={{ __html: player.name }}/></option>
                  //       )
                  //     })}
                  //   </select>
                  // </li>
                );
              })}
            </ul>
          </div>
          <div className='matches-container'>
            {/* we can still put stuff here */ }
            <div className='matches'>
              <h1>Matches</h1>
              {teamInfo.matches.map(match => {
                return (
                  <div className='match'>
                    <h1><span className='secondary'>Week {match.week}</span> vs. <span className='secondary'>{match.enemy}</span></h1>
                    <p className='match-score'>{getScoreText(match.score, match.enemy_score)}</p>
                    <div className='match-header'>
                      <h2>Games:</h2>
                      <p className='secondary'>(click to view)</p>
                    </div>
                    <div className='game-list'>
                      {teamInfo.games.filter(g => g.week == match.week).map(game => {
                        return (
                          <div 
                            className='game'
                            onClick={() => handleClick(game.id)}>
                            <p className='secondary'>{game.map}: <span className={(game.score > game.enemy_score) ? 'ql2' : 'ql1'}>{game.score}</span>-<span className='secondary'>{game.enemy_score}</span></p>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </div>
    }
    </>
  )
}