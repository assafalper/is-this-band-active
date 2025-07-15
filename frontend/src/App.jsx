import { useState } from 'react';

export default function App() {
  const [bandName, setBandName] = useState('');
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const checkBand = async () => {
    if (!bandName.trim()) return;
    setLoading(true);
    setStatus(null);

    try {
      const res = await fetch(`${process.env.REACT_APP_API_BASE_URL}/band/${encodeURIComponent(bandName)}`);
      if (!res.ok) throw new Error('Band not found');
      const data = await res.json();
      setStatus(data);
    } catch (err) {
      setStatus({ notFound: true });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-black text-gray-200">
      <h1 className="text-7xl font-bold mb-8 text-grey-700">Is This Band Active?</h1>
      <div className="flex gap-2 mb-6">
        <input
          type="text"
          value={bandName}
          onChange={(e) => setBandName(e.target.value)}
          placeholder="Enter band name..."
          className="px-4 py-2 border border-gray-300 rounded-md w-80 text-lg"
        />
        <button
          onClick={checkBand}
          className="bg-red-600 text-white px-4 py-2 rounded-md text-lg hover:bg-red-700"
        >
          Search
        </button>
      </div>

      {loading && <p className="text-lg">Loading...</p>}

      {!loading && status && !status.notFound && (
        <div className="text-center text-xl">
          {status.active ? (
            <p>✅ <strong>{status.name}</strong> is <span className="text-green-700 font-bold">active</span>.<br />
            Last album: <em>"{status.last_album_title}"</em> ({status.last_album_year})</p>
          ) : (
            <p>❌ <strong>{status.name}</strong> is <span className="text-red-700 font-bold">not active</span>.<br />
            Last album: <em>"{status.last_album_title}"</em> ({status.last_album_year})</p>
          )}
        </div>
      )}

      {!loading && status?.notFound && (
        <p className="text-xl text-gray-600">🚫 Band not found.</p>
      )}
    </div>
  );
}
