import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import ReviewSubmissions from "./pages/ReviewSubmissions";
import SubmitBand from './pages/SubmitBand';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/submit" element={<SubmitBand />} />
      <Route path="/admin/review" element={<ReviewSubmissions />} />
      
    </Routes>
  );
}
