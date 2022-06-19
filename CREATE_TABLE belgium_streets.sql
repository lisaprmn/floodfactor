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

/* sql query to populate the table :  */

INSERT INTO belgium_streets (street_id, postcode, streetname_de, streetname_fr, streetname_nl, region_code, nb_count)
SELECT street_id, postcode, streetname_de, streetname_fr, streetname_nl, region_code, COUNT(*)
FROM belgium_addresses
GROUP BY street_id, postcode, streetname_de, streetname_fr, streetname_nl, region_code
HAVING COUNT(*) > 1