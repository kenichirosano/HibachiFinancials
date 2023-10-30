USE financials;

-- Number of companies by the industry
select listed, industry, count(distinct EdinetCode) AS 'No. of Company'
from EdinetCode 
#where listed = '上場'
#where listed like '非上場'
group by listed, industry
order by listed, industry, count(distinct EdinetCode) desc;

-- List of the companies in the industry
select name, industry, left(ticker,4)
from EdinetCode 
where listed = '上場'
and industry in ('食料品','小売業')
-- where listed like '非上場'
group by name, industry, ticker
order by count(distinct EdinetCode) desc;


