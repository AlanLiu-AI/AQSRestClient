SELECT 'ComplianceStatus' as LookupType, ComplianceCode as Code, ComplianceCodeDesc as CodeDescription
FROM tu_ComplianceStatus
UNION
SELECT 'ContactType' as LookupType, ContactTypeCode as Code, ContactTypeDesc as CodeDescription
FROM tu_ContactType
UNION
SELECT 'EventCategory' as LookupType, EventCatCode as Code, EventCatDesc as CodeDescription
FROM tu_EventCats
UNION
SELECT 'ExtractorTypes' as LookupType, ExtractorName as Code, ExtractorDesc as CodeDescription
FROM tu_ExtractorTypes WHERE ExtractorName Not Like 'ExtractorName%'
UNION
SELECT 'InspectionMaintenanceResult' as LookupType, InspectMaintResult as Code, InspectMaintResultDesc as CodeDescription
FROM tu_InspectMaintResult
UNION
SELECT 'NoteType' as LookupType, NoteTypeCode as Code, NoteTypeDesc as CodeDescription
FROM tu_NoteTypes

