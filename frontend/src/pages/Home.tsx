import { Link } from 'react-router-dom';
import './Home.scss';

interface IProps {

}

export default function Home(props: IProps) {

  const weekList = [1, 2, 3, 4, 5, 6, 7, 8]

  function goToWeek(weekNum: number) {
    console.log('navigating to week ' + weekNum);
  }

  return (
    <div className='home'>
      <p>hi this is Home</p>
      <div className='week-list'>
        {weekList.map((num) => {
          return (
            <div className='week'>
              <Link to={`week/${num}`}>Week {num}</Link>
            </div>
          )
        })}
      </div>
    </div>
  )
}