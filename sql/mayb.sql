
-- pins on boards
DROP TABLE IF EXISTS `pins`;
CREATE TABLE IF NOT EXISTS `pins` (
    `pin_id` integer NOT NULL primary key,
    `image_url` text NOT NULL,
    `description` text NOT NULL,
    `refer_url` text NOT NULL, -- outer link
    `updated` text NOT NULL
);

CREATE INDEX pin_idx_1 ON pins(`image_url`);
CREATE INDEX pin_idx_2 ON pins(`updated`);

-- tags related with pins
DROP TABLE IF EXISTS `words`;
CREATE TABLE IF NOT EXISTS `words` (
    `pin_id` integer NOT NULL,
    `user` text NOT NULL,
    `word` text NOT NULL,
    `updated` text NOT NULL,
    primary key(`pin_id`, `user`, `word`)
);

CREATE INDEX word_idx_1 ON words(`pin_id`);
CREATE INDEX word_idx_2 ON words(`pin_id`, `user`);
CREATE INDEX word_idx_3 ON words(`word`);

-- distance cache of each pin
DROP TABLE IF EXISTS `clusters`;
CREATE TABLE IF NOT EXISTS `clusters` (
    `pin_id_a` text NOT NULL,
    `pin_id_b` text NOT NULL,
    `score` real NOT NULL,
    `updated` text NOT NULL,
    primary key(`pin_id_a`, `pin_id_b`)
);

CREATE INDEX clusters_idx_1 ON clusters(`score`);