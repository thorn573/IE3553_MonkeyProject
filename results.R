library(readr)

ci <- function(x1, x2) {
  n <- length(x1)
  
  X1 <- mean(x1)
  X2 <- mean(x2)
  
  S1 <- var(x1)
  S2 <- var(x2)
  
  z <- qnorm(0.975)
  c <- c(-1, 1)
  
  return((X2 - X1) + c * z * sqrt((S1 + S2) / n))
}

QWERTY.dat <- read_csv("QWERTY.csv")
Uniform.dat <- read_csv("Uniform.csv")
QFMLWY.dat <- read_csv("QFMLWY.csv")
Norman.dat <- read_csv("Norman.csv")
Alphabetical.dat <- read_csv("Alphabetical.csv")

qwerty_uniform.ci <- ci(QWERTY.dat$TIME, Uniform.dat$TIME)
mean(qwerty_uniform.ci)

qwerty_qfmlwy.ci <- ci(QWERTY.dat$TIME, QFMLWY.dat$TIME)
mean(qwerty_qfmlwy.ci)

qwerty_norman.ci <- ci(QWERTY.dat$TIME, Norman.dat$TIME)
mean(qwerty_norman.ci)

qwerty_alphabetical.ci <- ci(QWERTY.dat$TIME, Alphabetical.dat$TIME)
mean(qwerty_alphabetical.ci)

histo <- function(x1, x2) {
  col1 <- "yellow"
  col2 <- "olivedrab2"
  
  hist1 <- hist(x1)
  hist2 <- hist(x2)
  
  xl <- c(min(min(x1), min(x2)) - 2, max(max(x1), max(x2)) + 2)
  yl <- c(min(min(hist1$counts), min(hist2$counts)), 
          max(max(hist1$counts), max(hist2$counts)))
  
  hist(x1,
       breaks = 10,
       xlim = xl,
       ylim = yl,
       xlab = "Time (Minutes)",
       ylab = "Counts",
       main = "Time Historgram",
       col = rgb(234 / 255, 1, 0, 0.4))
  
  par(new = TRUE)
  
  hist(x2,
       breaks = 10,
       xlim = xl,
       ylim = yl,
       xlab = "",
       ylab = "",
       main = "",
       col = rgb(129 / 255, 1, 51 / 255, 0.4))
  
  legend(x = "topright", legend = c("QWERTY","QFMLWY"), 
         fill = c(col1,col2))
  
}

histo(QWERTY.dat$TIME, QFMLWY.dat$TIME)


