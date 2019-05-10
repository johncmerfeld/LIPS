library(data.table)
library(ggplot2)

y <- fread("pred6_ground_truth.csv")
y_hat <- fread("pred6.csv")

colnames(y) <- c("ABOUT","THINK","GOING", 
                 "THERE","WOULD","BECAUSE", 
                 "REALLY","PEOPLE","SOMETHING",
                 "WHICH", "RIGHT", "THIS")

colnames(y_hat) <- c("ABOUT","THINK","GOING", 
                 "THERE","WOULD","BECAUSE", 
                 "REALLY","PEOPLE","SOMETHING",
                 "WHICH", "RIGHT", "THIS")

y <- toupper(names(y)[max.col(y)])
y_hat <- toupper(names(y_hat)[max.col(y_hat)])

confusion_matrix <- as.data.frame(table(y_hat, y))

ggplot(data = confusion_matrix,
       mapping = aes(x = y_hat,
                     y = y)) +
  geom_tile(aes(fill = Freq)) +
  geom_text(aes(label = sprintf("%1.0f", Freq)), vjust = 1) +
  scale_fill_gradient(low = "red",
                      high = "green",
                      trans = "log")
