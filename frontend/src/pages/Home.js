import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FaPhoneAlt } from "react-icons/fa"; // Import the phone icon from react-icons
import "./Home.css"; // Import the CSS file

const Home = () => {
  const [articles, setArticles] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("https://nhs-project.onrender.com/api/translated-conditions")
      .then((response) => response.json())
      .then((data) => {
        const filteredData = data.map(article => {
          if (article && article.sections && Array.isArray(article.sections)) {
            // Filter out sections with titles containing "cookies"
            const filteredSections = article.sections.filter(section => !section.title.toLowerCase().includes("cookies"));

            // Filter out paragraphs containing "cookies"
            const updatedSections = filteredSections.map(section => {
              return {
                ...section,
                paragraphs: section.paragraphs.filter(paragraph => !paragraph.toLowerCase().includes("cookies"))
              };
            });

            return { ...article, sections: updatedSections };
          } else {
            console.error("Fetched data is not in the expected format:", article);
            return null;
          }
        }).filter(article => article !== null);

        setArticles(filteredData);
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  const handleContainerClick = (article) => {
    navigate('/article', { state: { article } });
  };
  const handleEmergencyClick = () => {
    navigate('/first-aid');
  };

  if (articles.length === 0) return <p>Loading...</p>;

  return (
    <div className="home-container">
      <div className="home-header">
        <h1 className="home-title">Mirë se vini në Shëndetin Tuaj</h1>
        <p className="home-motto">Your health, our priority</p>
      </div>
      <div className="content-row">
        <div className="article-container" onClick={() => handleContainerClick(articles[0])}>
          <h1 className="article-title">{articles[0].title}</h1>
          <p className="article-summary">{articles[0].sections[0]?.paragraphs[0]}</p>
        </div>
        <div className="emergency-container" onClick={handleEmergencyClick}>
          <h2 className="emergency-title">Numrat e emergjencës</h2>
          <p className="emergency-number"><FaPhoneAlt /> Policia e shtetit: 129</p>
          <p className="emergency-number"><FaPhoneAlt /> Zjarrfikse: 128</p>
          <p className="emergency-number"><FaPhoneAlt /> Ambulanca: 127</p>
          <p className="emergency-number"><FaPhoneAlt /> Sherbimi i emergjencës: 112</p>
        </div>
      </div>
      <div className="content-row">
        <div className="article-container" onClick={() => handleContainerClick(articles[1])}>
          <h1 className="article-title">{articles[1].title}</h1>
          <p className="article-summary">{articles[1].sections[0]?.paragraphs[0]}</p>
        </div>
      </div>
    </div>
  );
};

export default Home;