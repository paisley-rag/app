import "./App.css";
import ChatContainer from "./components/ChatContainer.tsx";
import UploadForm from "./components/UploadForm.tsx";
import Sidenav from './components/Sidenav.tsx';
import Evals from './components/Evals.tsx';
import { Route, Switch } from 'wouter';

function App() {

  return (
    <div className="app">
      <Sidenav />
      <Switch>
        <Route path='/upload' component={UploadForm} />
        <Route path='/chat' component={ChatContainer} />
        <Route path='/evals' component={Evals} />
      </Switch>
    </div>
  );
}

export default App;
