import React, { useState, useEffect, forwardRef, useImperativeHandle } from "react";
import { useNavigate } from "react-router-dom";
import "./HealthAZ.css";

const HealthAZ = forwardRef(({ setSearchResults }, ref) => {
  const [data, setData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("https://nhs-project.onrender.com/api/translated-conditions")
      .then((response) => response.json())
      .then((dataArray) => {
        const filteredData = dataArray.map(data => {
          if (data && data.sections && Array.isArray(data.sections)) {
            const filteredSections = data.sections.filter(section => !section.title.toLowerCase().includes("cookies"));

            const updatedSections = filteredSections.map(section => {
              return {
                ...section,
                paragraphs: section.paragraphs.filter(paragraph => !paragraph.toLowerCase().includes("cookies"))
              };
            });

            return { ...data, sections: updatedSections, title: data.title || "Untitled" };
          } else {
            console.error("Fetched data is not in the expected format:", data);
            return null;
          }
        }).filter(data => data !== null);

        setData(filteredData);
      })
      .catch((error) => console.error("Error fetching data:", error));
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
