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

confusion_table <- as.data.frame(table(y_hat, y))
confusion_matrix <- reshape(confusion_table, idvar = "y", timevar = "y_hat", direction = "wide")

acc <- 0
total <- 0
for (i in 1:nrow(confusion_table)) {
  total <- total + confusion_table[i,3]
  if (as.character(confusion_table[i,1]) == as.character(confusion_table[i,2])) {
    acc <- acc + confusion_table[i,3]
  }
}

acc <- (acc * 100) / total

ggplot(data = confusion_table,
       mapping = aes(x = y_hat,
                     y = y)) +
  geom_tile(aes(fill = Freq)) +
  geom_text(aes(label = sprintf("%1.0f", Freq)), vjust = 1) +
  scale_fill_gradient(low = "red",
                      high = "green",
                      trans = "log")
