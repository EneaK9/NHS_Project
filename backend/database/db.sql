-- DROP TABLES IF EXIST
DROP TABLE IF EXISTS condition_sections_albanian;
DROP TABLE IF EXISTS conditions_albanian;

-- CREATE conditions_albanian table
CREATE TABLE conditions_albanian (
  id SERIAL PRIMARY KEY,
  condition_name VARCHAR(255) NOT NULL,
  condition_slug VARCHAR(255) NOT NULL UNIQUE,
  url VARCHAR(500),
  full_json TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CREATE condition_sections_albanian table
CREATE TABLE condition_sections_albanian (
  id SERIAL PRIMARY KEY,
  condition_slug VARCHAR(255) NOT NULL,
  section_name VARCHAR(255) NOT NULL,
  section_content TEXT,
  section_order INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_condition_slug
    FOREIGN KEY (condition_slug)
    REFERENCES conditions_albanian(condition_slug)
    ON DELETE CASCADE
);
