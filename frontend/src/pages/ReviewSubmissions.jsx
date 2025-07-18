import { useEffect, useState } from "react";

export default function ReviewSubmissions() {
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_BASE_URL}/admin/review/`)
      .then((res) => res.json())
      .then((data) => setSubmissions(data))
      .catch(() => alert("Failed to fetch submissions."))
      .finally(() => setLoading(false));
  }, []);

  const handleAction = async (id, action) => {
    const res = await fetch(`${process.env.REACT_APP_API_BASE_URL}/admin/review/${id}/${action}`, {
      method: "POST",
    });
    if (res.ok) {
      setSubmissions((prev) => prev.filter((s) => s.id !== id));
    } else {
      alert("Failed to process submission.");
    }
  };

  if (loading) return <p className="p-4">Loading...</p>;

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Pending Submissions</h1>
      {submissions.length === 0 ? (
        <p>No submissions to review.</p>
      ) : (
        submissions.map((s) => (
          <div key={s.id} className="border p-4 rounded mb-4">
            <p><strong>Name:</strong> {s.name}</p>
            <p><strong>Active:</strong> {s.active ? "Yes" : "No"}</p>
            <p><strong>Last Album:</strong> {s.last_album_title} ({s.last_album_year})</p>
            <div className="mt-2 flex gap-2">
              <button
                onClick={() => handleAction(s.id, "approve")}
                className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
              >
                Approve
              </button>
              <button
                onClick={() => handleAction(s.id, "reject")}
                className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
              >
                Reject
              </button>
            </div>
          </div>
        ))
      )}
    </div>
  );
}
