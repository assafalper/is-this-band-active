import { Link } from "react-router-dom";

export default function Layout({ children, showTitle = false }) {
  return (
    <div className="relative min-h-screen bg-black text-gray-200 px-4 pt-20">
      {/* Top-left navigation */}
      <div className="absolute top-4 left-4 flex gap-4">
        <Link to="/submit" className="text-blue-400 hover:underline">
          Submit a Band
        </Link>
        <Link to="/admin" className="text-blue-400 hover:underline">
          Admin Review
        </Link>
      </div>

      {/* Main content */}
      <div className="flex flex-col items-center justify-center">
        {showTitle && (
          <h1 className="text-5xl md:text-7xl font-bold mb-8 text-gray-300 text-center">
            Is This Band Active?
          </h1>
        )}
        {children}
      </div>
<div className="fixed bottom-2 right-4 text-sm text-gray-500">
  <a
    href="https://github.com/assafalper/is-this-band-active"
    target="_blank"
    rel="noopener noreferrer"
    className="hover:underline"
  >
    © 2025 Assaf Alper
  </a>
</div>
    </div>
  );
}
