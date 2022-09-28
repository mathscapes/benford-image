library(tidyr)
library(ggplot2)
batch <- read.csv("csv/bs2_data.csv", header = TRUE, sep = ",")
batch

ggplot(batch) + 
  geom_point(alpha = 0.5, size=2, aes(x=digit, y=gray, color=image)) + 
  geom_line(aes(x=digit, y=gray, color=image), alpha = 0.5) +
  labs(title='Benford Curves for Grayscale data') +
  ylim(0,100) + 
  scale_x_continuous(breaks = seq(1, 10)) +
  theme_linedraw()
