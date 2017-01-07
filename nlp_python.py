#!/usr/bin/env python
import MySQLdb as mdb
import sys
from datetime import date
from dateutil.relativedelta import relativedelta
import re
import locale
import os
import json

######### Please set the environmental variables for database configuration #########

DB_USERNAME = os.environ.get('NLP_DB_USERNAME')
DB_PASSWORD = os.environ.get('NLP_DB_PASSWORD')
DB_HOST = os.environ.get('NLP_DB_HOST')
DB_NAME = os.environ.get('NLP_DB_NAME')

######### Please set the environmental variables for database configuration #########

DATA = 'data'
PROJECTID = 'projectid'
MINBUDGET = 'minBUDGET'
MAXBUDGET = 'maxBUDGET'
MAXBHK = 'maxBHK'
PROPTYPE = 'propType'
APARTMENT = 'apartment'
PLOT = 'plot'
LAND = 'LAND'
TOTAL_PROPTYPE = 'APARTMENT,LAND,ROW HOUSE,VILLA,VILLAMENT,BUNGALOW'
POSSESSION = 'possession'
AREAUNIT = 'areaUnit'
MINAREA = 'minArea'
MAXAREA = 'maxArea'
AMENITIES = 'amenities'
CITYID = 'city_id'
LOCKEYWORD = 'LocKeyword'
LAKH = 100000
CRORE = 10000000
SITE_URL = 'https://www.hdfcred.com'
FLD_PROJECTIMAGE2 = 'https://www.hdfcred.com/project-images1'
DOCUMENT_ROOT = ''
ALWAYS_LIST = [
	'inLocation', 'notInLocation', 'distLocation', 'nearByLocation', 
	'aroundLocation', 'directionLocation', 'LocKeyword', 'inLat', 
	'inLong', 'notInLat', 'notInLong', 'distLat', 'distLong',
	'nearByLat', 'nearByLong', AMENITIES
]

LATLNG_TO_KM = 0.008

CITIES = [
	'Mumbai','Pune','Bangalore','Hyderabad','Chennai',
	'Delhi','Agra','Ahmedabad','Aurangabad','Bhopal',
	'Bhubaneswar','Chandigarh','Guwahati','Indore','Jaipur',
	'Kanpur','Kerala','Kolkata','Lucknow','Meerut','Mysore',
	'Nashik','Vadodara','Kochi','Thrissur','Calicut','Trivandrum',
	'Kottayam','Thiruvalla','Kannur','Palakkad'
]

BEDROOMS = [
	"-1","0","0.3","0.5","1",
	"1.5","2","2.5","3","3.5",
	"4","4.5","5","5.5","6","6.5",
	"7","7.5","8","8.5","9",
	"9","9.5","10","10.5"
]

POSSESSIONS = [0, 3, 6, 12, 24, 36, 36]
CONVERSION_UNITS = [0.0010764, 10.764, 43560, 1, 107639.11, 27878400, 9, 1076.4]

class NLP(object):
	initalized = None
	def __new__(cls, **kwargs):
		if cls.initalized == None:
			try:
				cls.db = mdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME)
				cls.cursor = cls.db.cursor(mdb.cursors.DictCursor)
			except mdb.Error, e:
				print "Error %d: %s" % (e.args[0],e.args[1])
				sys.exit(1)
			cls.initalized = True
		return object.__new__(cls, **kwargs)

	def __init__(self, **kwargs):
		locale.setlocale(locale.LC_MONETARY, 'en_IN.UTF-8')
		self.input_data = {DATA: {}}
		self.query_list = list()
		self.total_project_count = 0
		self.proptype_flag = False
		for key, value in kwargs.items():
			self.convert_to_list(key, value)

	def get(self):
		self.get_max_bhks()
		if PROJECTID in self.input_data[DATA].keys():
			if not self.input_data[DATA][PROJECTID]:
				return json.dumps({'message': 'failure', 'status': 2, 'data': []})
			else:
				project_info = self.project_info(self.input_data[DATA][PROJECTID])
				return json.dumps({'message': 'success', 'status': 1, 'total': self.total_project_count, 'data': project_info})
			return
		return self.get_location_keyword()

	def get_location_keyword(self):
		query = ""
		if self.input_data[DATA].get(MINBUDGET) != None and self.input_data[DATA].get(MAXBUDGET) != None:
			query += " AND `minimum_price` BETWEEN %d AND %d " % (self.input_data[DATA][MINBUDGET], self.input_data[DATA][MAXBUDGET])
		elif self.input_data[DATA].get(MAXBUDGET) != None:
			query += " AND `minimum_price` <= %d " % (self.input_data[DATA][MAXBUDGET])
		elif self.input_data[DATA].get(MINBUDGET) != None:
			query += " AND `minimum_price` >= %d " % (self.input_data[DATA][MINBUDGET])
		if self.input_data[DATA].get(MAXBHK) != None:
			query += " AND `No_Of_Bedroom` IN (%s) " % (self.max_bhks_string)
		if self.input_data[DATA].get(PROPTYPE) != None:
			proptype = self.input_data[DATA][PROPTYPE]
			proptype_list = proptype.lower().split(',')
			if APARTMENT in proptype_list or PLOT in proptype_list:
				self.proptype_flag = True
			if proptype.lower() == PLOT:
				proptype = LAND
		else:
			proptype = TOTAL_PROPTYPE
		query += " AND FIND_IN_SET(Config_Type,'%s') " % (proptype)
		if self.input_data[DATA].get(POSSESSION) != None:
			possession = self.input_data[DATA][POSSESSION]
			from_date = date.today()
			to_date = (from_date + relativedelta(months=+POSSESSIONS[possession])).strftime('%Y-%m-%d')
			from_date = from_date.strftime('%Y-%m-%d')
			if possession == 0:
				query += " AND Possession <= '%s' " % (from_date)
			elif possession > 0 and possession < 6:
				query += " AND Possession BETWEEN '%s' AND '%s' " % (from_date, to_date)
			elif possession == 6:
				query += " AND Possession >= '%s' " % (to_date)
		if self.input_data[DATA].get(AREAUNIT) != None:
			area_unit = self.input_data[DATA][AREAUNIT]
		else:
			area_unit = 4
		if self.input_data[DATA].get(MINAREA) != None and self.input_data[DATA].get(MAXAREA) != None:
			minArea = self.area_conversion(self.input_data[DATA][MINAREA], area_unit)
			maxArea = self.area_conversion(self.input_data[DATA][MAXAREA], area_unit)
			query += " AND Area_Value_Sort BETWEEN %d AND %d " % (minArea, maxArea)
		elif self.input_data[DATA].get(MINAREA) != None:
			minArea = self.area_conversion(self.input_data[DATA][MINAREA], area_unit)
			query += " AND Area_Value_Sort >= %d " % (minArea)
		elif self.input_data[DATA].get(MAXAREA) != None:
			maxArea = self.area_conversion(self.input_data[DATA][MAXAREA], area_unit)
			query += " AND Area_Value_Sort <= %d " % (maxArea)
		if self.input_data[DATA].get(AMENITIES) != None:
			amenities_list = self.input_data[DATA][AMENITIES]
			amenity_query = list()
			for amenity in amenities_list:
				amenity_query.append("amenity_code like '%{:s}%'".format(amenity))
			query += " AND (%s) " % (" or ".join(amenity_query))
		if self.input_data[DATA].get(CITYID) != None:
			query += " AND Project_City in (%d)" % (self.input_data[DATA][CITYID])
		if self.input_data[DATA].get(LOCKEYWORD) != None and len(self.input_data[DATA][LOCKEYWORD]) > 0:
			for locKey in self.input_data[DATA][LOCKEYWORD]:
				if locKey == 'in':
					self.distance = 5
					self.limit = 1
					self.get_location('inLocation', 'in', locKey, query)
				elif locKey == 'notIn':
					self.distance = 5
					self.limit = 1
					self.get_location('notInLocation', 'not in', locKey, query)
				elif locKey == 'dist':
					self.distance = 5
					self.limit = 1
					self.get_location('distLocation', 'in', locKey, query)
				elif locKey == 'nearBy':
					self.distance = 20
					self.limit = 5
					self.get_location('nearByLocation', 'in', locKey, query)
				elif locKey == 'around':
					self.distance = 20
					self.limit = 5
					self.get_location('aroundLocation', 'in', locKey, query)
				elif locKey == 'direction':
					self.distance = 20
					self.limit = 5
					self.get_location('directionLocation', 'in', locKey, query)
		else:
			if self.input_data[DATA].get('sort') != None:
				sort_cond = " order by %s %s " % (self.input_data[DATA].get('sort'), self.input_data[DATA].get('sort_by')) 
			self.query_process("", query, sort_cond)
		project_ids = list()
		for qry in self.query_list:
			NLP.cursor.execute(qry)
			result = NLP.cursor.fetchall()
			project_ids.extend(map(lambda r: str(r['project_no']), result))
		project_id_string = ','.join(set(project_ids))
		if project_id_string:
			project_info = self.project_info(project_id_string)
			return json.dumps({'message': 'success', 'status': 1, 'total': self.total_project_count, 'data': project_info}) # give success response
		else:
			return json.dumps({'message': 'failure', 'status': 2, 'data': []}) # give failure response

	def get_location(self, location_key, identify_key, locKey, query):
		cond_location = ""
		if len(self.input_data[DATA][location_key]) > 0:
			city_code = list()
			suburb_code = list()
			area_code = list()
			order_cond_by = list()
			having_cond_by = list()
			select = order_by = having = ""
			if locKey == 'in' or locKey == 'dist':
				i = 1
				select = list()
				for key, area in enumerate(self.input_data[DATA][location_key]):
					area_lat = self.input_data[DATA][locKey+"Lat"][key]
					area_lng = self.input_data[DATA][locKey+"Long"][key]
					get_location_find = self.find_location_code(area, area_lat, area_lng, locKey)
					if get_location_find:
						if get_location_find['from_gt'] == 'City' and get_location_find.get('get_code') != None:
							city_code.extend(get_location_find['get_code'])
						elif get_location_find['from_gt'] == 'Suburb' and get_location_find.get('get_code') != None:
							suburb_code.extend(get_location_find['get_code'])
						elif get_location_find['from_gt'] == 'Area' and get_location_find.get('get_code') != None:
							area_code.extend(get_location_find['get_code'])
					select_query = """ ( 6371 * acos(
								cos( radians(%f) ) * 
								cos( radians( Map_Latitude ) ) * 
								cos( radians( Map_Longitude ) - radians(%f) ) + 
								sin( radians(%f) ) *
								sin( radians( Map_Latitude ) ) 
								)
							) as distance%d """ % (round(float(area_lat.strip()), 8), round(float(area_lng.strip()), 8), round(float(area_lat.strip()), 8), i)
					select.append(select_query)
					if len(self.input_data[DATA][location_key]) >= 1:
						order_cond_by.append("distance%d" % (i))
						if self.proptype_flag == 1:
							self.distance = 10
						having_cond_by.append("distance%d <= %d" % (i, self.distance))
					i += 1
				select = ",".join(select)
				if len(city_code) > 0:
					cond_location += " and Project_City %s (%s) " % (identify_key, ",".join(city_code))
				if len(suburb_code) > 0:
					cond_location += " and Project_Suburb %s (%s) " % (identify_key, ",".join(suburb_code))
				if len(area_code) > 0:
					cond_location += " and Project_Area %s (%s) " % (identify_key, ",".join(area_code))
				query += cond_location
				if len(self.input_data[DATA][location_key]) > 1:
					order_by = " order by least(%s) asc " % (",".join(order_cond_by))
				else:
					order_by = " order by %s asc " % (",".join(order_cond_by))
				if len(city_code) == 0 and len(suburb_code) == 0 and len(area_code) == 0:
					if len(having_cond_by) > 0:
						having = " having %s " % (" or ".join(having_cond_by))
				query += having
				self.query_process(select, query, order_by)
			if locKey == 'notIn' or locKey == 'nearBy' or locKey == 'around' or locKey == 'direction':
				for key, area in enumerate(self.input_data[DATA][location_key]):
					if locKey == 'direction':
						if self.input_data[DATA].get('locationDirection') != None:
							direction_name = self.input_data[DATA]['locationDirection']
							change_param_qty = 5
							area_lat = self.input_data[DATA][locKey+'Lat'][key]
							area_lng = self.input_data[DATA][locKey+'Long'][key]
							die_result = self.get_direction_changed(direction_name, area_lat, area_lng, change_param_qty)
							area_lat = die_result['latitude']
							area_lng = die_result['longitude']
					else:
						area_lat = self.input_data[DATA][locKey+'Lat'][key]
						area_lng = self.input_data[DATA][locKey+'Long'][key]
					get_location_find = self.find_location_code(area, area_lat, area_lng, locKey)
					if get_location_find['from_gt'] == 'City' and get_location_find.get('get_code') != None:
						city_code.extend(get_location_find['get_code'])
					elif get_location_find['from_gt'] == 'Suburb' and get_location_find.get('get_code') != None:
						suburb_code.extend(get_location_find['get_code'])
					elif get_location_find['from_gt'] == 'Area' and get_location_find.get('get_code') != None:
						area_code.extend(get_location_find['get_code'])
				if len(city_code) > 0:
					cond_location += " and Project_City %s (%s) " % (identify_key, ','.join(city_code))
				if len(suburb_code) > 0:
					cond_location += " and Project_Suburb %s (%s) " % (identify_key, ','.join(suburb_code))
				if len(area_code) > 0:
					cond_location += " and Project_Area %s (%s) " % (identify_key, ','.join(area_code))
				query += cond_location
				self.query_process(select, query, order_by)

	def query_process(self, select, where_cond, order_by):
		if not select:
			select = "distinct(project_no)"
		else:
			select = "distinct(project_no), %s" % (select)
		final_query = "select %s from all_project_info where 1=1 %s %s" % (select, where_cond, order_by)
		self.query_list.append(final_query)

	def project_info(self, project_ids):
		allConfigMinSize = 0
		allConfigMaxSize = 90000
		allConfigMinBudget = 0
		allConfigMaxBudget = 100*CRORE
		allConfigMinEMI = 0
		allConfigMaxEMI = CRORE
		self.cache_amenities()
		project_info_sql = """select a.Project_No as projectId, a.Project_Name as projectName, a.Project_City_Name as projectCity, a.Project_Area_Name as projectArea,
							 a.Possession_Text as possession, a.Developer_Name as developerName,
							 a.Area_Unit as areaUnit, a.PricePerUnit as pricePerUnit, a.P_MinPrice, 
							 GetConfigurationCombinedWithEMI(Project_No, '%s','%s',%d,%d,%d,%d,%d,%d) as ProjectConfigString,
							 IF(a.amenity_code IS NOT NULL,a.amenity_code,'') as amenityCodes,
							 a.Address as projectAddress, a.Area_Value as areaValue, a.Area_Type as areaType from all_project_info a join developer_master b
							 on a.Developer_id = b.Developer_Code where Project_No IN (%s) group by Project_No""" % (TOTAL_PROPTYPE, ",".join(BEDROOMS), allConfigMinSize, allConfigMaxSize, allConfigMinBudget, allConfigMaxBudget, allConfigMinEMI, allConfigMaxEMI, project_ids)
		self.total_project_count = NLP.cursor.execute(project_info_sql)
		if self.input_data[DATA].get('limit') != None:
			offset, limit = map(int, self.input_data[DATA]['limit'])
			project_info_results = NLP.cursor.fetchall()[offset:(offset+limit)]
		elif self.input_data[DATA].get('api_type') != None and self.input_data[DATA]['api_type'].upper() == 'NLP':
			offset, limit = 0, 20
			project_info_results = NLP.cursor.fetchall()[offset:(offset+limit)]
		else:
			project_info_results = NLP.cursor.fetchall()
		for key, project in enumerate(project_info_results):
			project_configs = project['ProjectConfigString'].split('#')
			bhks = area_types = configs = list()
			for config_key, config in enumerate(project_configs):
				bhk_str = config.split('*')[1]
				if bhk_str == ' 1RK':
					bhks.append('0.5')
				else:
					bhks.append(bhk_str[-4:])
				area_types.append(config.split('*')[4])
				configs.append(config.split('*')[0])
			if self.input_data[DATA].get(MAXBHK) != None and str(self.input_data[DATA][MAXBHK]) in BEDROOMS:
				bhk = BEDROOMS.index(str(self.input_data[DATA].get(MAXBHK)))
			else:
				bhk = BEDROOMS[0]
			project['bhk'] = bhk
			project['areaType'] = project['areaType'].replace('_', ' ')
			project['priceInWords'] = self.number_to_words(project['P_MinPrice'])
		project_ids = map(lambda r: str(r['projectId']), project_info_results)
		project_info_results = dict(zip(project_ids, project_info_results))
		images_sql = """SELECT Project_No, GROUP_CONCAT(Project_Config_No) AS Project_Config_No,
			GROUP_CONCAT(Image_type) AS Image_Type,
			GROUP_CONCAT(Image_Type_Code) AS Image_Type_Code,
			GROUP_CONCAT(Image_FileName) AS Image_FileName,
			GROUP_CONCAT(Image_Description) AS Image_Description,
			GROUP_CONCAT(Image_Order) AS Image_Order
		FROM
			(SELECT 
				Project_No, Image_type, Project_Config_No,
				CASE Image_type
					WHEN 'PROJECT_PLAN' THEN 1
					WHEN 'CONFIG_PLAN' THEN 2
					WHEN 'UNDER_CONSTRUCTION' THEN 3
					WHEN 'SITE_PLAN' THEN 4
					WHEN 'SAMPLE_FLAT' THEN 5
					WHEN 'FLOOR_PLAN' THEN 6
					WHEN 'FLOOR_PLAN_2D' THEN 7
				END AS Image_Type_Code,
				Image_FileName,	Image_Description, Image_Order
			FROM
				project_config_images
			WHERE
				Status = 'ACTIVE'
					AND Image_type IN ('CONFIG_PLAN' , 'FLOOR_PLAN', 'FLOOR_PLAN_2D', 'PROJECT_PLAN', 'UNDER_CONSTRUCTION', 'SITE_PLAN', 'SAMPLE_FLAT')) as t
		WHERE
			Project_No IN (%s)
		GROUP BY Project_No""" % (','.join(project_ids))
		NLP.cursor.execute(images_sql)
		temp_images_results = NLP.cursor.fetchall()
		images_project_no = map(lambda r: r['Project_No'], temp_images_results)
		temp_images_results = dict(zip(images_project_no, temp_images_results))
		images_results = list()
		for pid, image_result in temp_images_results.iteritems():
			image_type_code = image_result['Image_Type_Code'].split(',')
			image_type = image_result['Image_Type'].split(',')
			image_filename = image_result['Image_FileName'].split(',')
			image_description = image_result['Image_Description'].split(',')
			image_order = image_result['Image_Order'].split(',')
			project_config_nos = image_result['Project_Config_No'].split(',')
			image_type_code, image_order, image_type, image_filename, image_description, project_config_nos = map(list, zip(*sorted(zip(image_type_code, image_order, image_type, image_filename, image_description, project_config_nos), key=lambda r: r[0])))
			i = 0
			images_results = list()
			while i < len(image_type_code):
				image_dict = {'Image_Type_Code': image_type_code[i], 'Image_Type': image_type[i], 'Image_FileName': image_filename[i], 'Image_Description': image_description[i], 'Image_Order': image_order[i], 'Project_Config_No': project_config_nos[i]}
				images_results.append(image_dict)
				i += 1
			if project_info_results.get(pid) != None:
				project_info_results[pid]['images'] = self.get_config_images(images_results, pid)
		for pid, project in project_info_results.iteritems():
			displayURLHD = "/home/webuser/hdfcred.com/html/project-images1/%s/%s_%s_HD.jpg" % (pid, pid, re.sub(r"/[^A-Za-z0-9:\_-]/", '', project['projectName'].replace(' ', '_')))
			displayURL = "/home/webuser/hdfcred.com/html/project-images1/%s/%s_%s.jpg" % (pid, pid, re.sub(r"/[^A-Za-z0-9:\_-]/", '', project['projectName'].replace(' ', '_')))
			displayBannerURL = "/home/webuser/hdfcred.com/html/resale/images/user_uploaded/banners/%s/235x300.jpg" % (pid)
			if os.path.exists(displayURLHD):
				project['display_image'] = "https://www.hdfcred.com/project-images1/%s/%s_%s_HD.jpg" % (pid, pid, re.sub(r"/[^A-Za-z0-9:\_-]/", '', project['projectName'].replace(' ', '_')))
			elif os.path.exists(displayURL):
				project['display_image'] = "https://www.hdfcred.com/project-images1/%s/%s_%s.jpg" % (pid, pid, re.sub(r"/[^A-Za-z0-9:\_-]/", '', project['projectName'].replace(' ', '_')))
			elif os.path.exists(displayBannerURL):
				project['display_image'] = "https://www.hdfcred.com/resale/images/user_uploaded/banners/%s/235x300.jpg" % (pid)
			else:
				project['display_image'] = "https://www.hdfcred.com/resale/images/nophoto.png"
			project['image'] = project['display_image']
			project['amenityCodes'] = project['amenityCodes'].strip(',').split(',')
			project['url'] = self.project_overview_url(project['projectCity'], project['developerName'], project['projectName'], project['projectId'], '')+'/'
			total_config = project['ProjectConfigString'].split('#')
			project['totalConfigs'] = len(total_config)
			map(project.pop, ['display_image', 'ProjectConfigString', 'P_MinPrice'])
		return project_info_results.values()

	def cache_amenities(self):
		all_amenities_sql = "SELECT Amenity_code, Amenity_Desc, Facility_Group, Rank_1, Rank_2 FROM amenities_master"
		NLP.cursor.execute(all_amenities_sql)
		self.all_amenities = NLP.cursor.fetchall()
		amenity_codes = map(lambda r: int(r['Amenity_code']), self.all_amenities)
		self.all_amenities = dict(zip(amenity_codes, self.all_amenities))

	def find_location_code(self, location, area_lat, area_lng, locKey):
		last_search = re.sub(r"[^A-Za-z0-9]", '', location)
		get_mysql_city = self.mysql_string_replace_fn("City_Name")
		check_city = "select City_code from city_master where %s = '%s'" % (get_mysql_city, last_search)
		num_rows = NLP.cursor.execute(check_city)
		if num_rows > 0:
			city_result = NLP.cursor.fetchone()
			return {'get_code': [str(city_result['City_code'])], 'from_gt': 'City'}
		get_mysql_suburb = self.mysql_string_replace_fn("suburb_name")
		check_suburb = "select suburb_code from suburb_master where %s = '%s'" % (get_mysql_suburb, last_search)
		num_rows = NLP.cursor.execute(check_suburb)
		if num_rows > 0:
			suburb_result = NLP.cursor.fetchone()
			return {'get_code': [str(suburb_result['suburb_code'])], 'from_gt': 'Suburb'}
		get_mysql_area = self.mysql_string_replace_fn("am.Area_name")
		check_area = "select am.Area_code as Area_code from area_master am inner join suburb_master sm on sm.suburb_code=am.Suburb_Code where %s ='%s'" % (get_mysql_area, last_search)
		num_rows = NLP.cursor.execute(check_area)
		if num_rows > 0:
			area_result = NLP.cursor.fetchone()
			return {'get_code': [str(area_result['Area_code'])], 'from_gt': 'Area'}
		else:
			where = ""
			area_ids = list()
			if locKey == "in":
				return False
			if locKey != "notIn":
				if self.input_data[DATA].get(CITYID) != None:
					where = " WHERE Project_City  in (%s)" % (self.input_data[DATA][CITYID])
				project_per_area_sql = """SELECT Project_Area_Name as name, Project_Area as id, AVG(Map_Latitude) as latitude, 
										AVG(Map_Longitude) as longitude,CAST(
										IF
										(
										( 6371 * acos( cos( radians(%f) ) * 
										cos( radians( SUBSTRING(AVG(Map_Latitude),1,8) ) ) * 
										cos( radians( SUBSTRING(AVG(Map_Longitude),1,8) ) - radians(%f) ) + 
										sin( radians(%f) ) * 
										sin( radians( SUBSTRING(AVG(Map_Latitude),1,8) ) ) 
										) 
										) IS NULL, 
										'0.0',
										( 6371 * acos( cos( radians(%f) ) * 
										cos( radians( SUBSTRING(AVG(Map_Latitude),1,8) ) ) * 
										cos( radians( SUBSTRING(AVG(Map_Longitude),1,8) ) - radians(%f) ) + 
										sin( radians(%f) ) * 
										sin( radians( SUBSTRING(AVG(Map_Latitude),1,8) ) ) 
										)
										)
										)
										AS DECIMAL(10,6)
										)
										AS distance,Project_No,
										COUNT(Project_No) AS projectCount
										FROM project_master %s
										GROUP BY Project_Area 
										HAVING distance < %d order by distance
										LIMIT %d""" % (round(float(area_lat.strip()), 8), round(float(area_lng.strip()), 8), round(float(area_lat.strip()), 8), round(float(area_lat.strip()), 8), round(float(area_lng.strip()), 8), round(float(area_lat.strip()), 8), where, self.distance, self.limit)
				num_rows = NLP.cursor.execute(project_per_area_sql)
				selected_areas = NLP.cursor.fetchall()
				for area in selected_areas:
					area_ids.append(str(area['id']))
			return {'get_code': area_ids, 'from_gt': 'Area'}

	def mysql_string_replace_fn(self, column):
		mysql_string_replace = """LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(%s, ' ', ''),"'",''),'"',''),'@',''),'-',''),'_',''))""" % (column)
		return mysql_string_replace

	def area_conversion(self, area, units):
		return area*CONVERSION_UNITS[units-1]

	def convert_to_currency(self, num):
		return locale.currency(round(num, 1), grouping=True)[:-1]

	def get_direction_changed(self, direction, lat, lng, change_param_qty):
		change_param_qty *= LATLNG_TO_KM
		if direction.lower() == 'south':
			lat -= change_param_qty
		elif direction.lower() == 'east':
			lng -= change_param_qty
		elif direction.lower() == 'north':
			lat += change_param_qty
		elif direction.lower() == 'west':
			lng += change_param_qty
		return {'direction': direction, 'latitude': lat, 'longitude': lng}

	def customize_string(self, string):
		clean_string = re.sub(r"[^a-zA-Z0-9\/_|+ -]", '', string)
		clean_string = clean_string.strip('-').lower()
		clean_string = re.sub(r"[\/_|+ -]+", '-', clean_string)
		return clean_string

	def get_max_bhks(self):
		if self.input_data[DATA].get(MAXBHK) != None and str(self.input_data[DATA][MAXBHK]) in BEDROOMS:
			max_bhks = BEDROOMS[BEDROOMS.index(str(self.input_data[DATA][MAXBHK])):]
		else:
			max_bhks = BEDROOMS
		self.max_bhks_string = ','.join(max_bhks)

	def convert_to_list(self, key, value, delim=','):
		if isinstance(value, int) or isinstance(value, float):
			self.input_data[DATA][key] = value
		elif isinstance(value, str):
			value = value.strip().split(delim)
			if key in ALWAYS_LIST:
				self.input_data[DATA][key] = value
			elif len(value) == 1:
				self.input_data[DATA][key] = value[0]
			else:
				self.input_data[DATA][key] = value
		else:
			if key in ALWAYS_LIST:
				self.input_data[DATA][key] = list()
			else:
				self.input_data[DATA][key] = ""

	def project_overview_url(self, city, developer, project, pid, ref):
		return "%s/%s-%s-in-%s-p-%s%s" % (SITE_URL, self.customize_string(developer), self.customize_string(project), self.customize_string(city), pid, ref)

	def get_amenities(self, project_row):
		amenities_sql = """SELECT DISTINCT AM.Amenity_code as id, AM.Amenity_Desc as name
			FROM project_config_amenities PCA  
			LEFT JOIN amenities_master AM ON(PCA.Amenity_Code = AM.Amenity_Code) 
			WHERE PCA.Project_No = %s 
			AND PCA.Status = 'ACTIVE' 
			AND AM.Status = 'ACTIVE' 
			AND PCA.Amenity_Type = 'Common Amenities' AND AM.Amenity_Type = 'PROJECT' ORDER BY PCA.Amenity_Order""" % (project_row['projectId'])
		NLP.cursor.execute(amenities_sql)
		amenities_results = NLP.cursor.fetchall()
		return list(amenities_results)

	def number_to_words(self, num):
		if num < LAKH:
			return self.convert_to_currency(num)
		elif num >= LAKH and num < CRORE:
			if num % LAKH == 0:
				return self.convert_to_currency(num/LAKH) + " L+"
			return self.convert_to_currency(1.0*num/LAKH) + " L+"
		elif num >= CRORE:
			if num % CRORE == 0:
				return self.convert_to_currency(num/CRORE) + " Cr+"
			return self.convert_to_currency(1.0*num/CRORE) + " Cr+"

	def get_config_images(self, image_results, pid):
		image_base_path = '%s/project-images1/%d' % (DOCUMENT_ROOT, pid)
		result = list()
		for image_result in image_results:
			if image_result['Image_Type'] == 'CONFIG_PLAN':
				url_image = '%s%s/gallery/mob_%s' % (image_base_path, image_result['Project_Config_No'], image_result['Image_FileName'].replace(' ', '%20'))
				url_image_upload = '%supload/%s' % (image_base_path, image_result['Image_FileName'].replace(' ', '%20'))
				if os.path.exists(url_image):
					result.append('%s/%s/%s/gallery/mob_%s' % (FLD_PROJECTIMAGE2, pid, image_result['Project_Config_No'], image_result['Image_FileName'].replace(' ', '%20')))
				elif os.path.exists(url_image_upload):
					result.append('%s/%s/upload/%s' % (FLD_PROJECTIMAGE2, pid, image_result['Image_FileName'].replace(' ', '%20')))
			if image_result['Image_Type'] == 'PROJECT_PLAN':
				url_image = '%sgallery/mob_%s' % (image_base_path, image_result['Image_FileName'])
				url_image_upload = '%supload/%s' % (image_base_path, image_result['Image_FileName'])
				if os.path.exists(url_image):
					result.append('%s/%s/gallery/mob_%s' % (FLD_PROJECTIMAGE2, pid, image_result['Image_FileName']))
				elif os.path.exists(url_image_upload):
					result.append('%s/%s/upload/%s' % (FLD_PROJECTIMAGE2, pid, image_result['Image_FileName']))
			if image_result['Image_Type'] == 'UNDER_CONSTRUCTION':
				url_image = '%sgallery/mob_%s' % (image_base_path, image_result['Image_FileName'])
				url_image_upload = '%supload/%s' % (image_base_path, image_result['Image_FileName'])
				if os.path.exists(url_image):
					result.append('%s/%s/gallery/mob_%s' % (FLD_PROJECTIMAGE2, pid, image_result['Image_FileName']))
				elif os.path.exists(url_image_upload):
					result.append('%s/%s/upload/%s' % (FLD_PROJECTIMAGE2, pid, image_result['Image_FileName']))
			if image_result['Image_Type'] == 'SITE_PLAN':
				url_image = '%slayout/mob_%s' % (image_base_path, image_result['Image_FileName'])
				url_image_upload = '%supload/%s' % (image_base_path, image_result['Image_FileName'])
				if os.path.exists(url_image):
					result.append('%s/%s/layout/mob_%s' % (FLD_PROJECTIMAGE2, pid, image_result['Image_FileName']))
				elif os.path.exists(url_image_upload):
					result.append('%s/%s/upload/%s' % (FLD_PROJECTIMAGE2, pid, image_result['Image_FileName']))
			if image_result['Image_Type'] == 'SAMPLE_FLAT':
				url_image = '%s%s/sample/mob_%s' % (image_base_path, image_result['Project_Config_No'], image_result['Image_FileName'])
				url_image_upload = '%supload/%s' % (image_base_path, image_result['Image_FileName'])
				if os.path.exists(url_image):
					result.append('%s/%s/%s/sample/mob_%s' % (FLD_PROJECTIMAGE2, pid, image_result['Project_Config_No'], image_result['Image_FileName']))
				elif os.path.exists(url_image_upload):
					result.append('%s/%s/upload/%s' % (FLD_PROJECTIMAGE2, pid, image_result['Image_FileName']))
			if image_result['Image_Type']  in ['FLOOR_PLAN', 'FLOOR_PLAN_2D', 'FLOOR_PLAN_3D']:
				url_image = '%s%s/floorplan/mob_%s' % (image_base_path, image_result['Project_Config_No'], image_result['Image_FileName'])
				url_image_upload = '%supload/%s' % (image_base_path, image_result['Image_FileName'])
				if os.path.exists(url_image):
					result.append('%s/%s/%s/floorplan/mob_%s' % (FLD_PROJECTIMAGE2, pid, image_result['Project_Config_No'], image_result['Image_FileName']))
				elif os.path.exists(url_image_upload):
					result.append('%s/%s/upload/%s' % (FLD_PROJECTIMAGE2, pid, image_result['Image_FileName']))


def main():
	nlp = NLP(LocKeyword = 'in', inLocation = 'Andheri', inLat =  '19.1148921698148370000', inLong = '72.8738831180171600000', propType = 'APARTMENT', maxBHK = 2, city_id = 1, api_type = 'nlp', limit = '0,20')
	print nlp.get()

if __name__ == '__main__':
	main()
