import React, { useEffect, useState } from 'react';
import { match, team } from '../Types';
import './Main.scss';
import { BrowserRouter as Router, Route, Routes, createBrowserRouter, RouterProvider } from 'react-router-dom';
import Home from './Home/Home';
import Teams from './Teams/Teams';
import Team from '../components/Team/Team';
import axios from 'axios';

interface IProps {

}



export default function Main(props: IProps) {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/teams" element={<Teams />} />
        <Route path="/teams/:teamId" element={<Team />} />
      </Routes>
    </Router>
  )
}