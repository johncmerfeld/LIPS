library(ggplot2)
library(reshape2)

data <- data.frame(numChars = seq(1, 33),
  count = c(36,  364, 1487, 3192, 4632, 6199, 6705, 5981, 4924, 3501,
          2120, 1220,  619,  271,  115,   34,   15,    6,    3,    0,    0,
          0,    0,    1,    0,    0,    0,    1,    0,    0,    0,    0,
          1),
  instances = c(90922, 379439, 454939, 435504, 243576, 159275, 124531,
                71363,  50426,  29271,  14292,   5861,   3323,    897,    376,
                86,     24,      7,      3,      0,      0,      0,      0,
                1,      0,      0,      0,      1,      0,      0,      0,
                0,      1))

data$count <- (data$count * 100) / 41427
data$instances <- (data$instances * 100) / 2064118

ggplot(data,
       aes(x = numChars,
           y = count)) +
  geom_bar(stat = 'identity',
           aes(fill = "Unique words in the dictionary")) +
  scale_x_continuous(limits = c(0,20),
                     breaks =  scales::pretty_breaks(n = 20),
                     expand = c(0,0)) + 
  scale_fill_manual(name = "",
                      values = c(`Unique words in the dictionary` = "darkgreen")) +
  labs(x = "Characters per word",
       y = "Percentage of words") +
  theme(legend.text = element_text(size = 16),
        axis.text.x = element_text(size = 16),
        axis.text.y = element_text(size = 16),
        axis.title.x = element_text(size = 16),
        axis.title.y = element_text(size = 16))