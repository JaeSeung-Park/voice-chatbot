import React, { useEffect, useState } from 'react';
import Header from './components/Header/Header';
// import PromptSubmit from './components/PromptSubmit/PromptSubmit';
import Message from './components/Message/Message';
import Loader from './components/Common/Loader';
import Chatbot from './components/jsx/jsx';

interface PromptData {
  prompt: string | null;
  bot: any;
}

function App() {
  const [list, setList] = useState<PromptData[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  
  useEffect(() => {
    console.log(isLoading, 'list');
  }, [isLoading]);
  
  return (
    <div className='flex h-[80vh] justify-center flex-col items-center'>
      <div className='border-black relative border-2 h-[667px] border- w-[375px] bg-[#ECECEC] mx-auto rounded-md'>
        <Header />
        <ul className='py-3 px-2 h-[587px] overflow-y-auto'>
          {list.map(item => (
            <Message key={`${Math.random()}-${Date.now()}`} item={item} />
          ))}
          <li>
            {isLoading && <div className='flex justify-center items-center'><Loader /></div>}
          </li>
        </ul>
        <Chatbot isLoading={isLoading} setIsLoading={setIsLoading} setList={setList} list={list} />
      </div>
    </div>
  );
}

export default App;