CREATE TABLE employees (
id SERIAL PRIMARY KEY,
name TEXT,
email TEXT,
department_id INT,
salary NUMERIC
);

INSERT INTO employees (name, email, department_id, salary) VALUES
('John Doe', 'john@example.com', 1, 50000),
('Jane Smith', 'jane@example.com', 2, 60000),
('Alice Johnson', 'alice@example.com', 1, 55000),
('Bob Brown', 'bob@example.com', 3, 45000),
('Carol White', 'carol@example.com', 2, 62000);

--3.1
CREATE OR REPLACE FUNCTION calc_bonus(salary NUMERIC)
RETURNS NUMERIC
LANGUAGE plpgsql
AS $$
BEGIN
    salary := salary * 0.10;
    RETURN salary;
END;
$$;

SELECT name, salary, calc_bonus(salary) AS bonus
FROM employees;

--3.2
CREATE OR REPLACE FUNCTION department_status(dep_id INT)
RETURNS TEXT
LANGUAGE plpgsql
AS $$
DECLARE
    employee_count INT;
BEGIN
    SELECT COUNT(*) INTO employee_count
    FROM employees
    WHERE dep_id = department_id;
    IF employee_count > 10 THEN RETURN 'Big_Department';
    ELSE RETURN 'small';
    END IF;
END;
$$;

SELECT department_id, department_status(department_id)
FROM employees
GROUP BY department_id
ORDER BY department_id ASC;

--3.3
CREATE OR REPLACE FUNCTION sum_salary(state NUMERIC, salary NUMERIC)
RETURNS NUMERIC
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN state + COALESCE(salary, 0);
END;
$$;

CREATE AGGREGATE total_salaries(NUMERIC) (
    SFUNC = sum_salary,
    STYPE = NUMERIC,
    INITCOND = '0'
);

SELECT total_salaries(salary)
FROM employees;

--Простым способом(от себя)
CREATE OR REPLACE FUNCTION s_salary()
RETURNS NUMERIC
LANGUAGE plpgsql
AS $$
DECLARE all_sum NUMERIC;
BEGIN
    SELECT SUM(salary) INTO all_sum
    FROM employees;
    RETURN all_sum;
END;
$$;

SELECT salary, s_salary() AS total
FROM employees;

--3.3
CREATE FUNCTION safe_divide(numerator NUMERIC, denominator NUMERIC) RETURNS NUMERIC AS $$
BEGIN
    IF denominator = 0 THEN
        RAISE EXCEPTION 'Division by zero';
    END IF;
    RETURN ROUND(numerator / denominator);
EXCEPTION
    WHEN others THEN
        RETURN NULL;
END;
$$ LANGUAGE plpgsql;

--3.4
CREATE OR REPLACE FUNCTION safe_divide(numerator NUMERIC, denominator NUMERIC)
RETURNS NUMERIC
AS $$
BEGIN
    IF denominator = 0 THEN
        RAISE EXCEPTION 'Division by zero';
    END IF;

    RETURN ROUND(numerator / denominator);

EXCEPTION
    WHEN SQLSTATE 'P0001' THEN
        RAISE;
    WHEN others THEN
        RETURN NULL;
END;
$$ LANGUAGE plpgsql;

SELECT safe_divide(10, 0);
SELECT safe_divide(10, 2);
SELECT safe_divide(2, null);

--3.5
SELECT name, LENGTH(name) AS name_length FROM employees;

--3.6
CREATE FUNCTION email_domain(email TEXT) RETURNS TEXT AS $$
BEGIN
    RETURN split_part(email, '@', 2);
END;
$$ LANGUAGE plpgsql;

SELECT name, email, email_domain(email) AS domain
FROM employees;

--3.7
CREATE FUNCTION net_salary(salary NUMERIC, tax_rate NUMERIC) RETURNS NUMERIC AS $$
BEGIN
    RETURN salary - (salary * tax_rate);
END;
$$ LANGUAGE plpgsql;

SELECT name, salary, net_salary(salary, 0.2) AS net_salary
FROM employees;

--3.8
CREATE FUNCTION department_employees(dept_id INTEGER) RETURNS SETOF employees AS $$
BEGIN
    RETURN QUERY SELECT * FROM employees WHERE department_id = dept_id;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM department_employees(2);

--Cleanup
DROP FUNCTION calc_bonus;
DROP FUNCTION department_status;
DROP AGGREGATE IF EXISTS total_salaries(NUMERIC);
DROP FUNCTION safe_divide;
DROP FUNCTION department_employees;
DROP FUNCTION net_salary;
DROP FUNCTION email_domain;
DROP TABLE employees CASCADE;
