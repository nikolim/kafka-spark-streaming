import logo from './logo.svg';
import { useEffect, useState } from 'react';
import Plot from './components/plot';
import './App.css';
import io from 'socket.io-client';

function App() {

  const [btcPrices, setBtcPrices] = useState([]);

  const appendBtcPrice = (price) => {
    setBtcPrices((prices) => [price, ...prices].slice(0, 100));
  };

  useEffect(() => {
    const socket = io('http://localhost:5000');
      socket.on('btc', (data) => appendBtcPrice(data.price)
    )}
   ,[]);

  return (
    <div className="App">
      <header className="App-header">
        <Plot data={btcPrices} />
      </header>
    </div>
  );
}

export default App;
