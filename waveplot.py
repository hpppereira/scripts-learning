'''
Plot wave parameters fields and points
'''

def wavefield():

	# In[181]:

	# Plot the field using Basemap.  Start with setting the map
	# projection using the limits of the lat/lon data itself:

	plt.figure(figsize=(16,14))

	m=Basemap(projection='mill',lat_ts=10,llcrnrlon=lon.min(),   urcrnrlon=lon.max(),llcrnrlat=lat.min(),urcrnrlat=lat.max(),   resolution='c')

	# convert the lat/lon values to x/y projections.

	lons, lats = np.meshgrid(lon,lat)
	# x, y = lons, lats
	x, y = m(*np.meshgrid(lon,lat))

	# plot the field using the fast pcolormesh routine 
	# set the colormap to jet.

	m.pcolormesh(x,y,data_hs,shading='flat',cmap=plt.cm.jet)
	m.colorbar(location='right')

	# Add a coastline and axis values.

	m.drawcoastlines()
	m.fillcontinents()
	m.drawmapboundary()
	m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
	m.drawmeridians(np.arange(-180.,180.,60.),labels=[0,0,0,1])

	# Add a colorbar and title, and then show the plot.

	plt.title('NWW3 Significant Wave Height from NOMADS')
	plt.show()


