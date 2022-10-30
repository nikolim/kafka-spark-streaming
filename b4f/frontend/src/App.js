import { useEffect, useState } from 'react';
import Plot from './components/plot';
import io from 'socket.io-client';

function App() {

  const [btcPrices, setBtcPrices] = useState([]);
  const [hashRates, setHashRates] = useState([]);
  const [corrs, setCorrs] = useState([]);

  const appendBtcPrice = (price) => setBtcPrices((prices) => [...prices, price].slice(-20));
  const appendHashRate = (hashRate) => setHashRates((hashRates) => [...hashRates, hashRate].slice(-20));
  const appendCorr = (corr) => setCorrs((corrs) => [...corrs, corr].slice(-20));

  useEffect(() => {
    const socket = io('http://localhost:5000');
    socket.on('btc', (data) => {
      appendBtcPrice(data.price);
      appendHashRate(data.hash_rate);
      appendCorr(data.corr);
    }
    )
  }, []);


  return (
    <div className="h-screen bg-gray-800 grid place-items-center">
      <div>
        <h1 className="text-5xl text-white text-center pb-24">Bitcoin Streaming Analysis</h1>
        <div className="flex">
          <div className="flex flex-col items-center max-w-[30%]">
            <h1 className="text-4xl text-white"> Bitcoin price</h1>
            <Plot data={btcPrices} color={"#1a237e"} />
            <div className="text-xl text-white"> {btcPrices[btcPrices.length - 1]}$</div>
          </div>
          <div className="flex flex-col items-center max-w-[30%]">
            <h1 className="text-4xl text-white"> Hashrate </h1>
            <Plot data={hashRates} color={"#7b1fa2"} />
            <div className="text-xl text-white"> {hashRates[hashRates.length - 1]} EH/s</div>
          </div>
          <div className="flex flex-col items-center max-w-[30%]">
            <h1 className="text-4xl text-white"> Correlation </h1>
            <Plot data={corrs} color={"#f06292"} />
            <div className="text-xl text-white"> {btcPrices[btcPrices.length - 1]} </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
