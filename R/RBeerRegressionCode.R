allStyles<-read.csv("C:/Users/Matthew/Desktop/BigData/Project/ddddd.csv",quote="\"",encoding='UTF-8')

a<-lm(Average.Rating~average.ABV,data=allStyles)
j<-seq(2,14,1)
afitline<-a$coefficients[1]+a$coefficients[2]*j
plot(allStyles$average.ABV,allStyles$Average.Rating,xlab="Average ABV",ylab="Average Rating",main="Higher Alcohol - Better Rating?",xlim=c(0,15))
lines(afitline,lwd=3,col="red")
text(x=allStyles[allStyles$Average.Rating<2.7,]$average.ABV,y=allStyles[allStyles$Average.Rating<2.7,]$Average.Rating,label=allStyles[allStyles$Average.Rating<2.7,]$Beer.Style,pos=c(4,4,3,4))
