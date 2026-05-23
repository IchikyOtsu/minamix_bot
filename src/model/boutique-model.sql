CREATE TABLE IF NOT EXISTS boutique_roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_id BIGINT NOT NULL,
    prix INT NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    exclusif TINYINT(1) NOT NULL DEFAULT 0
);
