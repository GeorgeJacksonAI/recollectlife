import { Link } from "react-router-dom";
import { BookOpen } from "lucide-react";
import { useWoodyButton } from "@/hooks/useWoodyButton";

export default function Navbar() {
  const { handleWoodyClick } = useWoodyButton();

  return (
    <div className="fixed top-0 left-0 right-0 z-50 px-4 pt-4 md:px-6 md:pt-6">
      <nav className="max-w-6xl mx-auto bg-white/70 backdrop-blur-md border border-white/20 rounded-2xl shadow-lg shadow-black/5">
        <div className="px-6 md:px-8 h-16 md:h-18 flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-[#5C3D2E] to-[#4A2F1F] flex items-center justify-center shadow-md transition-transform group-hover:scale-105">
              <BookOpen className="w-5 h-5 text-white" />
            </div>
            <span className="text-lg md:text-xl font-semibold text-[#5C3D2E] font-story hidden sm:inline">
              Life Story
            </span>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center gap-3 md:gap-6">
            <Link
              to="/auth"
              className="text-sm md:text-base text-[#8B6F5C] hover:text-[#5C3D2E] transition-colors font-medium"
            >
              Log In
            </Link>
            <Link to="/auth">
              <button
                onClick={handleWoodyClick}
                className="btn-woody px-4 md:px-6 py-2 md:py-2.5 rounded-xl text-sm md:text-base font-medium text-white"
              >
                Start for Free
              </button>
            </Link>
          </div>
        </div>
      </nav>
    </div>
  );
}
