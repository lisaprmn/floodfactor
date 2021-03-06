CREATE TABLE [dbo].[belgium_addresses]
(
	  [address_id] INT NOT NULL,
      [EPSG_31370_x] FLOAT,
	  [EPSG_31370_y] FLOAT,
	  [EPSG_4326_lat] FLOAT,
	  [EPSG_4326_lon] FLOAT,
	  [box_number] NVARCHAR(50),
	  [house_number] NVARCHAR(50),
	  [municipality_id] INT,
	  [municipality_name_de] NVARCHAR(100),
	  [municipality_name_fr] NVARCHAR(100),
	  [municipality_name_nl] NVARCHAR(100),
	  [postcode] INT,
	  [postname_fr] NVARCHAR(500),
	  [postname_nl] NVARCHAR(500),
	  [street_id] INT,
	  [streetname_de] NVARCHAR(500),
	  [streetname_fr] NVARCHAR(500),
	  [streetname_nl] NVARCHAR(500),
	  [region_code] NVARCHAR(255),
	  [status] NVARCHAR(50)
)

CREATE TABLE [dbo].[flooding_risk]
(
	[address_id] INT NOT NULL,
	[risk_level] NVARCHAR(50),
	[alea_type] NVARCHAR(50),
	[map_object_id] FLOAT,
	[map_local_id] NVARCHAR(100),
	[map_src_file] NVARCHAR(100)
)
