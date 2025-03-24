CREATE TABLE IF NOT EXISTS conditions_albanian (
  id SERIAL PRIMARY KEY,
  condition_name VARCHAR(255) NOT NULL,
  condition_slug VARCHAR(255) UNIQUE NOT NULL,
  url VARCHAR(500),
  full_json TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS condition_sections_albanian (
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
