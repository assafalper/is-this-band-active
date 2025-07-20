import { useState } from "react";
import Layout from '../components/Layout';

export default function SubmitBand() {
  const [message, setMessage] = useState("");

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    const formData = new FormData(form);

    try {
      const res = await fetch("https://is-this-band-active.onrender.com/submit-form/", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setMessage(data.message || "Band submitted!");
    } catch (err) {
      setMessage("Failed to submit band.");
    }
  };

  return (
    <Layout>
    <div className="max-w-xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Submit a Band</h1>

      <form onSubmit={handleFormSubmit} className="space-y-4">
        <input type="hidden" name="mode" value="single" />

        <div>
          <label className="block font-semibold">Band Name</label>
          <input type="text" name="name" required className="w-full border p-2 rounded" />
        </div>

        <div>
          <label className="block font-semibold">Is the band active?</label>
          <select name="active" className="w-full border p-2 rounded">
            <option value="true">Yes</option>
            <option value="false">No</option>
          </select>
        </div>

        <div>
          <label className="block font-semibold">Last Album Title</label>
          <input type="text" name="last_album_title" className="w-full border p-2 rounded" />
        </div>

        <div>
          <label className="block font-semibold">Last Album Year</label>
          <input type="number" name="last_album_year" className="w-full border p-2 rounded" />
        </div>

        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Submit
        </button>
      </form>

      {message && <p className="mt-4 text-green-600">{message}</p>}
    </div>
  </Layout>);
}
