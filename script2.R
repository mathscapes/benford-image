library(tidyr)
library(ggplot2)
batch <- read.csv("csv/my_csv.csv",header = TRUE, sep = ",")
batch

ggplot(batch) + 
  geom_point(alpha = 0.25, size=2, aes(x=digit, y=pct, color=image)) + 
  geom_line(aes(x=digit, y=pct, color=image), alpha = 0.25) +
  labs(title='Benford Curves for Grayscale data') +
  scale_y_sqrt() +
  scale_x_continuous(breaks = seq(1, 10)) +
  theme_linedraw() + 
  theme(legend.position="none")

