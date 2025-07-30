USE[TestDB]
SELECT TOP(1)
    *
FROM 
-- declare @HubID nvarchar(100)

-- --set @HubID = null

-- if (@HubID = 'ALL')
-- begin
--     Set @HubID = null
-- end


-- declare @StartDateTime datetime;
-- declare @EndDateTime datetime;
-- DECLARE @OldDateTime datetime;

-- set @EndDateTime =  dateadd(hour,4, left(convert(varchar, getdate(),120),10))
-- set @StartDateTime = dateadd(day,-1, @EndDateTime)
-- SET @OldDateTime = dateadd(day,-3,@StartDateTime)
-- --declare @datefrom datetime = '2019-01-26'
-- --set @EndDateTime =  dateadd(hour,4, left(convert(varchar, @datefrom,120),10))
-- --set @StartDateTime = dateadd(day,-1, @EndDateTime)

-- select I.RouteName, I.ConsignmentID, I.BilledTo, I.ConsignedDT, I.ShipperReference, I.DeliveryAttempts, I.LastDeliveryAttempt, I.Hub, I.NonDeliveryDT, I.AuthReason, I.AuthorisorID, I.AuthorisorName, I.LastReason as ReasonCapturedbyCourier,
--     I.DriverID as CourierID, I.Firstname + I.LastName as CourierName, I.CourierEmployeeNo, I.CrewEmployeeNo, I.CrewName, I.RouteAllocatedToID, I.RouteAllocatedToName,
--     I.CustomerGroupID, I.FullAddress, I.Suburb, I.Area, I.Township

-- from(	SELECT ISNULL(F.RouteName,'') AS RouteName,
--         A.ConsignmentID, B.BilledTo, dbo.udf_TimeUnixToSQL(B.LastParcelDateTime) as ConsignedDT,
--         ISNULL(B.ShipperReference,'') AS ShipperReference,
--         RAMTnTv1.dbo.udf_DeliveryAttempts(A.ConsignmentID) AS DeliveryAttempts,
--         CONVERT(VARCHAR(10), F.EventDateTime,120) AS LastDeliveryAttempt,
--         F.HubID AS Hub,
--         ND.RecordDT AS NonDeliveryDT,
--         ISNULL(F.AuthNote,'') AS AuthReason,
--         ISNULL(F.AuthorisorID,'') AS AuthorisorID,
--         ISNULL(F.AuthorisorName,'') AS AuthorisorName,
--         ISNULL(ND.Reason,'') AS LastReason,
--         F.DriverID, F.Firstname, F.LastName, F.EmployeeNo AS CourierEmployeeNo,
--         isnull(F.CrewEmployeeNo, '') AS CrewEmployeeNo, isnull(F.CrewName, '') AS CrewName,
--         isnull(SDVD.RouteAllocatedToID, '') AS RouteAllocatedToID,
--         isnull(SDVD.RouteAllocatedToName, '') AS RouteAllocatedToName,
--         X.CustomerGroupID,

--         (IsNull(X.StreetAddress1,'') + '' + IsNull(X.StreetAddress2,''))as FullAddress,
--         Z.Suburb, Z.Area, Z.Township
--     FROM RMSEEv4.dbo.ConsignmentStatus AS A WITH (NOLOCK)
--         LEFT JOIN ConsignmentsArchive AS B WITH (NOLOCK) ON A.ConsignmentID = B.ConsignmentID
--         left join Customers as X WITH (NOLOCK) ON B.ReceiverID = X.CustomerID
--         left join RAMTnTv1.dbo.vw_zones_All AS Z WITH (NOLOCK) ON Z.ZoneId= X.ZoneId
--         LEFT JOIN RAMTnTv1.dbo.PODCapturePOD AS C ON C.ConsignmentID = A.ConsignmentID
-- 			--outer apply (select top 1 * from RAMMobile.dbo.vw_sync_NonDelivery as ND with (nolock) where ND.ConsignmentID = A.ConsignmentID and ND.RecordDT between @StartDateTime and @EndDateTime order by ND.RecordDT desc) as ND
-- 			outer apply (select top 1
--             *
--         from RAMMobile.dbo.Sync_NonDelivery as ND with (nolock)
--         where ND.ConsignmentID = A.ConsignmentID and ND.RecordDT between @StartDateTime and @EndDateTime
--         order by ND.RecordDT desc) as ND
--         LEFT JOIN (SELECT
--             D.ConsignmentID,
--             D.EventDateTime,
--             E.AuthNote,
--             E.AuthorisorID,
--             e3.FirstName + ' ' + e3.LastName AS AuthorisorName,
--             I.HubID,
--             DA.DriverID, Empl.Firstname, Empl.LastName, Empl.EmployeeNo, e2.EmployeeNo AS CrewEmployeeNo, e2.FirstName + ' ' + e2.LastName AS CrewName,
--             (SELECT TOP 1
--                 BB.RouteName
--             FROM dbo.DelVehDepRoute AS AA LEFT JOIN Routes AS BB ON AA.RouteID = BB.RouteID
--             WHERE DelVehDepID = I.DelVehDepID) AS RouteName
--         FROM RAMTnTv1.dbo.DelVehArrNonDel AS D WITH (NOLOCK)
--             LEFT JOIN RAMTnTv1.dbo.DelVehArr AS I WITH (NOLOCK) ON I.DelVehArrID = D.DelVehArrID
--             LEFT JOIN RAMTnTv1.dbo.TrackingAuth AS E WITH (NOLOCK) ON D.TrackingAuthID = E.TrackingAuthID
--             left join RAMTnTv1.dbo.DelVehArr AS DA WITH (NOLOCK) ON DA.DelVehArrID = D.DelVehArrID
--             left join RAMTnTv1.dbo.Employees AS Empl WITH (NOLOCK) ON Empl.EmployeeID = DA.DriverID
--             LEFT JOIN RAMTnTv1.dbo.Employees AS e2 WITH (NOLOCK) ON e2.EmployeeID = DA.CoDriverID
--             LEFT JOIN RAMTnTv1.dbo.Employees AS e3 WITH (NOLOCK) ON e3.EmployeeID = E.AuthorisorID
--         WHERE D.DelVehArrID = (SELECT MAX(DelVehArrID)
--             FROM
--                 RAMTnTv1.dbo.DelVehArrNonDel AS G WITH (NOLOCK)
--             WHERE G.ConsignmentID = D.ConsignmentID)
--             and (isnull(@HubID,'') = '' or I.HubID IN (select ltrim(rtrim(value))
--             from dbo.udf_split(@HubID, ',')))
-- 							) AS F ON A.ConsignmentID = F.ConsignmentID
--         LEFT JOIN RAMTnTv1.dbo.MiscClosure AS H WITH (NOLOCK) ON A.ConsignmentID = H.ConsignmentID
-- 			outer apply (SELECT TOP 1
--             *
--         FROM RAMSQLCOL10.RAMMobileDash.dbo.SummaryByDelVehDep WITH (nolock)
--         WHERE RecordDT between @OldDateTime and @EndDateTime and RouteNames = F.RouteName
--         order by RecordDT desc) as SDVD
--     --outer apply (SELECT TOP 1 * FROM RAMMobileDash.dbo.SummaryByDelVehDep WITH (nolock) WHERE RecordDT between @OldDateTime and @EndDateTime and RouteNames = F.RouteName order by RecordDT desc) as SDVD

--     WHERE C.ReceivedDateTime IS NULL
--         AND CONVERT(VARCHAR(10),F.EventDateTime,120) = CONVERT(VARCHAR(10), DATEADD(DAY,-1,@EndDateTime), 120)
-- 			--AND H.ConsignmentID IS NULL
-- 			) as I


-- GROUP BY I.RouteName, I.ConsignmentID, I.BilledTo, I.ConsignedDT, I.ShipperReference, I.DeliveryAttempts, I.LastDeliveryAttempt, I.Hub,I.NonDeliveryDT, I.AuthReason, I.AuthorisorID, I.AuthorisorName,
-- 			I.LastReason, I.DriverID, I.Firstname, I.LastName, I.CourierEmployeeNo, I.CrewEmployeeNo, I.CrewName, I.RouteAllocatedToID, I.RouteAllocatedToName,I.CustomerGroupID,I.FullAddress,I.Suburb,I.Area,I.Township
-- ORDER BY I.RouteName, I.ConsignmentID, I.ShipperReference, I.DeliveryAttempts, I.LastDeliveryAttempt, I.Hub, I.LastReason