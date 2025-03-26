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
      console.log("Fetched data: ", dataArray);  // Add this line to inspect data

      const formattedData = dataArray.reduce((acc, item) => {
        const { condition_slug, condition_name, section_name, section_content, section_order } = item;

        // If this condition_slug isn't in the accumulator yet, add it
        if (!acc[condition_slug]) {
          acc[condition_slug] = {
            condition_slug,
            condition_name,
            sections: [],
          };
        }

        // If section_content is a string, split it into paragraphs
        const paragraphs = typeof section_content === "string" ? section_content.split("\n") : section_content;

        // Add the section data under the correct condition
        acc[condition_slug].sections.push({
          section_name,
          section_content: paragraphs,
          section_order,
        });

        return acc;
      }, {});

      // Convert the accumulator object back to an array
      const resultArray = Object.values(formattedData);

      // Optional: Filter out sections containing "cookies"
      const filteredData = resultArray.map(data => {
        const filteredSections = data.sections.filter(section => !section.section_name.toLowerCase().includes("cookies"));
        const updatedSections = filteredSections.map(section => {
          return {
            ...section,
            section_content: section.section_content.filter(paragraph => !paragraph.toLowerCase().includes("cookies"))
          };
        });

        return { ...data, sections: updatedSections, title: data.condition_name || "Untitled" };
      });

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
