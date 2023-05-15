from get_site_row_col import get_dset,get_lat_lon
from datetime import datetime,timedelta
import numpy as np
import csv

def convert_time(thisTime):
	'''purpose:获得本地时间和utc时间'''
	utcTime = datetime.strptime(thisTime,'%Y%m%d%H')
	localTime = (utcTime+timedelta(hours=8))
	localTime2 = localTime.strftime('%Y-%m-%d %H:00')

	return utcTime.strftime('%Y-%m-%d %H:00'),localTime2

def get_site_pol(dataPath,latlonFile,ctlFile,speList):
	'''purpose:获取站点的污染物模拟结果'''
	latlon = get_lat_lon(latlonFile)
	dataSet = get_dset(dataPath,ctlFile)
	keys = list(dataSet.keys())
	sitePol = {}
	thisTime = ctlFile.split('.')[-2]
	utcTime,localTime = convert_time(thisTime)
	for k in latlon.keys():
		# print('>>>>%s'%k)
		colPos = latlon.get(k)
		colPos.append(utcTime)
		colPos.append(localTime)
		for varName in speList:
			dataArray = dataSet.get(varName)
			row,col = int(colPos[5]),int(colPos[6])
			value = np.array(dataArray[0,0,row,col]).tolist()
			colPos.append(value)
		sitePol[k] = colPos

	return sitePol

def write_csv(dictData,headName,outPath,fileName):
	'''purpose:字典数据写出到csv文件'''
	with open(outPath+'/'+fileName+'.csv','w',newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(headName)
		for k,v in dictData.items():
			for k,v in v.items():
				writer.writerow(v)

def write_all_time(begTime,endTime,dataPath,latlonFile,speList,fileStype):
	'''purpose:获取所有时刻的污染数据'''
	headName = ['Station','区域','站点','经度','纬度','Row','Col','UTCTime','localTime']
	headName.extend(speList)
	startTime = datetime.strptime(begTime,'%Y%m%d%H')
	endTime2 = datetime.strptime(endTime,'%Y%m%d%H')
	allData = {}
	while startTime <= endTime2:
		thisTime = startTime.strftime('%Y%m%d%H')
		print('>>>>%s'%thisTime)
		ctlFile = fileStype.format(thisTime)
		sitePol = get_site_pol(dataPath,latlonFile,ctlFile,speList)
		allData[thisTime] = sitePol
		startTime += timedelta(hours=1)
	write_csv(allData,headName,dataPath,fileName)

if __name__ == '__main__':
	begTime = '2019092419'
	endTime = '2019092608'
	dataPath = r'C:\Users\schao\Downloads\NAQ数据处理\data'
	latlonFile = r'C:\Users\schao\Downloads\datagrid\输出数据1.csv'
	speList = ['PM25','so2','no2']
	fileName = '输出数据2'
	fileStype = 'testd2.{}.ctl'
	write_all_time(begTime,endTime,dataPath,latlonFile,speList,fileStype)



