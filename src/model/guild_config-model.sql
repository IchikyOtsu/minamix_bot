CREATE TABLE IF NOT EXISTS guild_config (
    guild_id BIGINT UNSIGNED NOT NULL,
    config_key VARCHAR(100) NOT NULL,
    value VARCHAR(255) NOT NULL,
    PRIMARY KEY (guild_id, config_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
