import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Match } from '../Types';
import './Week.scss';


const match1: Match = {
  redTeamName: '+back',
  redTeamCaptain: 'Flood',
  redTeamScore: 10,
  blueTeamName: 'FAT',
  blueTeamCaptain: 'Skinner',
  blueTeamScore: 8,
  serverName: 'Cocaine, Bad Bitches and Alcohol TX',
  week: 1,
  mapNum: 1,
  mapName: 'quarantine',
};

const match2: Match = {
  redTeamName: 'QLCAT',
  redTeamCaptain: 'cows',
  redTeamScore: 3,
  blueTeamName: 'Who Spec\'n?',
  blueTeamCaptain: 'doc',
  blueTeamScore: 10,
  serverName: 'Thunderdome 6 TX 1',
  week: 1,
  mapNum: 2,
  mapName: 'campgrounds',
};

const match3: Match = {
  redTeamName: 'Anime Babes',
  redTeamCaptain: 'STO1C',
  redTeamScore: 10,
  blueTeamName: 'Spit on Them Father',
  blueTeamCaptain: 'monster',
  blueTeamScore: 5,
  serverName: 'Thunderdome 6 CHI 1',
  week: 2,
  mapNum: 3,
  mapName: 'overkill',
};

const matches = [match1, match2, match3];

interface IProps {

}

export default function Week(props: IProps) {

  const { weekNum } = useParams();

  // const [matchList, setMatchList] = useState<Match[]>([]);
  const [matchList, setMatchList] = useState<Match[]>(matches);

  useEffect(() => {
      console.log('week component loaded with a weekNum of ' + weekNum);
  });

  function fetchMatchList(weekNum: number) {

  }

  return (
    <div className='match-list'>
      <p>hi this is week {weekNum}</p>
      {matchList.map(match => {
        return (
          <div className='match'>
            <p>{match.redTeamCaptain} vs. {match.blueTeamCaptain}</p>
          </div>          
        )
      })}
    </div>
  )
}