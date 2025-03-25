import React, { useState, useEffect, forwardRef, useImperativeHandle } from "react";
import { useNavigate } from "react-router-dom";
import "./HealthAZ.css"; // Import the CSS file

const HealthAZ = forwardRef(({ setSearchResults }, ref) => {
  const [data, setData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
  fetch("https://nhs-project.onrender.com/api/translated-conditions")
    .then((response) => response.json())
    .then((rawData) => {
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

      setData(filteredData);
    })
    .catch((error) => console.error("❌ Error fetching data:", error));
}, []);

  useImperativeHandle(ref, () => ({
    handleSearch(query) {
      const lowerCaseQuery = query.toLowerCase();
      const results = data.filter(article => 
        article.title.toLowerCase().includes(lowerCaseQuery) ||
        article.sections.some(section =>
          section.title.toLowerCase().includes(lowerCaseQuery) ||
          section.paragraphs.some(paragraph => paragraph.toLowerCase().includes(lowerCaseQuery))
        )
      );
      setSearchResults(results);
      navigate('/search');
    }
  }));

  if (data.length === 0) return <p>Loading...</p>;

  const handleContainerClick = (article) => {
    navigate('/article', { state: { article } });
  };

  return (
    <div>
      {data.map((article, index) => (
        <div key={index} className="container" onClick={() => handleContainerClick(article)}>
          <h1 className="title">{article.title}</h1>
        </div>
      ))}
    </div>
  );
});

export default HealthAZ;