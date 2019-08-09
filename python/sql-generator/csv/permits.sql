SELECT pa.PermitId, pa.PermitNo,pa.Permittee,s.SiteNo,s.SiteCompany,s.SiteAddr1,s.SiteCity,s.SiteState,s.SiteZipCode,s.MapCategory
FROM CTS_Data_AnchorageAK..t_PermitAccounts pa
JOIN CTS_Data_AnchorageAK..t_PermitOps po ON po.PermitID = pa.PermitID
JOIN CTS_Data_AnchorageAK..t_Site s ON s.SiteID = pa.SiteID
WHERE po.ActivePermit = 1 AND pa.PermitType = 'FOG' AND pa.PermitId < 50000

