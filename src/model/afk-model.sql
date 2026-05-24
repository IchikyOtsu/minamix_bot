CREATE TABLE IF NOT EXISTS afk_users (
    user_id       BIGINT UNSIGNED NOT NULL,
    guild_id      BIGINT UNSIGNED NOT NULL,
    original_nick VARCHAR(32),
    reason        VARCHAR(200)    NOT NULL,
    start_time    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time      TIMESTAMP       NULL,
    PRIMARY KEY (user_id, guild_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
