SELECT *
FROM [RAMTnTv1].[dbo].[MorningExceptions]

-- USE [RAMTnTv1]
-- declare	@DaysAgo INT = 1,
--     @HubID VARCHAR(100) = 'ALL' ,
--     @Supervisor VARCHAR(100)  = 'ALL'

-- SET NOCOUNT ON;

-- DECLARE @StartDT DATETIME, @EndDT DATETIME;
-- SET @StartDT = DATEADD(d,-@DaysAgo,CONVERT(VARCHAR(10),GETDATE(),120));
-- SET @EndDT = CONVERT(VARCHAR, DATEADD(MINUTE, +1439 , @StartDT), 100);

-- /* Prepare Departures and Departure Mobile Activity Times - START */

-- IF OBJECT_ID(N'tempdb..#DelVehDeps') IS NOT NULL
-- BEGIN
--     DROP TABLE #DelVehDeps
-- END
-- IF OBJECT_ID(N'tempdb..#DelVehDepActivityTimes') IS NOT NULL
-- BEGIN
--     DROP TABLE #DelVehDepActivityTimes
-- END

-- CREATE TABLE #DelVehDeps
-- (
--     DelVehDepID VARCHAR(16),
--     OpenDateTime DATETIME,
--     CloseDateTime DATETIME,
--     DriverID VARCHAR(16),
--     CoDriverID VARCHAR(16)
-- )
-- CREATE TABLE #DelVehDepActivityTimes
-- (
--     DelVehDepID VARCHAR(16),
--     MobileActivityTimes VARCHAR(100)
-- )

-- INSERT INTO #DelVehDeps
--     (DelVehDepID, OpenDateTime, CloseDateTime, DriverID, CoDriverID)
-- SELECT
--     DVD.DelVehDepID, DVD.OpenDateTime, DVD.CloseDateTime, DVD.DriverID, DVD.CoDriverID
-- FROM
--     DelVehDep AS DVD WITH(NOLOCK)
-- WHERE
--     DVD.CloseDateTime BETWEEN @StartDT AND @EndDT

-- INSERT INTO #DelVehDepActivityTimes
--     (DelVehDepID, MobileActivityTimes)
-- SELECT
--     DVD.DelVehDepID,
--     [RAMMobile].[dbo].[udf_MobileActivityTimes](DVD.DelVehDepID)
-- FROM
--     #DelVehDeps AS DVD

-- /* END */

-- SELECT DISTINCT
--     E.EmployeeNo,
--     E.FirstName + ' ' + E.LastName as 'EmployeeName',
--     ISNULL(SC.TK_Department,'') AS Department,
--     ISNULL(SC.VIP_Position,'') AS Position,
--     E.HubID,
--     CAST(WE.Date AS DATE) as DATE,
--     ISNULL(WE.Shift_Start,'') AS ShiftStart,
--     ISNULL(CONVERT(VARCHAR(5), WE.In1, 108), '00:00')  AS StartTime,
--     CONVERT(VARCHAR(8), WE.Out1, 108)  AS EndTime,
--     WE.Total_OT,
--     ISNULL(convert(float,DD.ScanningTimeAM)/1440,'') AS ScanningTimeAM,
--     ISNULL(CONVERT(VARCHAR(5), DD.DepartureDT, 108), '00:00')  as DepartureTime,
--     convert(varchar(8), WE.Shift_Start, 114) as shiftstart,
--     --convert(varchar(5),WE.In1, 108) as in1,
--     case when convert(varchar(5), WE.Shift_Start, 114) >= convert(varchar(5),WE.In1, 114) and WE.Shift_Start != 'None' and DD.DepartureDT is not null and we.Shift_Start < '24:00'
--  	         then convert(varchar(3), datediff(minute,  CONVERT(varchar(5), WE.Shift_Start,114), CONVERT(varchar(8), DD.DepartureDT,114))/60)+':'+right('0'+ convert(varchar(2), datediff(minute,   CONVERT(varchar(8), WE.Shift_Start,114), CONVERT(varchar(8), DD.DepartureDT,114))%60),2) -- RIGHT(CONVERT(varchar(8), WE.Shift_Start ,100), 7))
--           when  convert(varchar(5), WE.Shift_Start, 114) < convert(varchar(5),WE.In1, 114) and WE.Shift_Start != 'None' and DD.DepartureDT is not null and we.Shift_Start < '24:00'
--  		 then  convert(varchar(3), datediff(minute,   convert(varchar(5),WE.In1, 114), ISNULL(CONVERT(VARCHAR(5), DD.DepartureDT, 114), '00:00'))/60)+':'+right('0'+ convert(varchar(2),datediff(minute,    convert(varchar(5),WE.In1, 114), ISNULL(CONVERT(VARCHAR(5), DD.DepartureDT, 114), '00:00'))%60),2)
--  		 else '0:00'
--  		 end as 'LeaveHubTime',

--     ISNULL(CONVERT(VARCHAR(8), DA.ArrivalDT, 108), '00:00:00')  as ArrivalTime,
--     ISNULL(dbo.udf_DelVehDepIDsbyDriver(E.EmployeeID,@StartDT,@EndDT), '') AS DepartureID,
--     ISNULL(DD.DeliveryStops, 0) AS DeliveryStops,
--     ISNULL(DD.TotalConsignmentCount, 0) AS TotalConsignmentCount,
--     ISNULL(DA.PODConsignmentCount, 0) AS PODConsignmentCount,
--     ISNULL(DA.NonDelConsignmentCount, 0) AS NonDelConsignmentCount,
--     ISNULL(DA.LossTheftConsignmentCount, 0) as LossTheftConsignmentCount,
--     ISNULL(DA.CollectedConsignmentCount, 0) AS CollectedConsignmentCount,
--     ISNULL(DD.RouteNames, '') AS RouteNames,
--     ISNULL(	CONVERT(CHAR(16),DD.FirstActivityOnMobileTime,120), '') AS FirstActivityOnMobileTime,
--     ISNULL(	CONVERT(CHAR(16), DD.LastActivityOnMobile,120), '') AS LastActivityOnMobile
-- FROM
--     RAMTnTv1.dbo.Employees AS E WITH (NOLOCK)
--     LEFT JOIN [RAMCOLOSYNSQL01].[TKSQL].[dbo].[8am_HR_Syn_Compare] AS SC WITH (NOLOCK) ON VIP_EMPLOYEE = SUBSTRING(E.EmployeeNo, PATINDEX('%[^0 ]%', E.EmployeeNo + ' '), LEN(E.EmployeeNo))
--     LEFT JOIN [RAMCOLOSYNSQL01].[TKSQL].[dbo].[8am_Daily] AS WE WITH (NOLOCK) ON WE.Emp_NO = SUBSTRING(E.EmployeeNo, PATINDEX('%[^0 ]%', E.EmployeeNo + ' '), LEN(E.EmployeeNo)) COLLATE database_default

--  OUTER APPLY (
--  	SELECT
--         MIN(LEFT(DVDA.MobileActivityTimes, LTRIM(RTRIM(CHARINDEX('|', DVDA.MobileActivityTimes +'|')-1)))) AS 'FirstActivityOnMobileTime',

--         MAX(LTRIM(RTRIM(LEFT(STUFF(DVDA.MobileActivityTimes, 1, CHARINDEX('|', DVDA.MobileActivityTimes +'|'), ''), CHARINDEX('|',STUFF(DVDA.MobileActivityTimes , 1, CHARINDEX('|', DVDA.MobileActivityTimes +'|'), '')+'|')-1) ))) AS 'LastActivityOnMobile',

--         MAX(DVD.CloseDateTime) AS DepartureDT,
--         SUM(DATEDIFF(MINUTE, DVD.OpenDateTime, DVD.CloseDateTime)) as ScanningTimeAM,
--         COUNT(DVD.DelVehDepID) AS Departures,
--         SUM(MSD.TotalConsignmentCount) AS TotalConsignmentCount,
--         SUM(MSD.TotalParcelCount) AS TotalParcelCount,
--         SUM(MSD.DeliveryStops) AS DeliveryStops,
--         MAX(dbo.udf_DelVehDepRouteNamesbyDriver(DVD.DriverID, @StartDT, @EndDT)) as RouteNames,
--         MAX(dbo.udf_DelVehDepRegistrationNobyDriver(DVD.DriverID, @StartDT, @EndDT)) as RegistrationNos
--     FROM
--         #DelVehDeps AS DVD WITH(NOLOCK) INNER JOIN
--         #DelVehDepActivityTimes AS DVDA ON DVD.DelVehDepID = DVDA.DelVehDepID LEFT JOIN
--         MovementSummary AS MSD WITH(NOLOCK) ON MSD.MovementID = DVD.DelVehDepID AND MSD.CloseDateTime = DVD.CloseDateTime
--     WHERE
--  		DVD.CloseDateTime BETWEEN @StartDT AND @EndDT
--         AND (DVD.DriverID = E.EmployeeID OR DVD.CoDriverID = E.EmployeeID)
--  ) AS DD

--  OUTER APPLY (
--  	SELECT
--         SUM(DATEDIFF(mi,DVA.OpenDateTime, DVA.CloseDateTime)) as ScanningTimePM,
--         MAX(DVA.openDateTime) as ArrivalDT,
--         COUNT(DelVehDepID) as Arrivals,
--         SUM(MSA.PODConsignmentCount) AS PODConsignmentCount,
--         SUM(MSA.PODParcelCount) AS PODParcelCount,
--         SUM(MSA.NonDelConsignmentCount) AS NonDelConsignmentCount,
--         SUM(MSA.NonDelParcelCount) AS NonDelParcelCount,
--         SUM(MSA.LossTheftConsignmentCount) AS LossTheftConsignmentCount,
--         SUM(MSA.LossTheftParcelCount) AS LossTheftParcelCount,
--         SUM(MSA.CollectedConsignmentCount) AS CollectedConsignmentCount,
--         SUM(MSA.CollectedParcelCount) AS CollectedParcelCount
--     FROM
--         DelVehArr AS DVA WITH(NOLOCK)
--         LEFT JOIN MovementSummary AS MSA WITH(NOLOCK) ON MSA.MovementID = DVA.DelVehArrID AND MSA.CloseDateTime = DVA.CloseDateTime
--     WHERE
--  		DVA.CloseDateTime BETWEEN @StartDT AND @EndDT
--         AND (DVA.DriverID = E.EmployeeID OR DVA.CoDriverID = E.EmployeeID)
--  ) AS DA

-- WHERE
--  	E.isActive = 1
--     AND WE.Shift_Start  <> 'None'
--     AND (@Supervisor = 'All' OR WE.Supervisor = @Supervisor)
--     AND (@HubID = 'All' OR HubID IN (select ltrim(rtrim(value))
--     from dbo.udf_split(@HubID, ',')))
--     AND [Date] BETWEEN @StartDT and @EndDT
