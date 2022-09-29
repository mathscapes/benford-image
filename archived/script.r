library(tidyr)
library(ggplot2)
batch <- read.csv("batch.csv", header = TRUE, sep = ",")
batch <- pivot_longer(batch, cols = starts_with("red_"), names_to = "rlead", names_prefix = "red_", values_to = "red", values_drop_na = TRUE)
batch <- pivot_longer(batch, cols = starts_with("green_"), names_to = "glead", names_prefix = "green_", values_to = "green", values_drop_na = TRUE)
batch <- pivot_longer(batch, cols = starts_with("blue_"), names_to = "blead", names_prefix = "blue_", values_to = "blue", values_drop_na = TRUE)
batch

ggplot(batch) + 
  geom_boxplot(color='red', aes(rlead, red)) + 
  geom_boxplot(color='green', aes(glead, green)) + 
  geom_boxplot(color='blue', aes(blead, blue)) +
  labs(title='Benford Law Distribution for RGB channelwise data') +
  theme_linedraw()
