USE financials;

/* The way to import edinet code cvs file
1. Download CVS from EDINET and open the file
2. Remove the first row (file info) 
3. Save as UTF-16 txt file
4. Open txt in text editor and save as CVS
5. Import on MySQL Workbench using import wizard (selecting UTF-16, tab seperator)
6. Run the statements to alter column names to English
*/

/* ------------------------- After importing the text file to create EdinetCode tab,e run the following statements to change the column names and data types ------------------------- */
ALTER TABLE EdinetCode CHANGE COLUMN ＥＤＩＮＥＴコード edinetCode varchar(10);
ALTER TABLE EdinetCode ADD CONSTRAINT PRIMARY KEY (edinetCode);
ALTER TABLE EdinetCode CHANGE COLUMN 提出者種別 entityType varchar(30);
ALTER TABLE EdinetCode CHANGE COLUMN 上場区分 listed varchar(8);
ALTER TABLE EdinetCode CHANGE COLUMN 連結の有無 consolidated varchar(8);
ALTER TABLE EdinetCode CHANGE COLUMN 資本金 equityAmount int;
ALTER TABLE EdinetCode CHANGE COLUMN 決算日 fiscalEnding varchar(30);
ALTER TABLE EdinetCode CHANGE COLUMN 提出者名 name varchar(255);
ALTER TABLE EdinetCode CHANGE COLUMN 提出者名（英字） nameEnglish varchar(255);
ALTER TABLE EdinetCode CHANGE COLUMN 提出者名（ヨミ） ruby varchar(255);
ALTER TABLE EdinetCode CHANGE COLUMN 所在地 address varchar(255);
ALTER TABLE EdinetCode CHANGE COLUMN 提出者業種 industry varchar(10);
ALTER TABLE EdinetCode CHANGE COLUMN 証券コード ticker int;
ALTER TABLE EdinetCode CHANGE COLUMN 提出者法人番号 corporateNumber varchar(30);
CREATE INDEX companyNameJ_idx on EdinetCode(name);
CREATE INDEX companyNameE_idx on EdinetCode(nameEnglish);
update EdinetCode a, EdinetCode b set a.ticker = left(b.ticker,4) 
where a.edinetCode = b.edinetCode;
CREATE INDEX companyEdinetCode_idx on EdinetCode(ticker);
/* ------------------------- Run the following statements ------------------------- */

/*
Previously when the table was not imported and createed from scrach,
the following is the statement to create Edinetcode table from scratch (when import was not used.)
Create table if not exists EdinetCode(
	edinetCode varchar(255),
    entityType varchar(255),
    listed varchar(255),
    consolidated varchar(255),
    equityAmount varchar(255),
    fiscalEnding varchar(255),
    name varchar(255),
    nameEnglish varchar(255),
    ruby varchar(255),
    address varchar(255),
    industry varchar(255),
    ticker varchar(255),
    corporateNumber varchar(255),
    
    PRIMARY KEY (edinetCode)
);
*/

# Number of companies by the industry
select listed, industry, count(distinct EdinetCode) AS 'No. of Company'
from EdinetCode 
where listed = '上場'
#where listed like '非上場'
group by listed, industry
order by count(distinct EdinetCode) desc;

# Number of companies by the industry
select *
from EdinetCode 
where listed = '上場' and industry = 'サービス業' ;

