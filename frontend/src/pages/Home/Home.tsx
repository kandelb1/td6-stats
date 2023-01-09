import { Link } from 'react-router-dom';
import './Home.scss';

interface IProps {

}

export default function Home(props: IProps) {
  return (
    <div className='home'>
      <h1>Home</h1>
      <p>Browse matches by <Link to="/teams">teams</Link>, week, -something-, -something- </p>
    </div>
  )
}