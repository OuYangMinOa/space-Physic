using DataFrames,CSV,NetCDF

Floder = "D:\\space physic\\FORMOSAT3\\2007"
save_file ="D:\\space physic\\FORMOSAT3\\csv_2007"

cd(Floder)
file_day = readdir()
for day in file_day
    cd(string(Floder,"\\",day))
    file = readdir()
    alt = []
    geo_lo = []
    geo_la = []
    ele = []
    timeing = []
    for each in file
        arr = split(each,".")
        this_time = join([arr[4],":",arr[5]])
        alllt = ncread(each,"MSL_alt")
        append!(alt,alllt)
        append!(geo_lo,ncread(each,"GEO_lon"))
        append!(geo_la,ncread(each,"GEO_lat"))
        append!(ele   ,ncread(each,"ELEC_dens"))
        append!(timeing,[this_time for i in 1:length(alllt)])
    end
    df = DataFrame(MSL_alt=alt,GEO_lon=geo_lo,GEO_lat=geo_la,ELEC_dens=ele,time=timeing)
    CSV.write(string(save_file,"\\$day.csv"), df)
end




