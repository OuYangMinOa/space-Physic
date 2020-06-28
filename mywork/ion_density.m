global z_2;
global lon;
global lat;
global z;
global lon_len;
global lat_len;

floder_2007 = 'D:/space physic/FORMOSAT3/csv_2007';
floder_2008 = 'D:/space physic/FORMOSAT3/csv_2008';

dx = 10;
dy = 5;

lon_len  = 360 / dx;
lat_len  = 180 / dy;

x = linspace(-180,180,lon_len);
y = linspace(-90, 90,lat_len);

global X;
global Y;
[X, Y] = meshgrid(x,y);


lon = linspace(-180+dx,180,lon_len);
lat = linspace(-90 +dy, 90,lat_len);

 
z_2 = cell(lon_len,lat_len,1);

z = zeros(lon_len,lat_len);

walk_data(127:219,floder_2008);
plot_ion();

function walk_data(arr,floderr)
    read_floder = dir( strcat(floderr,"/*.csv"));
    for i = arr
       disp(read_floder(i).name);
       df = readtable( strcat(floderr,'/',read_floder(i).name));
       df_num = table2array(df(:,1:4));
       df_cell = table2cell(df(:,5));
       msL_alt = df_num(:,1);
       geo_lon = df_num(:,2);
       geo_lat = df_num(:,3);
       ele_den = df_num(:,4);
       timeing = df_cell(:);
       add_int_lattice(msL_alt,geo_lon,geo_lat,ele_den,timeing);
    end
end

function add_int_lattice(malt,glon,glat,eden,time_)
    global lon;
    global lat;
    global z_2;
    f = find(malt>250 & malt<400);
    
    for i = 1:length(f)
        x_index_arr = find(lon>=glon(f(i)));
        y_index_arr = find(lat>=glat(f(i)));
        x_index = x_index_arr(1);
        y_index = y_index_arr(1);
        t_str = time_(f(i));
        t_str = t_str{1};
        L_t = mod((str2num(t_str(1:2)) + floor(glon(f(i))/15)),23);
        if (any([22,23,0,1,2]==L_t))
            z_2{x_index,y_index}(end+1,:) = [eden(f(i))];
        end
    end
end


function plot_ion()
    global z_2;
    global lon_len;
    global lat_len;
    global z;
    global X;
    global Y;
    for i =1:lon_len
       for j=1:lat_len
           if (~isempty(z_2{i,j}))
               z(i,j) = median(z_2{i,j});
           else
               z(i,j)=0;
           end
        end
    end
    colormap jet;
    pcolor(X,Y,z');
    shading interp;
    colorbar();
    hold on;
    load coast;
    plot(long,lat,'k');
    axis equal;
    axis([-180 180 -90 90]);
    set(gca,'xtick',-180:30:180);
    set(gca,'ytick',-90:30:90);
    set(gca,'fontsize',12);
    xlabel('Longitude (\circE)');
    ylabel('Latitude (\circN)');
    
end

















