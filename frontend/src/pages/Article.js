import React from "react";
import { useLocation } from "react-router-dom";
import "./Article.css"; // Import the CSS file


const Article = () => {
  const location = useLocation();
  const article = location.state?.article;

  if (!article) return <p>No article data available.</p>;

  return (
    <div className="article-container">
      <h1 className="article-title">{article.title}</h1>
      {article.sections.map((section, index) => (
        <div key={index} className="article-section">
          <h2 className="article-section-title">{section.title}</h2>
          {section.paragraphs.map((paragraph, pIndex) => (
            <p key={pIndex} className="article-paragraph">{paragraph}</p>
          ))}
        </div>
      ))}
      <href className="article-sublinks">{article.sublinks}</href>
    </div>
  );
};

export default Article;