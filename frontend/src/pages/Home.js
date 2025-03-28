import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FaInfoCircle } from "react-icons/fa";
import { FaPhoneAlt } from "react-icons/fa";
import "./Home.css";

const Home = () => {
  const [articles, setArticles] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("https://nhs-project.onrender.com/api/translated-conditions")
      .then((response) => response.json())
      .then((rawData) => {
        // Transform the API rows into grouped condition articles
        const grouped = {};

        rawData.forEach((entry) => {
          const slug = entry.condition_slug;

          if (!grouped[slug]) {
            grouped[slug] = {
              title: slug
                .replace(/_/g, " ")
                .replace(/\b\w/g, (char) => char.toUpperCase()),
              sections: [],
            };
          }

          grouped[slug].sections.push({
            title: entry.section_name,
            paragraphs: entry.section_content.split("\n"),
          });
        });

        const articlesArray = Object.values(grouped);

        // Optional filter to remove "cookies" mentions
        const filteredData = articlesArray.map((article) => {
          const filteredSections = article.sections.filter(
            (section) =>
              !section.title.toLowerCase().includes("cookies") &&
              !section.paragraphs.some((p) =>
                p.toLowerCase().includes("cookies")
              )
          );

          return { ...article, sections: filteredSections };
        });

        setArticles(filteredData);
      })
      .catch((error) =>
        console.error("❌ Error fetching translated conditions:", error)
      );
  }, []);

  const handleContainerClick = (article) => {
    navigate("/article", { state: { article } });
  };

  const handleEmergencyClick = () => {
    navigate("/first-aid");
  };

  if (articles.length === 0) return <p>Loading...</p>;

  return (
    <div className="home-container">
      <div className="home-header">
        <h1 className="home-title">Mirë se vini në Shëndetin tuaj</h1>
        <p className="home-motto">Shëndeti juaj, përkushtimi ynë.</p>
      </div>
      <div className="content-row">
        <div
          className="article-container"
          onClick={() => handleContainerClick(articles[0])}
        >
          <h1 className="article-title">{articles[0].title}</h1>
          <p className="article-summary">
            {articles[0].sections[0]?.paragraphs[0]}
          </p>
        </div>
        <div
          className="emergency-container"
          onClick={handleEmergencyClick}
        >
          <h2 className="emergency-title">Numrat e emergjencës</h2>
          <p className="emergency-number">
            <FaPhoneAlt /> Policia e shtetit: 129
          </p>
          <p className="emergency-number">
            <FaPhoneAlt /> Zjarrfikse: 128
          </p>
          <p className="emergency-number">
            <FaPhoneAlt /> Ambulanca: 127
          </p>
          <p className="emergency-number">
            <FaPhoneAlt /> Shërbimi i emergjencës: 112
          </p>
        </div>
      </div>
      <div className="content-row">
        <div
          className="article-container"
          onClick={() => handleContainerClick(articles[1])}
        >
          <h1 className="article-title">{articles[1].title}</h1>
          <p className="article-summary">
            {articles[1].sections[0]?.paragraphs[0]}
          </p>
        </div>
      </div>
      <div className="content-row">
        <div
          className="article-container"
          onClick={() => navigate("/about")}
          style={{ cursor: 'pointer' }}
        >
          <h1 className="article-title">
            <FaInfoCircle style={{ marginRight: '10px' }} />
            Rreth Nesh
          </h1>
          <p className="article-summary">
            Ne ofrojmë informacion shëndetësor të besueshëm në gjuhën shqipe, duke përkthyer materiale nga NHS për komunitetin shqipfolës.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Home;