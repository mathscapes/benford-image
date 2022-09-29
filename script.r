library(ggplot2)
batch <- read.csv("csv/batch_test.csv",header = TRUE, sep = ",")
batch

ggplot(batch) + 
  geom_point(alpha = 0.25, size=2, aes(x=dig, y=prb, color=ref)) + 
  geom_line(aes(x=dig, y=prb, color=ref), alpha = 0.25) +
  geom_line(aes(x=dig, y=ben), color="blue") + 
  ylim(0,40) +
  scale_x_continuous(breaks = seq(1, 10)) +
  theme_linedraw() + 
  theme(legend.position="none")

