CREATE SCHEMA IF NOT EXISTS humanresources;
CREATE SCHEMA IF NOT EXISTS sales;
CREATE SCHEMA IF NOT EXISTS production;

CREATE TABLE IF NOT EXISTS humanresources.department (
    departmentid SERIAL PRIMARY KEY,
    name VARCHAR(50),
    groupname VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS humanresources.employee (
    businessentityid SERIAL PRIMARY KEY,
    nationalidnumber VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS humanresources.employeepayhistory (
    businessentityid INT,
    ratechangedate DATE,
    rate NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS production.productcategory (
    productcategoryid SERIAL PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS production.productsubcategory (
    productsubcategoryid SERIAL PRIMARY KEY,
    productcategoryid INT,
    name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS production.product (
    productid SERIAL PRIMARY KEY,
    name VARCHAR(50),
    productsubcategoryid INT
);

CREATE TABLE IF NOT EXISTS sales.salesorderheader (
    salesorderid SERIAL PRIMARY KEY,
    orderdate DATE
);

CREATE TABLE IF NOT EXISTS sales.salesorderdetail (
    salesorderdetailid SERIAL PRIMARY KEY,
    salesorderid INT,
    productid INT,
    unitprice NUMERIC(10,2),
    orderqty INT,
    unitpricediscount NUMERIC(5,2) DEFAULT 0
);

INSERT INTO humanresources.department (name, groupname) VALUES
('Engineering', 'Research and Development'),
('Tool Design', 'Research and Development'),
('Sales', 'Sales and Marketing'),
('Marketing', 'Sales and Marketing'),
('Purchasing', 'Inventory Management'),
('Research and Development', 'Research and Development'),
('Production', 'Manufacturing'),
('Production Control', 'Manufacturing'),
('Human Resources', 'Executive General and Administration'),
('Finance', 'Executive General and Administration');

INSERT INTO humanresources.employee (nationalidnumber) VALUES
('111111111'),
('222222222'),
('333333333'),
('444444444'),
('555555555');

SELECT * FROM humanresources.employee;

INSERT INTO humanresources.employeepayhistory (businessentityid, ratechangedate, rate) VALUES
(1, '2020-01-01', 30.00),
(1, '2021-01-01', 35.00),
(2, '2020-01-01', 50.00),
(2, '2022-01-01', 60.00),
(3, '2019-01-01', 25.00),
(4, '2021-06-01', 80.00),
(5, '2020-03-01', 45.00);

SELECT * FROM humanresources.employeepayhistory;

INSERT INTO production.productcategory (name) VALUES
('Bikes'),
('Components'),
('Clothing'),
('Accessories');

INSERT INTO production.productsubcategory (productcategoryid, name) VALUES
(1, 'Mountain Bikes'),
(1, 'Road Bikes'),
(2, 'Handlebars'),
(2, 'Brakes'),
(3, 'Jerseys'),
(4, 'Helmets');

SELECT * FROM production.productsubcategory;

INSERT INTO production.product (name, productsubcategoryid) VALUES
('Mountain-100', 1),
('Mountain-200', 1),
('Road-150', 2),
('HL Handlebar', 3),
('Front Brakes', 4),
('Jersey S', 5),
('Helmet L', 6);

INSERT INTO sales.salesorderheader (orderdate) VALUES
('2023-01-15'),
('2023-02-20'),
('2023-03-10');

INSERT INTO sales.salesorderdetail (salesorderid, productid, unitprice, orderqty, unitpricediscount) VALUES
(1, 1, 3399.99, 2, 0.00),
(1, 3, 1500.00, 1, 0.05),
(2, 2, 2500.00, 3, 0.00),
(2, 4, 89.99, 5, 0.10),
(3, 5, 106.50, 2, 0.00),
(3, 6, 49.99, 4, 0.00),
(3, 7, 34.99, 2, 0.00);

SELECT * FROM sales.salesorderdetail;

-- 1 task
SELECT COUNT(name), groupname
FROM humanresources.department
GROUP BY groupname
ORDER BY COUNT(name) DESC;

-- 2 task
SELECT MAX(eh.rate) AS MAX_RATE, e.nationalidnumber
FROM humanresources.employeepayhistory eh
JOIN humanresources.employee e ON eh.businessentityid = e.businessentityid
GROUP BY e.nationalidnumber;

-- 3 task
SELECT MIN(od.unitprice) AS MIN_PRICE, p.name, sb.name
FROM sales.salesorderdetail od
JOIN production.product p ON od.productid = p.productid
JOIN production.productsubcategory sb ON p.productsubcategoryid = sb.productsubcategoryid
GROUP BY p.name, sb.name;

-- 4 task
SELECT COUNT(sb.productsubcategoryid), c.name
FROM production.productsubcategory sb
JOIN production.productcategory c ON sb.productcategoryid = c.productcategoryid
GROUP BY c.name;

-- 5 task
SELECT AVG(od.unitprice * od.orderqty * (1 - unitpricediscount)) AS avg_total_sub, sb.name
FROM sales.salesorderdetail od
JOIN production.product p ON p.productid = od.productid
JOIN production.productsubcategory sb ON p.productsubcategoryid = sb.productsubcategoryid
GROUP BY sb.name;

-- 6 task
SELECT businessentityid, rate, ratechangedate
FROM humanresources.employeepayhistory
WHERE rate = (SELECT MAX(rate) FROM humanresources.employeepayhistory);