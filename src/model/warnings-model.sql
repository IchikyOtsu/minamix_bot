CREATE TABLE IF NOT EXISTS warnings (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id      BIGINT UNSIGNED NOT NULL,
    guild_id     BIGINT UNSIGNED NOT NULL,
    moderator_id BIGINT UNSIGNED NOT NULL,
    reason       VARCHAR(500)    NOT NULL,
    created_at   TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_guild (user_id, guild_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
