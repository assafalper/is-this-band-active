import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import SubmitBand from './pages/SubmitBand';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/submit" element={<SubmitBand />} />
    </Routes>
  );
}
