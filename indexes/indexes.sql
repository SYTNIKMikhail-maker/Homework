CREATE TABLE customer(
    customer_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    modified_date DATE,
    age INT,
    active BOOLEAN
);

ALTER TABLE customer
ADD CONSTRAINT customer_pk PRIMARY KEY (customer_id);

INSERT INTO customer
SELECT
    gs AS customer_id,
    CONCAT('firstname', gs),
    CONCAT('lastname', gs),
    CONCAT('firstname', 'lastname', gs, '@email.com'),
    CURRENT_DATE + (gs % 365),
    gs % 90,
    gs % 7 = 0
FROM GENERATE_SERIES(1, 1000000) AS gs;

SELECT * FROM customer;

SELECT * 
FROM pg_indexes
WHERE tablename = 'customer';

CREATE INDEX customer_name_idx
ON customer (first_name, last_name);

CREATE INDEX customer_age_idx
ON customer (age);

EXPLAIN ANALYZE
SELECT *
FROM customer
WHERE age BETWEEN 18 AND 60;

CREATE INDEX idx_for_date 
ON customer(first_name, last_name) 
WHERE modified_date = '2014-12-21';

SELECT *
FROM pg_indexes
WHERE indexname = 'idx_for_date';

EXPLAIN ANALYZE
SELECT *
FROM customer
WHERE modified_date = '2014-12-21'
AND first_name = 'firstname1'
AND last_name = 'lastname1';

ALTER TABLE customer 
DROP CONSTRAINT customer_pk;

ALTER INDEX idx_for_date
RENAME TO idx_for_date_idx;

CREATE INDEX idx_modified_date 
ON customer USING HASH(modified_date);

SELECT * 
FROM pg_indexes
WHERE indexname = 'idx_modified_date';

CREATE INDEX idx_for_email 
ON customer (email) 
WHERE email like '%mail';

EXPLAIN ANALYZE 
SELECT email 
FROM customer 
WHERE email like '%mail';

CREATE INDEX expres_index 
ON customer((
    LOWER(LEFT(first_name, 1)) || ',' || last_name
));

EXPLAIN ANALYZE
SELECT * 
FROM customer 
WHERE LOWER(LEFT(first_name, 1)) || ',' || last_name = 'f,lastname1';




