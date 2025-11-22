-- ============================================================
-- Database and Pokemon Table Setup
-- ============================================================

CREATE DATABASE IF NOT EXISTS pokemons_db;
USE pokemons_db;

CREATE TABLE IF NOT EXISTS pokemon (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    types VARCHAR(100) NOT NULL,
    hp INT NOT NULL,
    attack INT NOT NULL,
    defense INT NOT NULL,
    sp_attack INT NOT NULL,
    sp_defense INT NOT NULL,
    speed INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_types (types)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

TRUNCATE TABLE pokemon;


INSERT INTO pokemon (name, types, hp, attack, defense, sp_attack, sp_defense, speed) VALUES
('Bulbasaur', 'Grass/Poison', 45, 49, 49, 65, 65, 45),
('Charmander', 'Fire', 39, 52, 43, 60, 50, 65),
('Squirtle', 'Water', 44, 48, 65, 50, 64, 43),
('Caterpie', 'Bug', 45, 52, 43, 60, 50, 35),
('Weedle', 'Bug/Poison', 40, 35, 30, 20, 20, 25),
('Rattata', 'Normal', 30, 56, 35, 25, 35, 72),
('Pikachu', 'Electric', 35, 55, 40, 50, 50, 90),
('Ubat', 'Poison/Flying', 40, 45, 35, 15, 30, 55),
('Meowth', 'Normal', 40, 45, 41, 40, 37, 90),
('Mankey', 'Fighting', 40, 80, 35, 35, 31, 70),
('Abra', 'Psychic', 25, 20, 15, 105, 55, 90),
('Eevee', 'Normal', 55, 55, 50, 45, 65, 55),
('Dratini', 'Dragon', 41, 64, 45, 50, 45, 50),
('Mew', 'Psychic', 100, 100, 100, 100, 100, 100);

-- ============================================================
-- Create Users Table (for future authentication)
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Create Favorites Table (for user favorites)
-- ============================================================
CREATE TABLE IF NOT EXISTS favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    pokemon_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_pokemon (user_id, pokemon_id),
    INDEX idx_user_id (user_id),
    INDEX idx_pokemon_id (pokemon_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Create Search Logs Table (for analytics)
-- ============================================================
CREATE TABLE IF NOT EXISTS search_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    search_query VARCHAR(255) NOT NULL,
    results_count INT,
    user_ip VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_query (search_query),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Verify data insertion
-- ============================================================
SELECT 'Database setup complete!' as status;
SELECT COUNT(*) as total_pokemon FROM pokemon;
SELECT MIN(id) as min_id, MAX(id) as max_id, COUNT(DISTINCT name) as unique_names FROM pokemon;

-- ============================================================
-- Sample queries to test
-- ============================================================
-- Test: Get all pokemon
-- SELECT * FROM pokemon ORDER BY id;

-- Test: Search by name
-- SELECT * FROM pokemon WHERE LOWER(name) LIKE LOWER('%pikachu%');

-- Test: Search by type
-- SELECT * FROM pokemon WHERE LOWER(types) LIKE LOWER('%electric%');

-- Test: Get stats
-- SELECT 
--     COUNT(*) as total_count,
--     ROUND(AVG(hp), 2) as avg_hp,
--     ROUND(AVG(attack), 2) as avg_attack,
--     ROUND(AVG(defense), 2) as avg_defense,
--     ROUND(AVG(sp_attack), 2) as avg_sp_attack,
--     ROUND(AVG(sp_defense), 2) as avg_sp_defense,
--     ROUND(AVG(speed), 2) as avg_speed
-- FROM pokemon;
