import os
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from get_site_row_col import get_dset
import numpy as np
import cartopy.io.shapereader as shpreader
from datetime import datetime
import cartopy.feature as cf
import matplotlib as mpl
import xarray as xr

def get_extent(wrfPath,wrfCtlFile):
	'''purpose:获取绘图的经纬度坐标顶点'''
	xlong = np.array(get_dset(wrfPath,wrfCtlFile).get('XLONG')[0,:,:])
	xlat = np.array(get_dset(wrfPath,wrfCtlFile).get('XLAT')[0,:,:])
	lonMin = np.min(xlong).tolist()
	lonMax = np.max(xlong).tolist()
	latMin = np.min(xlat).tolist()
	latMax = np.max(xlat).tolist()
	extent = [lonMin,lonMax,latMin,latMax]
	return extent

def dask_array2xarray(dset,speName,extent):
	'''purpose:daskarry2xarry'''
	ds = xr.Dataset()
	data = dset[speName]
	dims = data.dims
	ds['time'] = data['time']
	ds['lev'] = data['lev']
	ds['lat'] = np.linspace(extent[2],extent[3],360)
	ds['lon'] = np.linspace(extent[0],extent[1],240)
	ds[speName] = xr.DataArray(np.array(data),dims=dims)
	return ds


def plot_dset(extent,dset,speName,shpFile,outPath):
	'''purpose:数据画图'''
	# 使用Mercator，圆柱形投影。 
	projection = ccrs.Mercator()
	# 坐标投影CRS。
	crs = ccrs.PlateCarree()
	# 创建具有特定投影的轴对象。 
	plt.figure(dpi=150)
	ax = plt.axes(projection=projection, frameon=True)

	# 增加城市地图
	city = shpreader.Reader(shpFile).geometries()
	ax.add_geometries(city,crs,facecolor = 'none',edgecolor = 'k',linewidth = 1,zorder=1)
	# 在Mercator地图上以度绘制网格线。
	gl = ax.gridlines(crs=crs, draw_labels=True,
	                  linewidth=.6, color='gray', alpha=0.5, linestyle='-.')
	gl.xlabel_style = {"size" : 7}
	gl.ylabel_style = {"size" : 7}
	# 绘制边界和海岸线，使用cartopy功能。
	ax.add_feature(cf.COASTLINE.with_scale("50m"), lw=0.5)
	ax.add_feature(cf.BORDERS.with_scale("50m"), lw=0.3)
	# ax.add_feature(cf.OCEAN.with_scale('50m'))
	# ax.add_feature(cf.LAND.with_scale('50m'))
	dtime = np.array(dset[speName].time)[0]
	dtime = np.datetime_as_string(dtime, unit='h')
	comment = list(filter(None,dset[speName].comment.split(" ")))
	vmin = np.min(np.array(dset[speName][0,0]))
	vmax = np.max(np.array(dset[speName][0,0]))
	cmap = mpl.cm.jet
	cbar_kwargs = {'orientation':'vertical', 'shrink':0.9, "pad" : .1, 'aspect':40, 'label':'{}({}) '.format(*comment)}
	darray = dask_array2xarray(dset,speName,extent)
	print(np.array(darray[speName]).shape)
	darray[speName][0,0].plot.contourf(ax=ax, transform=ccrs.PlateCarree(), cbar_kwargs=cbar_kwargs, levels=100,cmap=cmap,vmin=vmin,vmax=vmax)
	# crs是PlateCarree -- 我们明确地告诉轴，我们正在创建以度为单位的边界。
	ax.set_extent(extent, crs=crs)
	plt.title(dtime)
	plt.show()
	# plt.savefig(outPath+'/'+dtime+speName+'.png')
	# plt.close()

def main(gridPath,gridCtlFile,wrfPath,wrfCtlFile,outPath,speName,shpFile):
	'''purpose:绘制污染物空间分布主程序'''
	if not os.path.exists(outPath):
		os.makedirs(outPath)
	extent = get_extent(wrfPath,wrfCtlFile)
	dset = get_dset(gridPath,gridCtlFile)
	plot_dset(extent,dset,speName,shpFile,outPath)

if __name__ == '__main__':
	gridPath = r'C:\Users\schao\Downloads\NAQ数据处理\data'
	gridCtlFile = 'testd2.2019092504.ctl'
	wrfPath = r'C:\Users\schao\Downloads\datagrid'
	wrfCtlFile = 'grid.d2.ctl'
	outPath = r'D:\jobs\read_grd\plot'
	speName = 'no2'
	shpFile = r'D:\jobs\聚光科技\谱育科技\202305\read_grd\shp\bou2_4m\bou2_4l.shp'
	main(gridPath,gridCtlFile,wrfPath,wrfCtlFile,outPath,speName,shpFile)