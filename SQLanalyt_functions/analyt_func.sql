--1task
WITH sales_ranked AS (
    SELECT p.name AS name, SUM(od.unitprice*od.orderqty*(1-od.unitpricediscount)) AS total_sales, PERCENT_RANK() OVER(ORDER BY SUM(od.unitprice*od.orderqty*(1-od.unitpricediscount))) AS pct_rank
    FROM sales.salesorderdetail od
    JOIN production.product p ON p.productid=od.productid
    JOIN sales.salesorderheader hd ON hd.salesorderid=od.salesorderid
    WHERE EXTRACT(YEAR FROM hd.orderdate) = 2013 AND EXTRACT(MONTH FROM hd.orderdate) = 1
    GROUP BY name
)
SELECT name, total_sales
FROM sales_ranked
WHERE pct_rank > 0.10 AND pct_rank < 0.90;

SELECT * FROM sales.salesorderheader;

--2task
SELECT p.name AS product_name, sb.name AS subcategory_name,
MIN(od.unitprice) OVER(PARTITION BY sb.productsubcategoryid) AS min_price
FROM production.product p
JOIN production.productsubcategory sb ON sb.productsubcategoryid=p.productsubcategoryid
JOIN sales.salesorderdetail od ON od.productid=p.productid;

--3task
WITH looking_for_rank AS (
    SELECT sb.name AS subcategory_name, od.unitprice AS price,
    DENSE_RANK() OVER (PARTITION BY productcategoryid ORDER BY od.unitprice) AS rnk
    FROM production.productsubcategory sb
    JOIN production.product p ON p.productsubcategoryid=sb.productsubcategoryid
    JOIN sales.salesorderdetail od ON od.productid=p.productid
)
SELECT DISTINCT subcategory_name, rank_, price
FROM looking_for_rank
WHERE rnk = 2;

--4task
WITH total_year_sum AS (
    SELECT DATE_TRUNC('year', oh.orderdate) AS year, cat.name AS name_cat, SUM(od.unitprice*od.orderqty*(1-od.unitpricediscount)) AS total_price
    FROM sales.salesorderdetail od
    JOIN sales.salesorderheader oh ON oh.salesorderid = od.salesorderid
    JOIN production.product p ON p.productid = od.productid
    JOIN production.productsubcategory sb ON sb.productsubcategoryid = p.productsubcategoryid
    JOIN production.productcategory cat ON cat.productcategoryid = sb.productcategoryid
    GROUP BY year, cat.name
),
prev AS (
    SELECT year, name_cat, total_price, LAG(total_price) OVER (PARTITION BY name_cat ORDER BY year) AS prev_sale
    FROM total_year_sum
)
SELECT year, name_cat, ROUND(((total_price-prev_sale)/prev_sale*100)::numeric, 2) AS YoY
FROM prev
WHERE year = '2023-01-01';

--5task
WITH total AS (
    SELECT DATE_TRUNC('day', dh.orderdate) AS date, MAX(od.unitprice*od.orderqty*(1-unitpricediscount)) AS total_price
    FROM sales.salesorderdetail od
    JOIN sales.salesorderheader dh ON od.salesorderid=dh.salesorderid
    GROUP BY DATE_TRUNC('day', dh.orderdate)
),
running_calc AS (
    SELECT date, total_price,
    MAX(total_price) OVER (ORDER BY date) AS running_max
    FROM total
)
SELECT date, running_max
FROM running_calc
WHERE date >= '2023-01-01' AND date < '2023-02-01';

--6task
WITH qty_sum AS (
    SELECT DATE_TRUNC('month', oh.orderdate) AS date, sb.name AS sub_name, p.name AS name, SUM(od.orderqty*od.unitprice) AS sum_qty
    FROM production.product p
    JOIN sales.salesorderdetail od ON od.productid=p.productid
    JOIN sales.salesorderheader oh ON oh.salesorderid=od.salesorderid
    JOIN production.productsubcategory sb ON sb.productsubcategoryid=p.productsubcategoryid
    WHERE oh.orderdate >= '2023-01-01' AND oh.orderdate < '2023-02-01'
    GROUP BY date, sb.name, p.name
),
running_max AS (
    SELECT date, sub_name, name, sum_qty, DENSE_RANK() OVER (PARTITION BY sub_name ORDER BY sum_qty DESC) AS rnk
    FROM qty_sum
)
SELECT date, sub_name, name, sum_qty
FROM running_max
WHERE rnk = 1;
