import os,csv
from xgrads import CtlDescriptor
from xgrads import open_CtlDataset
import numpy as np

def get_dset(dataPath,ctlFile):
	'''purpose:获取变量'''
	os.chdir(dataPath)
	ctl = CtlDescriptor(file=ctlFile)
	dset = open_CtlDataset(ctlFile)

	return dset

def get_lat_lon(latlonFile):
	'''purpose:获取站点的经纬度数据'''
	latlon = {}
	with open(latlonFile,'r') as ll:
		lines = ll.readlines()
		for l in lines[1:]:
			line = l.strip()
			cols = line.split(',')
			latlon[cols[0]] = cols[:]

	return latlon

def get_row_col(lat,lon,wrfCtlFile,dataPath):
	'''purpose:基于wrf的经纬度网格，获取目标点位在网格的位置'''
	xlong = get_dset(dataPath,wrfCtlFile).get('XLONG')[0,:,:]
	xlat = get_dset(dataPath,wrfCtlFile).get('XLAT')[0,:,:]
	shape = xlong.shape
	modelGrid = list( zip(np.ravel(xlong), np.ravel(xlat)) ) 
	neardis = [np.sqrt((lon-s[0])**2+(lat-s[1])**2) for s in modelGrid]
	neardisarray = np.array(neardis).reshape(shape)
	pos = np.where(neardisarray==np.min(neardisarray))
	row,col = pos[0][0],pos[1][0]

	return row,col

def write_csv(dictData,headName,outPath,fileName):
	'''purpose:字典数据写出到csv文件'''
	with open(outPath+'/'+fileName+'.csv','w',newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(headName)
		for k,v in dictData.items():
			writer.writerow(v)

def write_site_row_col(latlonFile,ctlFile,dataPath,fileName):
	'''purpose:获得所有站点的行列及写出'''
	headName = ['Station','区域','站点','经度','纬度','Row','Col']
	latlon = get_lat_lon(latlonFile)
	newDict = {}
	for k in latlon.keys():
		print('>>>>%s'%k)
		col = latlon.get(k)
		lat,lon = float(col[-1]),float(col[-2])
		sRow,sCol = get_row_col(lat,lon,ctlFile,dataPath)
		col.append(sRow)
		col.append(sCol)
		newDict[k] = col
	write_csv(newDict,headName,dataPath,fileName)

if __name__ == '__main__':
	dataPath = r'C:\Users\schao\Downloads\datagrid'
	ctlFile = 'grid.d2.ctl'
	latlonFile = 'C:/Users/schao/Downloads/NAQ数据处理/2020站点经纬度.csv'
	fileName = '输出数据1'
	write_site_row_col(latlonFile,ctlFile,dataPath,fileName)


