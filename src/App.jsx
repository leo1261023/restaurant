import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import UpTitle from './components/UpTitle'; 
import Host from './components/Host';
import Member from './components/Member';
import Signin from './components/Signin'; // 确保路径和文件名大小写一致
import Rec from './components/Rec';

function App() {
  return (
    <Router>
      <UpTitle />
      <Routes>
        <Route path="/" element={<Host />} />
        <Route path="/member" element={<Member />} />
        <Route path="/signin" element={<Signin />} />
        <Route path='/rec' element={<Rec />} />
      </Routes>
    </Router>
  );
}

export default App;
