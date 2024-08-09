import { Link } from 'wouter';
import classes from './Sidenav.module.css';

const Sidenav = () => {
  const assignClasses = (active: boolean) => {
    let css = [classes.navItem];
    if (active) css.push(classes.active);
    return css.join(' ');
  }

  return (
    <div className={classes.container}>
      <ul>
        <li><Link className={active => assignClasses(active)} href='/upload'>Upload</Link></li>
        <li><Link className={active => assignClasses(active)} href='/chat'>Chat</Link></li>
        <li><Link className={active => assignClasses(active)} href='/evals'>Evals</Link></li>
      </ul>
    </div>
  )
}

export default Sidenav;
