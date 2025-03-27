import React from "react";
import "./About.css";

const About = () => {
  return (
    <div className="about-page">
      <div className="about-header">
        <h1>Rreth Nesh</h1>
      </div>
      <div className="about-content">
        <section className="about-section">
          <h2>Misioni Ynë</h2>
          <p className="section-content">
            Ne ofrojmë informacion shëndetësor të besueshëm në gjuhën shqipe, duke përkthyer materiale nga NHS për t'i bërë këto burime të aksesueshme për komunitetin shqipfolës.
          </p>
        </section>
        
        <section className="about-section">
          <h2>Qëllimi Ynë</h2>
          <p className="section-content">
            Qëllimi ynë është të thyejmë barrierat gjuhësore në kujdesin shëndetësor, duke siguruar që komuniteti shqipfolës të ketë qasje në informacionin shëndetësor cilësor.
          </p>
        </section>

        <section className="about-section">
          <h2>Shërbimet Tona</h2>
          <p className="section-content">
            • Përkthime të besueshme të informacionit shëndetësor
            • Këshilla mjekësore të përgjithshme
            • Udhëzime për ndihmën e parë
            • Informacion për shërbimet shëndetësore
          </p>
        </section>
      </div>
    </div>
  );
};

export default About;
