allBeer<-read.csv("C:/Users/Matthew/Desktop/BigData/Project/AllBeerforR.csv",quote="\"",encoding='UTF-8')
beerStyles<-unique(allBeer$beer_style)
meanPerStyle<-function(beerStyles,allBeer){
  styleScores=vector('numeric')
  for (style in beerStyles){
    styleSet=allBeer[allBeer$beer_style==style,]
    styleScores<-c(styleScores,mean(styleSet$SCORE))
  }
  names(styleScores)<-beerStyles
  return(styleScores)
}
a<-meanPerStyle(beerStyles,allBeer)
write.table(a,"C:/Users/Matthew/Desktop/BigData/Project/StyleScores.csv",sep=",")
overallPerStyle<-function(beerStyles,allBeer){
  styleScores=vector('numeric')
  for (style in beerStyles){
    styleSet=allBeer[allBeer$beer_style==style,]
    styleScores<-c(styleScores,mean(styleSet$OVERALL..20.))
  }
  names(styleScores)<-beerStyles
  return(styleScores)
}
a<-overallPerStyle(beerStyles,allBeer)
write.table(a,"C:/Users/Matthew/Desktop/BigData/Project/StyleOverall.csv",sep=",")
abvPerStyle<-function(beerStyles,allBeer){
  styleScores=vector('numeric')
  for (style in beerStyles){
    styleSet=allBeer[allBeer$beer_style==style,]
    styleSet=styleSet[!is.na(styleSet$ABV....),]
    styleScores<-c(styleScores,mean(styleSet$ABV....))
  }
  names(styleScores)<-beerStyles
  return(styleScores)
}
a<-abvPerStyle(beerStyles,allBeer)
write.table(a,"C:/Users/Matthew/Desktop/BigData/Project/StyleABV.csv",sep=",")
write.table(table(allBeer$beer_style),"C:/Users/Matthew/Desktop/BigData/Project/StyleCounts.csv",sep=",")

sakeList<-c('Saké - Ginjo','Saké - Daiginjo','Saké - Genshu','Saké - Nigori')
