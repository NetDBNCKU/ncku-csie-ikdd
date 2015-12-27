data = read.csv('train.csv', header = TRUE)

level_str = sort(unique(data$Product_Info_2))
level = 1 : length(level_str)
names(level) = level_str

data$Product_Info_2 = level[data$Product_Info_2]
