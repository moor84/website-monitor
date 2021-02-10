CREATE TABLE IF NOT EXISTS websites (
    website_id SERIAL PRIMARY KEY,
    url VARCHAR (300) UNIQUE,
    name VARCHAR (100)
);

CREATE TABLE IF NOT EXISTS website_metrics (
    metric_timestamp TIMESTAMP,
    website_id INT NOT NULL,
    status_code SMALLINT NOT NULL,
    response_time REAL NOT NULL,
    regex_check BOOLEAN NOT NULL,
    CONSTRAINT website_metric_pkey PRIMARY KEY (website_id, metric_timestamp),
    CONSTRAINT fk_website FOREIGN KEY(website_id) REFERENCES websites(website_id)
);
