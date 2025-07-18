import { Routes, Route } from 'react-router-dom';
import Home from './pages/home';
import SubmitBand from './pages/SubmitBand';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<home />} />
      <Route path="/submit" element={<SubmitBand />} />
    </Routes>
  );
}
