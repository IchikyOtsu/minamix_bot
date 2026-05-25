CREATE TABLE IF NOT EXISTS rp_characters (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    guild_id   BIGINT UNSIGNED NOT NULL,
    user_id    BIGINT UNSIGNED NOT NULL,
    name       VARCHAR(100)    NOT NULL,
    prefix     VARCHAR(20)     NOT NULL,
    image_url  VARCHAR(500)    NOT NULL,
    created_at TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_prefix_guild (guild_id, prefix)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
