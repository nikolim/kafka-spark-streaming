import logo from './logo.svg';
import { useEffect, useState } from 'react';
import './App.css';
import io from 'socket.io-client';

function App() {

  const [btcPrice, setBtcPrice] = useState(0);

  useEffect(() => {
    const socket = io('http://localhost:5000');
    socket.on('btc', (data) => setBtcPrice(data.price));
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
