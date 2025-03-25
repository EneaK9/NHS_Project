import React, { useState, useRef } from "react";
import { Routes, Route, Link } from "react-router-dom";
import { FaSearch } from "react-icons/fa"; // Import search icon from react-icons
import Home from "./pages/Home";
import HealthAZ from "./pages/HealthAZ";
import Article from "./pages/Article"; // Import the Article component
import SearchResults from "./pages/SearchResults"; // Import the SearchResults component
import FirstAid from './pages/FirstAid';

import "./App.css"; // Import styles
import Logo1 from "./Logo1.png"; // Import your icon image

function App() {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const healthAZRef = useRef();

  const handleSearch = () => {
    if (searchQuery.trim() !== "" && healthAZRef.current) {
      setSearchResults([]); // Clear previous search results
      healthAZRef.current.handleSearch(searchQuery);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="app-container">
      {/* Header with logo, title, navigation and search */}
      <header className="header">
        <div className="header-left">
          <img src={Logo1} alt="Logo" className="logo" />
          <h1 className="header-title">Shëndeti Juaj</h1>
        </div>
        <nav className="navbar">
          <ul>
            <li><Link to="/">Kryefaqja</Link></li>
            <li><Link to="/health-a-z">Shëndeti</Link></li>
            <li><Link to="/first-aid">Ndihma e pare</Link></li>
          </ul>
        </nav>
        <div className="search-container">
          <input
            type="text"
            placeholder="Search..."
            className="search-box"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <FaSearch className="search-icon" onClick={handleSearch} />
        </div>
      </header>

      {/* Main Content Area */}
      <main className="content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/health-a-z" element={<HealthAZ ref={healthAZRef} setSearchResults={setSearchResults} />} />
          <Route path="/article" element={<Article />} /> 
          <Route path="/search" element={<SearchResults searchResults={searchResults} />} /> 
          <Route path="/first-aid" element={<FirstAid />} />
        </Routes>
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>© 2025 Shëndeti juaj. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
