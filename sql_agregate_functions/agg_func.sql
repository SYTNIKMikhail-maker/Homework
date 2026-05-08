

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

--7task
SELECT MIN(od.unitprice) AS min_price, sb.name
FROM sales.salesorderdetail od
JOIN production.product p ON od.productid = p.productid
JOIN production.productsubcategory sb ON p.productsubcategoryid = sb.productsubcategoryid
GROUP BY sb.name
HAVING MIN(od.unitprice) > 100;

