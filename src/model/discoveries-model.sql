CREATE TABLE IF NOT EXISTS discoveries (
    user_id     BIGINT UNSIGNED NOT NULL,
    guild_id    BIGINT UNSIGNED NOT NULL,
    egg_key     VARCHAR(50)     NOT NULL,
    found_at    TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, guild_id, egg_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
