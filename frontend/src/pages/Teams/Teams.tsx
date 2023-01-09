import './Teams.scss';
import { useLoaderData, useNavigate } from 'react-router-dom';
import { team } from '../../Types';
import axios from 'axios';
import { useEffect, useState } from 'react';

interface IProps {

}

export default function Teams(props: IProps) {

  const navigate = useNavigate();
  const [teamList, setTeamList] = useState<team[]>([]);

  useEffect(() => {
    fetchTeams();
  }, []);

  async function fetchTeams(): Promise<void> {
    let x = await axios.get('http://localhost:3001/teams');
    console.log(x.data.rows);
    setTeamList(x.data.rows);
  }
  
  function handleClick(teamId: number): void {
    console.log(`${teamId} clicked`);
    navigate(`/teams/${teamId}`);
  }

  return (
    <div className='teams-list'>
      {(teamList.length == 0)
      ? <p>Fetching teams...</p>
      :
      teamList.map(team => {
        return (
          <div
            className='team'
            onClick={() => handleClick(team.id)}>
            <h1>{team.captain}</h1>
            <p>{team.name}</p>
          </div>
        )
      })}
    </div>
  )
}