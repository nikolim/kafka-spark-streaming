import { useEffect, useState } from 'react';
import Plot from './components/plot';
import io from 'socket.io-client';

function App() {

  const [btcPrices, setBtcPrices] = useState([]);

  const appendBtcPrice = (price) => {
    setBtcPrices((prices) => [price, ...prices].slice(0, 100));
  };

  useEffect(() => {
    const socket = io('http://localhost:5000');
    socket.on('btc', (data) => appendBtcPrice(data.price)
    )
  }
    , []);


  return (
    <div className="App h-screen bg-gray-800 grid place-items-center">
      <h1 className="text-5xl text-white">Bitcoin Streaming Correlation</h1>
      <div className="flex">
        <div className="flex flex-col items-center max-w-[30%]">
          <h1 className="text-4xl text-white"> Bitcoin price</h1>
          <Plot data={btcPrices} color={"#1a237e"} />
          <div className="text-xl text-white"> {btcPrices[btcPrices.length - 1]}$</div>
        </div>
        <div className="flex flex-col items-center max-w-[30%]">
          <h1 className="text-4xl text-white"> Hashrate </h1>
          <Plot data={btcPrices} color={"#7b1fa2"} />
          <div className="text-xl text-white"> {btcPrices[btcPrices.length - 1]} hash/unit</div>
        </div>
        <div className="flex flex-col items-center max-w-[30%]">
          <h1 className="text-4xl text-white"> Correlation </h1>
          <Plot data={btcPrices} color={"#7b1fa2"} />
          <div className="text-xl text-white"> {btcPrices[btcPrices.length - 1]} </div>
        </div>
      </div>
    </div>
  );
}

export default App;
