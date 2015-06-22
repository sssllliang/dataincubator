# taxicab script
#
# This dataset is too large for normal R operations to run efficiently
# (system will crash). Use fastest functions, with minimum RAM requirements,
# and subset data to smallest usable set for each question.


# cbinding (.001s elapsed) should work
if ( !(exists("cab")) ) {
	
	if ( !(exists("trips")) ) {
		trips <- read.csv( unzip("data/trip_data_3.csv.zip") );
	}
	
	if ( !(exists("fares")) ) {
		fares <- read.csv( unzip("data/trip_fare_3.csv.zip") );
	}
	
	cab <- cbind(fares, trips[, c(4:5,7:14)]);
	save(cab, file="data/taxicab.RData");
	
	# keep only columns needed for questions
	cab <- cab[, c(2,4:7,9,11,16:21)];
	rm("trips"); rm("fares");
}

# remove rows with incomplete data
cab <- cab[complete.cases(cab),];

sum( !(fares$medallion == trips$medallion) );
sum( !(fares$hack_license == trips$hack_license) );
sum( !(fares$pickup_datetime == trips$pickup_datetime) );
sum( !(fares$vendor_id == trips$vendor_id) );

# rows match between frames; merge frames, but don't use merge()
system.time(cbind(fares, trips[, c(4:5,7:14)]))




# by definition, this data set is for cabs in NYC: lat=40.7 lon=-74 ; 
# all locations should be within geographic coordinates:
# 40.5 <= lat <= 41 ; -74.5 <= lon <= -71.5
cab <- cab[which(cab$pickup_latitude >= 40.5 & cab$pickup_latitude <= 41), ];
cab <- cab[which(cab$dropoff_latitude >= 40.5 & cab$dropoff_latitude <= 41), ];

cab <- cab[which(cab$pickup_longitude >= -74.5 & cab$pickup_longitude <= -71.5), ];
cab <- cab[which(cab$dropoff_longitude >= -74.5 & cab$dropoff_longitude <= -71.5), ];


range(cab$pickup_latitude);
range(cab$pickup_longitude);
range(cab$dropoff_latitude);
range(cab$dropoff_longitude);


range(cab$fare_amount); 
range(cab$surcharge); 
range(cab$tip_amount); 
range(cab$total_amount); 
# looks like good data; no weird ranges


range(cab$trip_time_in_secs); 
range(cab$trip_distance);

# some rows have 0 for time or distance
# other rows show time = 1s, while distance > 0.5mi
# omit all of this nonsense!
cab <- cab[which(cab$trip_distance > 0.1),];
cab <- cab[which(cab$trip_time_in_secs >= 60),];

# still other rows have distance/time values giving ludicrous speeds
# omit all rows showing avg speed > 60
cab <- cab[(cab$trip_distance <= cab$trip_time_in_secs/60), ];


# 1) What fraction of payments under $5 use a credit card? ####
# payment_type, total_amount   5,11

# subset fields
tmp <- cab[, c("payment_type", "total_amount")];

# subset payments less than $5
tmp <- tmp[which(tmp$total_amount < 5), ];

# count rows with payment_type == 'CRD'
card <- sum(tmp$payment_type == 'CRD');

# find quotient of payments made by card
card / nrow(tmp);

# Answer = 0.09083714



# 2) What fraction of payments over $50 use a credit card? ####
# payment_type, total_amount   5,11

# subset fields
tmp <- cab[, c("payment_type", "total_amount")];

# subset payments greater than $50
tmp <- tmp[which(tmp$total_amount > 50), ];

# count rows with payment_type == 'CRD'
card <- sum(tmp$payment_type == 'CRD');

# find quotient of payments made by card
card / nrow(tmp);

# Answer = 0.6772943




# 3) What is the mean fare per minute driven? ####
# fare_amount, trip_time_in_secs 6,16      

# subset fields
tmp <- cab[, c("fare_amount", "trip_time_in_secs")];

# convert seconds to minutes
tmp$trip_time_in_mins <- tmp$trip_time_in_secs/60;

# calculate average (fare/minute)
mean(tmp$fare / tmp$trip_time_in_mins);

# Answer = $1.07 per minute


# 4) What is the median of the taxi's fare per mile driven? ####
# fare_amount, trip_distance   6,17

# subset fields
tmp <- cab[, c("fare_amount", "trip_distance")];

# calculate median fare per mile
median(cab$fare_amount / cab$trip_distance);

# Answer = 5.000


# 5) What is the 95th percentile of the taxi's average driving speed in miles per hour? ####
# trip_distance, trip_time_in_secs   16,17

# subset columns
tmp <- cab[, c("trip_distance", "trip_time_in_secs")];

# convert seconds to hours
tmp$trip_time_in_hours <- tmp$trip_time_in_secs/3600;

# calculate average speed
tmp$speed <- tmp$trip_distance / tmp$trip_time_in_hours;

# find the 95th percentile
quantile(tmp$speed, probs=seq(.9,1,.05))

# Answer = 26.47059


# 6) What is the average ratio of the distance between the pickup and dropoff divided by the distance driven?* ####
# trip_distance, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude 17:21

# subset the columns
tmp <- cab[ ,c("trip_distance", "pickup_longitude", "pickup_latitude", "dropoff_longitude", "dropoff_latitude")];

# calculate the great circle distance
library("geosphere");

p1 <- matrix(c(tmp$pickup_longitude, tmp$pickup_latitude), nrow=15315922, ncol=2);
p2 <- matrix(c(tmp$dropoff_longitude, tmp$dropoff_latitude), nrow=15315922, ncol=2);

# great circle distance in miles
tmp$gc_distance <- distCosine(p1, p2, r=3959);

# calculate the avg ratio of gc_distance to trip_distance
mean(tmp$gc_distance / tmp$trip_distance);

# Answer = 0.7946263


# 7) What is the average tip for rides from JFK? ####
# tip_amount, pickup_longitude, pickup_latitude   9,18,19

# subset columns
tmp <- cab[, c("tip_amount", "pickup_longitude", "pickup_latitude")];

# from google maps, JFK lat=40.641510, lon=-73.778139
sum(
	tmp$pickup_longitude >= -73.80 & 
	tmp$pickup_longitude <= -73.77 &	
    	tmp$pickup_latitude  >= 40.64 &
	tmp$pickup_latitude  <= 40.65
    );
# ~ 220,000 pickups at JFK

# subset pickups from JFK
tmp <- tmp[ which(tmp$pickup_longitude >= -73.80 & 
		  	tmp$pickup_longitude <= -73.77 &	
		  	tmp$pickup_latitude  >= 40.64 &
		  	tmp$pickup_latitude  <= 40.65) , ];

# calculate average tip
mean(tmp$tip_amount);

# Answer = $4.478592



# 8) What is the median March revenue of a taxi driver? ####
# hack_license, pickup_datetime, fare_amount, surcharge, tip_amount   4,6,7,9

# subset columns
tmp <- cab[ , c("hack_license", "pickup_datetime", "fare_amount", "surcharge", "tip_amount")];

# convert factors to dates
tmp$pickup_datetime <- as.Date(tmp$pickup_datetime);


range(tmp$pickup_datetime);
# all cab rides occurred in March
tmp <- tmp[, -2]; # omit date column


# according to  http://work.chron.com/much-fare-taxi-drivers-keep-22871.html
# drivers keep ~2/3 of their gross fares, therefore . . .
# subtract .33 of gross fares

# add net revenue to df, then sort by driver; then get median:
tmp$revenue <- (tmp$tip_amount + 2*(tmp$fare_amount + tmp$surcharge)/3 );

tmp <- tmp[,c(1,5)];

# aggregate by driver (32750 unique hack licenses)
tmp <- aggregate.data.frame(x = list(tmp$revenue), by = list(tmp$hack_license), FUN = sum);
names(tmp) <- c("hack_license", "revenue");

# get median revenue
median(tmp$revenue);
 # Answer: 4657.342

# end #################################
