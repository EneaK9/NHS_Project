import React from 'react';
import { FaAmbulance, FaPhoneAlt, FaFireExtinguisher, FaCarCrash, FaShip, FaShieldAlt } from 'react-icons/fa'; // Import icons
import './FirstAid.css'; // Import the CSS file
import EmergIcon from '../EmergIcon.png'; // Import the image

const FirstAid = () => {
  return (
    <div className="first-aid-container">
      <h1 className="first-aid-title">Ndihma e Parë dhe Numrat e Emergjencës në Shqipëri</h1>
      <p className="first-aid-intro">
        Ndihma e parë është reagimi i parë dhe vendimtar në rast aksidenti ose urgjence mjeksore. Kjo mund të shpëtojë jetë! Gjithmonë kontaktoni shërbimet e emergjencës para se të veproni.
      </p>
      <h2 className="first-aid-subtitle">Numrat e Emergjencës në Shqipëri</h2>
      <div className="emergency-numbers-container">
        <ul className="emergency-numbers">
          <li><FaAmbulance /> <a href="tel:127">Ambulanca (Shërbimi Mjekësor i Urgjencës): 127</a></li>
          <li><FaShieldAlt /> <a href="tel:129">Policia: 129</a></li>
          <li><FaFireExtinguisher /> <a href="tel:128">Zjarrefikësja: 128</a></li>
          <li><FaPhoneAlt /> <a href="tel:112">Numri i Përgjithshëm i Emergjencës (Europian): 112</a></li>
          <li><FaCarCrash /> <a href="tel:126">Emergjenca Rrugore (Policia Rrugore): 126</a></li>
          <li><FaShip /> <a href="tel:125">Emergjenca Detare (Garda Detare): 125</a></li>
        </ul>
        <img src={EmergIcon} alt="Emergency Icon" className="emergency-icon" />
      </div>
      <p className="first-aid-note">
        Shënim: Numri 112 mund të përdoret gjithashtu për të kontaktuar çdo shërbim emergjent në Shqipëri.
      </p>
      <h2 className="first-aid-subtitle">Rregulla të Përgjithshme për Ndihmën e Parë</h2>
      <ul className="first-aid-rules">
        <li>Sigurohuni që jeni i sigurt para se t’i afroheni të dëmtuarit.</li>
        <li>Vlerësoni situatën: Kontrolloni ndërgjegjen, frymëmarrjen dhe pulsin.</li>
        <li>Kontaktoni menjëherë një nga numrat e emergjencës dhe jepni informacionin e saktë për vendodhjen.</li>
        <li>Mos lëvizni të dëmtuarin nëse ka dëmtim në kokë, zverk, ose kurriz, përveç rastit kur ka rrezik të zjarrit.</li>
        <li>Përdor pajisje mbrojtëse (doreza, maskë) për të shmangur infeksionet.</li>
      </ul>
      <h2 className="first-aid-subtitle">Situata Specifike dhe Udhëzime</h2>
      <div className="specific-situations">
        <h3>1. Humbje Ndërgjegjeje (Pa Frymëmarrje)</h3>
        <ul>
          <li>Vendosni personin në tokë dhe kontrolloni frymëmarrjen.</li>
          <li>Nëse nuk frymëron: Filloni CPR (30 shtypje gjoksi + 2 frymë shpirtërore).</li>
          <li>Vazhdoni deri sa të vijë ambulanca.</li>
        </ul>
        <h3>2. Gjakderdhje e Rëndë</h3>
        <ul>
          <li>Shtypni plagën me një leckë të pastër.</li>
          <li>Ngrini pjesën e lënduar mbi nivelin e zemrës.</li>
          <li>Mos hiqni objektin nëse është i fiksuar (p.sh., thikë).</li>
        </ul>
        <h3>3. Djegje</h3>
        <ul>
          <li>Fshijeni me ujë të ftohtë për 10-15 minuta.</li>
          <li>Mos përdorni akull ose vajra.</li>
          <li>Mbulojeni me një fashë steril.</li>
        </ul>
        <h3>4. Mbytje (Objekt në Frymëmarrje)</h3>
        <ul>
          <li>Jepni 5 goditje në mes të shpatullave.</li>
          <li>Nëse nuk funksionon, bëni 5 shtypje barku (manovra e Heimlich).</li>
        </ul>
        <h3>5. Kocka e Thyer</h3>
        <ul>
          <li>Mos lëvizni pjesën e dëmtuar.</li>
          <li>Fiksoni me pllakë ose shkop.</li>
          <li>Vendosni akull për të reduktuar ënjten.</li>
        </ul>
        <h3>6. Sulm në Zemër</h3>
        <ul>
          <li>Simbollohet me dhimbje gjoksi, frymëmarrje të vështirë, dhe të etur.</li>
          <li>Ndihmoni pacientin të ulet dhe thirrni 127.</li>
        </ul>
        <h3>7. Goditje në Tru (Stroke)</h3>
        <ul>
          <li>Simbollat: Zbardhje në fytyrë, dobësi në njërën anë, fjalë të paqarta.</li>
          <li>Thirrni 127 menjëherë dhe mos u jepni asgjë për të ngrënë/pirë.</li>
        </ul>
      </div>
      <h2 className="first-aid-subtitle">Këshilla të Rëndësishme</h2>
      <ul className="important-tips">
        <li>Ruani numrat e emergjencës në telefon ose afër derës.</li>
        <li>Krijo një çantë ndihme të parë në shtëpi/makinë.</li>
        <li>Mos hezitoni të ndihmoni, por veproni brenda kompetencave tuaja.</li>
      </ul>
      <br></br>
      <p className="first-aid-conclusion">
        Ndihma e parë mund të jetë diferenca midis jetës dhe vdekjes. Mësoni bazat dhe jini gati të veproni!
      </p>
      <p className="first-aid-note">
        Shënim: Ky skript është informativ. Për trajnim të plotë, ndiqni një kurs të certifikuar të ndihmës së parë.
      </p>
    </div>
  );
};

export default FirstAid;