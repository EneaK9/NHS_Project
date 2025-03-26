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
          {section.paragraphs.map((paragraph, pIndex) => {
            // Check if the paragraph contains an <img> tag
            if (paragraph.includes('<img')) {
              return (
                <div key={pIndex} className="article-paragraph">
                  {/* Using dangerouslySetInnerHTML to parse the HTML in the paragraph */}
                  <div dangerouslySetInnerHTML={{ __html: paragraph }} />
                </div>
              );
            } else {
              return (
                <p key={pIndex} className="article-paragraph">{paragraph}</p>
              );
            }
          })}
        </div>
      ))}
      <h2 className="sub-title">Nenlinqe: </h2>
      <div className="article-sublinks">
        {article.sublinks && article.sublinks.map((sublink, index) => (
          <p key={index}><a href={sublink}>{sublink}</a></p>
        ))}
      </div>
    </div>
  );
};

export default Article;
