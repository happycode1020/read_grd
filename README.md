# read_grd 使用说明
## 安装xgrads库，用于解析grd文件
1. cd xgrads-master/xgrads-master/
2. python setup.py install
3. 另外需要配置的库：cartopy  **pip install cartopy**

## 各个文件说明及使用
### get_site_row_col.py:基于经纬度文件获取站点在模拟区域的行列位置，并生成csv文件
**需要配置的参数如下：**
1.  dataPath = r'C:\Users\schao\Downloads\datagrid' # wrf文件的路径
	ctlFile = 'grid.d2.ctl' # wrf的ctl文件
	latlonFile = 'C:/Users/schao/Downloads/NAQ数据处理/2020站点经纬度.csv' # 初始经纬度文件路径，可进行修改
	fileName = '输出数据1' # 输出文件名称，可进行修改
2. 执行python get_site_row_col.py 

### get_site_pol.py:基于脚本一生成的csv文件，获取站点的污染结果，并输出csv文件
**需要配置的参数如下：**
1. begTime = '2019092419'  # 写出结果的开始时间
	endTime = '2019092608' # 写出结果的结束时间
	dataPath = r'C:\Users\schao\Downloads\NAQ数据处理\data' # grd文件路径
	latlonFile = r'C:\Users\schao\Downloads\datagrid\输出数据1.csv' # 脚本1生成的文件
	speList = ['PM25','so2','no2'] # 要获取的物种，需要和ctl文件中的物种名一致
	fileName = '输出数据2' # 输出文件名，可以修改
	fileStype = 'testd2.{}.ctl' # grd文件样式，其中{}代替时间
2. 执行 python get_site_pol.py 

### plot_dset.py:污染物空间分布绘制脚本
**需要配置的参数如下：**
1. gridPath = r'C:\Users\schao\Downloads\NAQ数据处理\data' # grd文件路径
	gridCtlFile = 'testd2.2019092504.ctl' # 需要绘制的grd ctl文件
	wrfPath = r'C:\Users\schao\Downloads\datagrid' # wrf文件路径
	wrfCtlFile = 'grid.d2.ctl' # wrf同区域的ctl文件
	outPath = './plot' # 画图输出路径
	speName = 'PM25' # 绘制物种名
	shpFile = r'D:\jobs\聚光科技\谱育科技\202305\read_grd\shp\bou2_4m\bou2_4l.shp' # 地图文件
2. 执行 python plot_dset.py

