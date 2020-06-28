using PyPlot, PyCall
pygui(true)

ccrs = pyimport("cartopy.crs")
cfeature = pyimport("cartopy.feature")


subplots()
ax = subplot(projection=ccrs.PlateCarree())
ax.coastlines(resolution="50m", color="k", linewidth=1)
ax.set_xticks(collect(-180:60:180), crs=ccrs.PlateCarree())
ax.set_yticks(collect(-90:30:90), crs=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE)
# ax.add_feature(cfeature.LAND)
# ax.add_feature(cfeature.RIVERS)
# ax.add_feature(cfeature.LAKES, alpha=0.5)
# ax.stock_img()
# title("hi")
xlabel("Longitude", labelpad=10)
ylabel("Latitude", labelpad=10)