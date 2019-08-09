SELECT 
	ContactID, 
	replace(replace(replace(ContactTitle, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS ContactTitle, 
	replace(replace(replace(ContactCompanyName, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS ContactCompanyName, 
	replace(replace(replace(ContactSalutation, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS ContactSalutation, 
	replace(replace(replace(ContactFirstName, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS ContactFirstName, 
	replace(replace(replace(ContactLastName, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS ContactLastName, 
    replace(replace(replace(ContactAddr1, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS ContactAddr1, 
	replace(replace(replace(ContactAddr2, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS ContactAddr2, 
	replace(replace(replace(ContactCity, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS ContactCity, 
	replace(replace(replace(ContactState, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS ContactState, 
	replace(replace(replace(ContactZip, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS ContactZip, 
	replace(replace(replace(ContactBusPhone, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS ContactBusPhone, 
	replace(replace(replace(ContactCellPhone, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS ContactCellPhone, 
	replace(replace(replace(ContactPager, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS ContactPager, 
	replace(replace(replace(ContactFax, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS ContactFax, 
	replace(replace(replace(ContactEmerPhone, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS ContactEmerPhone, 
	replace(replace(replace(ContactEmail, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS ContactEmail, 
	replace(replace(replace(ContactComments, '''', '.'),',','.'),CHAR(13)+CHAR(10),'\\n') AS ContactComments
FROM CTS_Data_AnchorageAK..t_Contacts
WHERE ContactID < 41919 --AND ContactID=1500
ORDER BY ContactID


SELECT 
	pa.PermitNo, pc.ContactID, pc.ContactTypeCode, pc.ProductType, pc.ContactPriority, pc.DateCreated
FROM CTS_Data_AnchorageAK..tl_Permits_Contacts pc
JOIN CTS_Data_AnchorageAK..t_Contacts c ON c.ContactID = pc.ContactID
JOIN CTS_Data_AnchorageAK..t_PermitAccounts pa ON pa.PermitID = pc.PermitID
JOIN CTS_Data_AnchorageAK..t_PermitOps po ON po.PermitID = pc.PermitID
WHERE pa.PermitType = 'FOG' AND po.ActivePermit=1 AND pc.ContactID < 41919
ORDER BY ContactID





