CREATE DATABASE fsuv_background_checks;

\c fsuv_background_checks; 

CREATE TABLE background(
	id SERIAL PRIMARY KEY,
	name VARCHAR(50) NOT NULL UNIQUE,
	url VARCHAR DEFAULT 'N/A',
	type VARCHAR(10) NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE candidate_background(
	candidate_id INTEGER,
	background_id INTEGER,
	description VARCHAR NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(candidate_id, background_id),
	CONSTRAINT fk_background_id
   		FOREIGN KEY(background_id) 
   			REFERENCES background(id)
   			ON DELETE CASCADE
   			ON UPDATE CASCADE
);

CREATE TABLE verification_request(
	id SERIAL PRIMARY KEY,
	user_sub_key VARCHAR NOT NULL,
	background_id INTEGER,
	title VARCHAR NOT NULL,
	candidate_id INTEGER NOT NULL,
	comment VARCHAR DEFAULT 'N/A',
	state VARCHAR NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT fk_background_id
   		FOREIGN KEY(background_id) 
   			REFERENCES background(id)
   			ON DELETE CASCADE
   			ON UPDATE CASCADE
);

CREATE OR REPLACE FUNCTION updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = now(); 
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_at_background BEFORE UPDATE
    ON background FOR EACH ROW EXECUTE PROCEDURE 
    updated_at_column();
	
CREATE TRIGGER update_at_candidate_background BEFORE UPDATE
    ON candidate_background FOR EACH ROW EXECUTE PROCEDURE 
    updated_at_column();

CREATE TRIGGER update_at_verification_request BEFORE UPDATE
    ON verification_request FOR EACH ROW EXECUTE PROCEDURE 
    updated_at_column();

INSERT INTO background(name, url, type) VALUES('disciplinary', 'https://www.procuraduria.gov.co/Pages/Generacion-de-antecedentes.aspx',  'web');
INSERT INTO background(name, url, type) VALUES('fiscal', 'https://www.contraloria.gov.co/web/guest/persona-natural', 'web');
INSERT INTO background(name, url, type) VALUES('judicial', 'https://antecedentes.policia.gov.co:7005/WebJudicial/index.xhtml', 'web');
INSERT INTO background(name, url, type) VALUES('corrective actions', 'https://srvcnpc.policia.gov.co/PSC/frm_cnp_consulta.aspx', 'web');
INSERT INTO background(name, url, type) VALUES('military situation', 'https://www.libretamilitar.mil.co/Modules/Consult/MilitaryCardCertificate', 'web');
INSERT INTO background(name, url, type) VALUES('traffic infraction', 'https://www.fcm.org.co/simit/#/home-public', 'web');
INSERT INTO background(name, url, type) VALUES('university degree', 'N/A', 'no web');