
# define a convenient function for rolling the die
roll <- function (rolls=1, die=1:6) {
	sample(die, rolls, replace=TRUE, prob=NULL);
}

set.seed(5946);

# initialize data frame for results
df <- data.frame(trial=rep(NA, 100), 
		 rolls=rep(NA, 100), 
		 sum=rep(NA, 100), 
		 mean=rep(NA, 100), 
		 stdev=rep(NA, 100)
	 	);

# M = 20 ##############################

# run 100 trials for M = 20
for (i in 1:nrow(df)) {
	
	# initialize vector
	result <- c();
	
	# simulate 1 trial of rolling die to SUM >= 20
	while (sum(result) < 20) {
		result <- c(result, roll());
	}

	# store results in data frame
	df$rolls[i] <- length(result);
	df$sum[i] <- sum(result);
	df$mean[i] <- mean(result);
	df$stdev[i] <- sd(result);
	
	df$trial[i] <- list(result);
}

print("### FOR M = 20 ###");
print( paste( "Mean Sum - M =", mean(df$sum) - 20) );
print( paste("StDev Sum - M = ", sd(df$sum) - 20 ) );

print( paste( "Mean Rolls =", mean(df$rolls)) );
print( paste("StDev Rolls = ", sd(df$rolls)) );


# M = 10000 #########################

# run 100 trials for M = 10000
for (i in 1:nrow(df)) {
	
	# initialize vector
	result <- c();
	
	# simulate 1 trial of rolling die to SUM >= 10000
	while (sum(result) < 10000) {
		result <- c(result, roll());
	}
	
	# store results in data frame
	df$rolls[i] <- length(result);
	df$sum[i] <- sum(result);
	df$mean[i] <- mean(result);
	df$stdev[i] <- sd(result);
	
	df$trial[i] <- list(result);
}

print("### FOR M = 10000 ###");
print( paste( "Mean Sum - M =", mean(df$sum) - 10000) );
print( paste("StDev Sum - M = ", sd(df$sum) - 10000 ) );

print( paste( "Mean Rolls =", mean(df$rolls)) );
print( paste("StDev Rolls = ", sd(df$rolls)) );
