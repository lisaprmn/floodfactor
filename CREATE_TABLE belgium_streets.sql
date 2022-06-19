CREATE TABLE [Flood_factor].[dbo].[belgium_streets]
(
	  [street_id] INT ,	
	  [postcode] SMALLINT,
	  [streetname_de] NVARCHAR(500),
	  [streetname_fr] NVARCHAR(500),
	  [streetname_nl] NVARCHAR(500),
	  [region_code] NVARCHAR(255),
	  [nb_count] INT
)