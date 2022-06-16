CREATE TABLE [dbo].[belgium_addresses]
(
      [EPSG_31370_x] FLOAT,
	  [EPSG_31370_y] FLOAT,
	  [EPSG_4326_lat] FLOAT,
	  [EPSG_4326_lon] FLOAT,
	  [address_id] INT NOT NULL,
	  [box_number] NVARCHAR(50),
	  [house_number] NVARCHAR(50),
	  [municipality_id] INT,
	  [municipality_name_de] NVARCHAR(100),
	  [municipality_name_fr] NVARCHAR(100),
	  [municipality_name_nl] NVARCHAR(100),
	  [postcode] SMALLINT,
	  [postname_fr] NVARCHAR(500),
	  [postname_nl] NVARCHAR(500),
	  [street_id] INT,
	  [streetname_de] NVARCHAR(500),
	  [streetname_fr] NVARCHAR(500),
	  [streetname_nl] NVARCHAR(500),
	  [region_code] NVARCHAR(255),
	  [status] NVARCHAR(50)
)