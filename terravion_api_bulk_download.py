################################################################################
# TerrAvion Bulk Download Sample
#
# This material contains sample programming source code ("Sample Code").
# TerrAvion grants you a nonexclusive license to compile, link, run,
# prepare derivative works of this Sample Code.  The Sample Code has not
# been thoroughly tested under all conditions.  TerrAvion, therefore, does
# not guarantee or imply its reliability, serviceability, or function. 
#
# All Sample Code contained herein is provided to you "AS IS" without
# any warranties of any kind. THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGMENT ARE EXPRESSLY
# DISCLAIMED.  SOME JURISDICTIONS DO NOT ALLOW THE EXCLUSION OF IMPLIED
# WARRANTIES, SO THE ABOVE EXCLUSIONS MAY NOT APPLY TO YOU.  IN NO 
# EVENT WILL TERRAVION BE LIABLE TO ANY PARTY FOR ANY DIRECT, INDIRECT, 
# SPECIAL OR OTHER CONSEQUENTIAL DAMAGES FOR ANY USE OF THE SAMPLE CODE
# INCLUDING, WITHOUT LIMITATION, ANY LOST PROFITS, BUSINESS 
# INTERRUPTION, LOSS OF PROGRAMS OR OTHER DATA ON YOUR INFORMATION
# HANDLING SYSTEM OR OTHERWISE, EVEN IF WE ARE EXPRESSLY ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGES.
#
# COPYRIGHT
# ---------
# (C) Copyright TerrAvion Inc. 2016
# All rights reserved.
#
#
# AUTHOR
# ------
# William Maio
# wmaio@terravion.com
# http://www.terravion.com
#
################################################################################

import os, sys,base64,argparse
from os.path import basename
from urllib2 import Request, urlopen, URLError, HTTPError
import datetime
import time
from datetime import datetime
from time import mktime
import json

# Contact wmaio@terravion.com for access_token
# Access_token 
# Pleaese modify the product_name to download the perspective product
'''
	NC => RGB
	CIR => Color Infrared
	NDVI => NDVI
	TIRS => Thermal 
	ZONE => Zoning 
'''

'''
	NDVI Color Map Options: 

	N-R3 => TerrAvion Default - This scale is based on the Historic TerrAvion color pallet and is very tightly focused on the range most relevant to variation in vines and similar crops.
	N-R2 => TerrAvion Wide Range - This pallet uses the same colors as the TerrAvion Default scale, but the range of variation is larger, it may be of use when looking at changes over a very long time as it will call out seasonal changes in bigger color blocks.
	N-AVHR => AVHRR Scale - Based on the scle of the NASA Earth imaging mission, this scale is a finely graded to categorize variation into many different gradations.
	Green Gradient - A continuous scale from black to bright green, this scale show the data in a monochrome scale which does not bin any pixel.  Each pixel value is a unique color brightness.  This scale may make categorization hard, but you can see the full sensitivity of the NDVI.
	N => TerrAvion Historic - This is the pallet we provided at the beginning of the season, it is provided for comparison and continuity purposes.  It is useful in looking at extreme changes in vigor.
'''
# Creating the folder if it does not exist 
def main(argv):
	argument_sample='python '+basename(os.path.realpath(__file__))+' -working_dir <working_dir> -year_week <year_week> -product_name <product_name> -access_token <access_token> -product_name <product_name>'
	parser = argparse.ArgumentParser(description=argument_sample)
	parser.add_argument('-working_dir',help="working_dir",nargs='?',default=None)
	parser.add_argument('-year_week',help='year_week get leayrs in given year_week',nargs='?',default=None)
	parser.add_argument('-username',help='username',nargs='?',default=None)
	parser.add_argument('-access_token',help='access_token',nargs='?',default=None)
	parser.add_argument('-product_name',help='product_name NC,CIR,NDVI,ZONE,TIRS,MULTIBAND',nargs='?',default=None)
	parser.add_argument('-color_map',help='color_map N-AVHRR N-R3 N-R2 N-GREENG',nargs='?',default='N-AVHRR')

	args = parser.parse_args()
	working_dir=args.working_dir
	year_week=args.year_week
	username=args.username
	product_name=args.product_name
	access_token=args.access_token
	color_map=args.color_map

	if not (username and access_token):
		print 'Pleaese include -username -access_token -working_dir'
		print 'email William Maio at wmaio@terravion.com if you need one'
		print parser.print_help()
		return 0
	if not year_week:
		print '--------------------------------------------------------------------------------------------------------------------------------'
		block_dic_struct=get_block_list_with_id(username,access_token)
		if not product_name:
			product_name='NDVI'
		layer_list=get_all_layers_list(block_dic_struct,product_name,username,access_token)

		# organize layers by week: 
		week_year_dic={}
		for layer in layer_list:
			date_object=datetime.strptime(layer['layerdate'], "%Y-%m-%dT%H:%M:%S.%fZ")
			week_year_index=str(date_object.isocalendar()[0])+'_'+"%02d" %date_object.isocalendar()[1]
			if not week_year_index in week_year_dic:
				week_dic={}
			else: 
				week_dic=week_year_dic[week_year_index]
			week_dic[layer['block_id']]=layer
			week_year_dic[week_year_index]=week_dic
		for week_year_index in sorted(week_year_dic.keys()):
			ranch_list=[]
			for block_id in week_year_dic[week_year_index]:
				ranch_name=week_year_dic[week_year_index][block_id]['block_name'].split('/')[0]
				if not ranch_name in ranch_list:
					ranch_list.append(ranch_name)
			print week_year_index, datetime.strptime(week_year_index + '-0', "%Y_%W-%w").strftime('%Y-%m-%d'),sorted(ranch_list)

		print '--------------------------------------------------------------------------------------------------------------------------------'
		print parser.print_help()
		print '--------------------------------------------------------------------------------------------------------------------------------'
	elif not working_dir:
		print 'pleaese include -working_dir'
		print '--------------------------------------------------------------------------------------------------------------------------------'
		print parser.print_help()
		print '--------------------------------------------------------------------------------------------------------------------------------'
	elif not product_name or product_name not in ['NC','CIR','NDVI','ZONE','TIRS','MULTIBAND']:
		print 'pleaese include valid -product_name [NC,CIR,NDVI,ZONE,TIRS,MULTIBAND]' 
		print '--------------------------------------------------------------------------------------------------------------------------------'
		print parser.print_help()
		print '--------------------------------------------------------------------------------------------------------------------------------'
	elif product_name:
		print 'download imagery',year_week 
		if not os.path.exists(working_dir):
		    os.makedirs(working_dir)
		block_dic_struct=get_block_list_with_id(username,access_token)
		layer_list=get_all_layers_list(block_dic_struct,product_name,username,access_token)
		# organize layers by week: 
		week_year_dic={}
		for layer in layer_list:
			date_object=datetime.strptime(layer['layerdate'], "%Y-%m-%dT%H:%M:%S.%fZ")
			week_year_index=str(date_object.isocalendar()[0])+'_'+"%02d" %date_object.isocalendar()[1]
			if not week_year_index in week_year_dic:
				week_dic={}
			else: 
				week_dic=week_year_dic[week_year_index]
			week_dic[layer['block_id']]=layer
			week_year_dic[week_year_index]=week_dic
		if year_week in week_year_dic.keys():
			week_year_index=year_week
			include_block_id_flag=check_duplicate_block_name(week_year_dic[week_year_index])
			for block_id in week_year_dic[week_year_index]:
				print 'downloading',week_year_dic[week_year_index][block_id]['block_name'], datetime.strptime(week_year_dic[week_year_index][block_id]['layerdate'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%Y-%m-%d')
				get_geotiff(week_year_dic[week_year_index][block_id],product_name,color_map,username,access_token,working_dir,include_block_id_flag)
		else:
			print 'invalid week_year',week_year_index
	else: 
		print '--------------------------------------------------------------------------------------------------------------------------------'
		print parser.print_help()
		print '--------------------------------------------------------------------------------------------------------------------------------'
def check_duplicate_block_name(block_dic):
	block_name_list=[]
	block_id_list=[]
	for block_id in block_dic:
		block_name_list.append(block_dic[block_id]['block_name'])
		block_id_list.append(block_id)
	if len(tuple(set(block_name_list)))==len(tuple(set(block_id_list))):
		return True
	else: 
		return None
def get_all_layers_list(block_dic_struct,product_name,username,access_token):
	if product_name=='MULTIBAND':
		product_name='NDVI'
	request_url='https://api.terravion.com/v1/users/'+username+'/layers?product='+product_name+'&access_token='+access_token
	print request_url
	request = Request(request_url)
	response_body = urlopen(request).read()
	layer_list_json=json.loads(response_body)
	# Organize the layer_id with block_name 
	layer_list=[]
	for layer_info in layer_list_json:
		layer_struct={}
		layer_struct['id']=layer_info['id']
		layer_struct['layerdate']=layer_info['layerDate']
		layer_struct['product']=layer_info['product']
		layer_struct['block_id']=layer_info['block']['id']
		layer_struct['block_name']=block_dic_struct[layer_info['block']['id']]['block_name']
		layer_list.append(layer_struct)
	return layer_list

def get_layer_list(block_dic_struct):
	# Get the layer list of the users between the time period of start_date and end_date and organize the layers by the block_name 

	request_url='https://api.terravion.com/v1/users/'+username+'/layers?epochStart='+str(start_date_epoc)+'&epochEnd='+str(end_date_epoc)+'&product='+product_name+'&access_token='+access_token
	print request_url
	request = Request(request_url)
	response_body = urlopen(request).read()
	layer_list_json=json.loads(response_body)
	# Organize the layer_id with block_name 
	layer_list=[]
	for layer_info in layer_list_json:
		print layer_info
		layer_struct={}
		layer_struct['id']=layer_info['id']
		layer_struct['layerdate']=layer_info['layerDate']
		layer_struct['product']=layer_info['product']
		layer_struct['block_id']=layer_info['block']['id']
		layer_struct['block_name']=block_dic_struct[layer_info['block']['id']]['block_name']
		layer_list.append(layer_struct)
	return layer_list
def get_user_colormap(username,access_token):
	request_url='https://api.terravion.com/v1/users/'+username+'/?access_token='+access_token
	request = Request(request_url)
	response_body = urlopen(request).read()
	user_info=json.loads(response_body)
	return user_info
def get_geotiff(layer_info,product_name,color_map,username,access_token,working_dir,include_block_id_flag):
	# Download the product specified by the product and colormap to the working directory 
	#http://docs.terravionv1.apiary.io/#reference/layers/usersuseridoremaillayerstileszxypngcolormapepochstartepochendproduct
	#print layer_info
	layer_id=layer_info['id']
	date_object=datetime.strptime(layer_info['layerdate'], "%Y-%m-%dT%H:%M:%S.%fZ")
	if include_block_id_flag:
		out_file_name=os.path.join(working_dir,date_object.strftime('%Y-%m-%d_%H%M-%S')+'_'+layer_info['block_name'].replace('/','-')+'_'+layer_info['block_id']+'_'+product_name+'.tiff')		
	else: 
		out_file_name=os.path.join(working_dir,date_object.strftime('%Y-%m-%d_%H%M-%S')+'_'+layer_info['block_name'].replace('/','-')+'_'+product_name+'.tiff')
	if product_name=='MULTIBAND':
		request_url='https://api.terravion.com/v1/layers/'+layer_id+'/geotiffs/multiband.tiff'+'?access_token='+access_token
		request = Request(request_url)
	elif 'NC'==layer_info['product'] or 'CIR'==layer_info['product']:
		request_url='https://api.terravion.com/v1/layers/'+layer_id+'/geotiffs/image.tiff?colorMap=null'+'&access_token='+access_token
		request = Request(request_url)
	elif 'TIRS' ==layer_info['product']:
		request_url='https://api.terravion.com/v1/layers/'+layer_id+'/geotiffs/image.tiff?colorMap=T'+'&access_token='+access_token
		request = Request(request_url)
	elif 'NDVI' ==layer_info['product'] or 'ZONE' ==layer_info['product']:
		request_url='https://api.terravion.com/v1/layers/'+layer_id+'/geotiffs/image.tiff?colorMap='+color_map+'&access_token='+access_token
		request = Request(request_url)
	print request_url
	response_file = urlopen(request)

	try:
		print 'writing',out_file_name
		with open(out_file_name, "wb") as local_file:
			local_file.write(response_file.read())
	except HTTPError, e:
		#handle errors
		print "HTTP Error:", e.code, url
	except URLError, e:
		print "URL Error:", e.reason, url
	return out_file_name

def get_block_list_with_id(username,access_token):
	# Getting the list of blocks owned by the user

	# http://docs.terravionv1.apiary.io/#reference/users/user-blocks-collection/retrieve-blocks-user-has-access-to
	request_url='https://api.terravion.com/v1/users/'+username+'/blocks'+'?access_token='+access_token
	print request_url
	request = Request(request_url)
	response_body = urlopen(request).read()
	#print response_body
	block_list_json=json.loads(response_body)
	block_dic_struct={}
	for block_info in block_list_json:
		block_struct={}
		block_struct['block_name']=str(block_info['block']['name'].encode("ascii", "ignore").encode("utf-8"))
		block_struct['block_id']=str(block_info['block']['id'])
		block_dic_struct[block_struct['block_id']]=block_struct
	return block_dic_struct
def get_mulitband_geotiff(layer_info,working_dir):
	# Download the multiband 16 bit image to the working directory 

	# http://docs.terravionv1.apiary.io/#reference/layers/usersuseridoremaillayersepochstartepochendproduct
	layer_id=layer_info['id']
	date_object=datetime.strptime(layer_info['layerdate'], "%Y-%m-%dT%H:%M:%S.%fZ")
	out_file_name=os.path.join(working_dir,date_object.strftime('%Y-%m-%d_%H%M-%S')+'_'+layer_info['block_name'].replace('/','-')+'_fiveband.tiff')
	request = Request('https://api.terravion.com/v1/layers/'+layer_id+'/geotiffs/multiband.tiff'+'?access_token='+access_token)
	response_file = urlopen(request)
	try:
		with open(out_file_name, "wb") as local_file:
			local_file.write(response_file.read())
	except HTTPError, e:
		#handle errors
		print "HTTP Error:", e.code, url
	except URLError, e:
		print "URL Error:", e.reason, url
	return out_file_name

if __name__ == '__main__':
	main(sys.argv[1:])