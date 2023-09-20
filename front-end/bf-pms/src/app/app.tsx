// eslint-disable-next-line @typescript-eslint/no-unused-vars
import styles from './app.module.css';
import { BrowserRouter, Routes,Route } from 'react-router-dom';
import  { ClientList,Clients } from 'clients'

function Home() {
  return <h1>Home</h1>;
}

export function App() {
  return (
    <BrowserRouter>
      
      <Routes>
        <Route path='/d' element={<Home/>} ></Route>
        <Route path='/c' element={<Clients/>} > </Route>
        <Route path='/' element={<ClientList/>} > </Route>

      </Routes>

    </BrowserRouter>
  );
}

export default App;
