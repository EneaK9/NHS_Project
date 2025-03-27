import React, { useState, useEffect, forwardRef, useImperativeHandle } from "react";
import { useNavigate } from "react-router-dom";
import "./HealthAZ.css";

const HealthAZ = forwardRef(({ setSearchResults }, ref) => {
  const [data, setData] = useState([]);
  const navigate = useNavigate();

<<<<<<< HEAD
  useEffect(() => {
    fetch("https://nhs-project.onrender.com/api/translated-conditions")
      .then((response) => response.json())
      .then((rawData) => {
=======
 useEffect(() => {
    fetch("https://nhs-project.onrender.com/api/translated-conditions")
      .then((response) => response.json())
      .then((rawData) => {
        // Transform the API rows into grouped condition articles
>>>>>>> 227c0a597b37a83c269dc61d85c3937edf8f6d84
        const grouped = {};

        rawData.forEach((entry) => {
          const slug = entry.condition_slug;

          if (!grouped[slug]) {
            grouped[slug] = {
<<<<<<< HEAD
              title:slug
                  .replace(/_/g, " ")
                  .replace(/\b\w/g, (char) => char.toUpperCase()),
=======
              title: slug
                .replace(/_/g, " ")
                .replace(/\b\w/g, (char) => char.toUpperCase()),
>>>>>>> 227c0a597b37a83c269dc61d85c3937edf8f6d84
              sections: [],
            };
          }

          grouped[slug].sections.push({
            title: entry.section_name,
            paragraphs: entry.section_content.split("\n"),
          });
        });

        const articlesArray = Object.values(grouped);

<<<<<<< HEAD
=======
        // Optional filter to remove "cookies" mentions
>>>>>>> 227c0a597b37a83c269dc61d85c3937edf8f6d84
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
<<<<<<< HEAD
      .catch((error) => console.error("❌ Error fetching data:", error));
=======
      .catch((error) =>
        console.error("❌ Error fetching translated conditions:", error)
      );
>>>>>>> 227c0a597b37a83c269dc61d85c3937edf8f6d84
  }, []);

  useImperativeHandle(ref, () => ({
    handleSearch(query) {
      const lowerCaseQuery = query.toLowerCase();
      const results = data.filter((article) =>
        article.title.toLowerCase().includes(lowerCaseQuery) ||
        article.sections.some((section) =>
          section.title.toLowerCase().includes(lowerCaseQuery) ||
          section.paragraphs.some((paragraph) =>
            paragraph.toLowerCase().includes(lowerCaseQuery)
          )
        )
      );
      setSearchResults(results);
      navigate("/search");
    },
  }));

  if (data.length === 0) return <p>Loading...</p>;

  const handleContainerClick = (article) => {
    navigate("/article", { state: { article } });
  };

  return (
    <div>
      {data.map((article, index) => (
        <div
          key={index}
          className="container"
          onClick={() => handleContainerClick(article)}
        >
          <h1 className="title">{article.title}</h1>
        </div>
      ))}
    </div>
  );
});

export default HealthAZ;
