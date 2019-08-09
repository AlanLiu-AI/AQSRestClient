SELECT 
	--Permittee,PermitNo,SiteAddr1,SiteCity,SiteState,SiteZipCode
	replace(replace(replace(Permittee, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS Permittee, 
	replace(replace(replace(PermitNo, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS PermitNo, 
	replace(replace(replace(SiteAddr1, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS SiteAddr1, 
	replace(replace(replace(SiteCity, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS SiteCity, 
	replace(replace(replace(SiteState, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS SiteState, 
	replace(replace(replace(SiteZipCode, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS SiteZipCode 
FROM CTS_Data_AnchorageAK.dbo.t_PermitAccounts p
INNER JOIN CTS_Data_AnchorageAK.dbo.t_Site s ON s.SiteID = p.SiteID
WHERE p.PermitType LIKE 'HLR' AND p.PermitID < 50000
ORDER BY p.PermitID ASC