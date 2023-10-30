# create database financials;
USE financials;

/* -------------------- EdinetCode table creatation STEPS ------------------------
1. Download CSV from EDINET and open the file with ATOM
2. Change encoding to JIS and Remove the first row (file info) 
3. Copy the text and paste in new tab
4. Save as UTF-8 csv file
5. Import on MySQL Workbench using import wizard (selecting UTF-8, comma seperator)
6. Run this statements to alter column names to English

/* ------------------------- After importing the text file to create EdinetCode tab,e run the following statements to change the column names and data types ------------------------- */
ALTER TABLE EdinetCode CHANGE COLUMN ＥＤＩＮＥＴコード 	edinetCode varchar(10);
ALTER TABLE EdinetCode ADD CONSTRAINT PRIMARY KEY (edinetCode); 	# edinetCode is primary key column
ALTER TABLE EdinetCode CHANGE COLUMN 提出者種別 					entityType varchar(30);
ALTER TABLE EdinetCode CHANGE COLUMN 上場区分 						listed varchar(10);
ALTER TABLE EdinetCode CHANGE COLUMN 連結の有無 					consolidated varchar(8);
ALTER TABLE EdinetCode CHANGE COLUMN 資本金 equityAmount 	int;
ALTER TABLE EdinetCode CHANGE COLUMN 決算日 fiscalEnding 		varchar(30);
ALTER TABLE EdinetCode CHANGE COLUMN 提出者名 						name varchar(255);
ALTER TABLE EdinetCode CHANGE COLUMN 提出者名（英字） 			nameEnglish varchar(255);
ALTER TABLE EdinetCode CHANGE COLUMN 提出者名（ヨミ） 			ruby varchar(255);
ALTER TABLE EdinetCode CHANGE COLUMN 所在地 							address varchar(255);
ALTER TABLE EdinetCode CHANGE COLUMN 提出者業種 					industry varchar(30);
ALTER TABLE EdinetCode CHANGE COLUMN 提出者法人番号 corporateNumber varchar(30);

UPDATE EdinetCode
SET 証券コード = 0
WHERE 証券コード IS NULL OR 証券コード = '';

ALTER TABLE EdinetCode CHANGE COLUMN 証券コード 					ticker int null;
UPDATE EdinetCode SET ticker = LEFT(ticker,4);

