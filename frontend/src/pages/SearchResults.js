import React from "react";
import { Link } from "react-router-dom";

const SearchResults = ({ searchResults }) => {
  if (searchResults.length === 0) return <p>No search results found.</p>;

  return (
    <div>
      <h1>Search Results</h1>
      {searchResults.map((article, index) => (
        <div key={index} className="search-result">
          <Link to="/article" state={{ article }}>
            <h2>{article.title}</h2>
          </Link>
        </div>
      ))}
    </div>
  );
};

export default SearchResults;