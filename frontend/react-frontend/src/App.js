import logo from './logo.svg';
import {useEffect, useState} from 'react';
import './App.css';

function App() {

  const [btcPrice, setBtcPrice] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setBtcPrice(data.price);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>The current bitcoin price is {btcPrice}.</p>
      </header>
    </div>
  );
}

export default App;
