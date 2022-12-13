import React from 'react';
import { Match } from '../Types';
import './Main.scss';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Home';
import Week from './Week';

interface IProps {

}

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

const games = [match1, match2, match3];

export default function Main(props: IProps) {

  return (
    <div className='main'>
      <p>hi this is Main</p>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="week">
            <Route path=":weekNum" element={<Week />} />
          </Route> 
        </Routes>
      </Router>
    </div>
  )
}