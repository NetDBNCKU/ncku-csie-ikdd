data = read.csv('train.csv')

# Convert a vector of enumerable strings to a vector of numbers
levels(data$Product_Info_2) = 1 : length(levels(data$Product_Info_2))
data$Product_Info_2 = as.numeric(data$Product_Info_2)

# Fill -1 into losing values
data[is.na(data)] = -1

# calculate the correlation
corr = cor(data)

#write.table(corr, 'output.csv')
