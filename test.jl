using NetCDF
using Statistics
using PyPlot, PyCall
using Distributed
using DataFrames
using CSV
using Dates
ccrs = pyimport("cartopy.crs")
cfeature = pyimport("cartopy.feature")

Floder = "D:\\space physic\\FORMOSAT3\\2007"

csv_flodler_2007 = "D:\\space physic\\FORMOSAT3\\csv_2007"
csv_flodler_2008 = "D:\\space physic\\FORMOSAT3\\csv_2008"

spring = collect(36:127)
summer = collect(128:219)
autumn = collect(220:311)
winter = vcat(collect(311:365),collect(1:34))

each_month = collect.(
    [1:31,
    32:59,
    60:90,
    91:120,
    121:151,
    152:181,
    182:212,
    183:243,
    244:273,
    274:304,
    305:334,
    335:365]
    )

Δx = 5
Δy = 2.5

lon = collect(-180:Δx:180)
lat = collect(-90:Δy:90)


X, Y = repeat(lon', length(lat), 1), repeat(lat, 1, length(lon))

lon_len = length(lon)
lat_len = length(lat)

lon_boundary = range(-180,180,length=lon_len+1)
lat_boundary = range(-90,90,length=lat_len+1)

global pre_z = []
for i = 1:lon_len
    this = []
    for j = 1:lat_len
        append!(this,[[]])
    end
    append!(pre_z,[this])
end #end for

global z = Array{Float64,2}(undef,lon_len,lat_len)

function __init__()
    pre_z = []
    for i = 1:lon_len
        this = []
        for j = 1:lat_len
            append!(this,[[]])
        end
        append!(pre_z,[this])
    end #end for
    z = Array{Float64,2}(undef,lon_len,lat_len)
end

function find_all(arr)
    cd(Floder)
    file_day = readdir()
    for day in file_day[arr]
        cd(string(Floder,"\\",day))
        file = readdir()
        @distributed for each in file
            alt = ncread(each,"MSL_alt")
            conde = findall(x->x>295&&x<305,alt)
            geo_lo= ncread(each,"GEO_lon")[conde]
            geo_la= ncread(each,"GEO_lat")[conde]
            ele= ncread(each,"ELEC_dens")[conde]
            add_in_lattice(geo_lo,geo_la,ele)
        end # end for
        println(day)
    end # end for
end

function find_all_csv(arr,csv_flodler)   
    cd(csv_flodler)
    file_day = readdir()
    for day in file_day[arr]
        println(day)
        df = CSV.read(day)
        alt = df.MSL_alt
        conde = findall(x->x>=250&&x<=400,alt)
        time_ = df.time[conde]
        geo_lo = df.GEO_lon[conde]
        geo_la = df.GEO_lat[conde]
        ele = df.ELEC_dens[conde]
        for (on,at,n,t) in zip(geo_lo,geo_la,ele,time_)
            h = Dates.hour(t + Dates.Hour(ceil(on/15)))
            if (h in [0,1,2,3,4,5,6,7])
                x_index = findall(x->x<=on,lon_boundary)[end]
                y_index = findall(x->x<=at,lat_boundary)[end]
                append!(pre_z[x_index][y_index],n)
            end
        end #end for
    end # end for
    #title(csv_flodler[end-3:end])
end


function alt_change(arr,csv_flodler,alt_down,alt_up)   
    cd(csv_flodler)
    file_day = readdir()
    for day in file_day[arr]
        println(day)
        df = CSV.read(day)
        alt = df.MSL_alt
        conde = findall(x->x>=alt_down&&x<=alt_up,alt)
        
        time_ = df.time[conde]
        geo_lo = df.GEO_lon[conde]
        geo_la = df.GEO_lat[conde]
        ele = df.ELEC_dens[conde]
        for (on,at,n,t) in zip(geo_lo,geo_la,ele,time_)
            h = Dates.hour(t + Dates.Hour(ceil(on/15)))
            if (h in [22,23,0,1,2])
                x_index = findall(x->x<=on,lon_boundary)[end]
                y_index = findall(x->x<=at,lat_boundary)[end]
                append!(pre_z[x_index][y_index],n)
            end
        end #end for
    end # end for
    #title("$(csv_flodler[end-3:end]) $alt_down ~ $alt_up")
end

function plot_ion(ttt="2007")
    for i = 1:lon_len
        for j = 1:lat_len
                out = []
                for i_a = i-2:i+2
                    for j_a  = j-2:j+2
                        if ((j_a>0) && (j_a<=lat_len))
                            if (i_a<=0)
                                i_a = lon_len + i_a
                            end
                            if (i_a>lon_len)
                                i_a = -lon_len + i_a
                            end
                            if (pre_z[i_a][j_a]!=[])
                                append!(out,pre_z[i_a][j_a])
                            end
                        end
                    end
                end
                if (out!=[])
                    z[i,j] = median(out)
                else
                    z[i,j] = 0
                end           
        end
    end
    pygui(true)
    figure(figsize=(10,5))
    ax = subplot(projection=ccrs.PlateCarree())
    ax.coastlines(resolution="50m", color="k", linewidth=1)
    ax.set_xticks(collect(-180:60:180), crs=ccrs.PlateCarree())
    ax.set_yticks(collect(-75:15:75), crs=ccrs.PlateCarree())
    #ax.stock_img()
    color_max = maximum(z)
    ax.add_feature(cfeature.COASTLINE)
    X, Y = repeat(lon', length(lat), 1), repeat(lat, 1, length(lon))
    clev = range(0,step=color_max/1000,color_max)
    ticks = range(0,length = 5,color_max)
    contourf(X,Y,z',clev,cmap="jet")#,vmin =maximum(z)*0.5 )
    #pcolor(X,Y,z',cmap="rainbow")
    
    #ax.add_feature(cfeature.LAND)
    # ax.add_feature(cfeature.RIVERS)
    # ax.add_feature(cfeature.LAKES, alpha=0.5)
    
    title("$ttt")

    colorbar(fraction=0.03, pad=0.04,ticks = ticks)
    xlabel("Longitude", labelpad=10)
    ylabel("Latitude", labelpad=10)
    
end

function hour_plot(arr,csv_flodler,day_time)
    pygui(true)
    cd(csv_flodler)
    file_day = readdir()
    ele_arr = []
    for day in file_day[arr]
        println(day)
        df = CSV.read(day)
        alt = df.MSL_alt
        conde = findall(x->x>=250&&x<=300,alt)
        time_ = df.time[conde]
        geo_lo = df.GEO_lon[conde]
        ele = df.ELEC_dens[conde]
        for (on,n,t) in zip(geo_lo,ele,time_)
            h = Dates.hour(t + Dates.Hour(ceil(on/15)))
            if (h in [2*day_time-2,2*day_time-1])
                append!(ele_arr,n)
            end
        end #end for
    end # end for
    figure()
    plot(ele_arr,"o")
    title("$(csv_flodler[end-3:end]) $(2*day_time-2) $(2*day_time-1)")
    #title("$(csv_flodler[end-3:end]) $alt_down ~ $alt_up")
end


function one_day(arr,csv_flodler,day_time)  
    cd(csv_flodler)
    file_day = readdir()
    for day in file_day[arr]
        println(day)
        df = CSV.read(day)
        alt = df.MSL_alt
        conde = findall(x->x>=250&&x<=300,alt)
        time_ = df.time[conde]
        geo_lo = df.GEO_lon[conde]
        geo_la = df.GEO_lat[conde]
        ele = df.ELEC_dens[conde]
        for (on,at,n,t) in zip(geo_lo,geo_la,ele,time_)
            h = Dates.hour(t + Dates.Hour(ceil(on/15)))
            if (h in [2*day_time-2,2*day_time-1] && n>0)
                x_index = findall(x->x<=on,lon_boundary)[end]
                y_index = findall(x->x<=at,lat_boundary)[end]
                append!(pre_z[x_index][y_index],n)
            end
        end #end for
    end # end for
    #title("$(csv_flodler[end-3:end]) $alt_down ~ $alt_up")
end


#@time find_all([1,2])
#__init__()
# @time find_all_csv([200,201],csv_flodler_2007)
# @time find_all_csv([200,201],csv_flodler_2008)
# @time plot_ion("2007")
# ttttt  = [13]

# for i in ttttt
#     __init__()
#     @time find_all_csv(each_month[i],csv_flodler_2008)
#     @time plot_ion("2008 month $i")
#     savefig("D:\\space physic\\mywork\\2008 month $i.png")
#     #close()
# end




for i in 1:1
    #hour_plot(summer,csv_flodler_2007,i)
    __init__()
    @time one_day(summer,csv_flodler_2008,i)
    @time plot_ion("2008 ($(2*i-2)~$(2*i-1))")
    savefig("D:\\space physic\\FORMOSAT3\\2008 ($(2*i-2)~$(2*i-1)).png")
    #close()
end

# for i in 1:20
#     __init__()
#     @time alt_change(summer,csv_flodler_2008,240+10i,250+10i)
#     @time plot_ion("2008 ($(240+10i) ~ $(250+10i))")
#     savefig("D:\\space physic\\FORMOSAT3\\2008 ($(240+10i) ~ $(250+10i)).png")
#     close()
# end

