# You will need to first install these packages
library(dplyr)
library(lubridate)
library(tidyr)
library(ggplot2)
library(RColorBrewer)
library(ggridges)


# year represents the year the observation was made

# date represents the day of the year the observation was made.
# The first two digits are for the month and the second two are for the day, so 0102 means January 2nd.

# element says what kind of observation it was:

#   TMAX, TMIN for maximum, minimumum temperature

# PRCP for precipitation (rain)

# value contains the observed value

# temperature units are tenths of degrees celsius, so 102 means 10.2 degrees celsius = 50.36 degrees Fahrenheit.

# PRCP units are tenths of mm, so 136 means 13.6 mm = 0.535 inches of rain fell that day.

# Reading the date as a character preserves the leading 0's
# which simplifies date conversion later
oxford = read.csv("oxford_weather.csv",
                  colClasses = c("integer", "character", "character", "integer"))

oxford %>%
  pivot_wider(names_from = element, values_from = value)->
  bildPrim

# Extract the day of the year
bildPrim %>%
  mutate(date = ymd(paste0(year, date))) %>%
  mutate(day_of_month = day(date)) ->
  bildPrim

bildPrim %>%
  mutate(mo_of_year = month(date)) ->
  bildPrim

bildPrim %>%
  mutate(jan = ifelse(mo_of_year==1,1,0),
         feb = ifelse(mo_of_year==2,1,0),
         march = ifelse(mo_of_year==3,1,0),
         april = ifelse(mo_of_year==4,1,0),
         may = ifelse(mo_of_year==5,1,0),
         june = ifelse(mo_of_year==6,1,0),
         july = ifelse(mo_of_year==7,1,0),
         aug = ifelse(mo_of_year==8,1,0),
         sept = ifelse(mo_of_year==9,1,0),
         oct = ifelse(mo_of_year==10,1,0),
         nov = ifelse(mo_of_year==11,1,0),
         dec = ifelse(mo_of_year==12,1,0),
  ) -> bildPrim

bildPrim %>%
  select(-c(date,mo_of_year,PRCP))->
  bildPrim

# Convert temperatures to Fahrenheit
bildPrim$TMAX <- ((9/5) * (bildPrim$TMAX/10) + 32)
bildPrim$TMIN <- ((9/5) * (bildPrim$TMIN/10) + 32)

midPtVal<-c()

for (i in 1:nrow(bildPrim)){
  tempBuf <- c(bildPrim$TMAX[i],bildPrim$TMIN[i])
  midPtVal[i] = median(tempBuf)
}

bildPrim %>%
  mutate(dailyMid = midPtVal) ->
  bildPrim

bildPrim %>%
  drop_na(dec)->
  bildPrim  

# december is being dropped by R because it appears to be causing a singularity issue,
# correlated with the intercept and year variables?
# december is being dropped by R because it appears to be causing a singularity issue,
# correlated with the intercept and year variables?
# SOOOO that means if I need to doo a prediction for dec I need to remove the year?
med0Mod=lm(dailyMid ~ year+jan+feb+march+april+may+june+july+aug+sept+oct+nov,data = bildPrim)
#summary(med0Mod)

#ggplot(data = bildPrim, mapping = aes(x = year, y = dailyMid))
#anova(medMod,med0Mod)
#medTMod=lm(dailyMid ~ year+TMAX+TMIN+day_of_month+mo_of_year+PRCP,data = bildPrim)
#summary(medMod)
#anova()
# categoragize the months

#med0Day=lm(dailyMid ~ day_of_month+year+jan+feb+march+april+may+june+july+aug+sept+oct+nov,data = bildPrim)
#summary(med0Day)
#summary(med0Mod)
med0Dec=lm(dailyMid ~ jan+feb+march+april+may+june+july+aug+sept+oct+nov+dec,data = bildPrim)
summary(med0Dec)
# yr2024moJan = data.frame(year=2024, jan=1, feb=0,march=0,april=0,may=0,june=0,july=0,aug=0,sept=0,oct=0,nov=0)
# yr2024day4moJan = data.frame(day_of_month=4,year=2024, jan=1, feb=0,march=0,april=0,may=0,june=0,july=0,aug=0,sept=0,oct=0,nov=0)
# yr2024day29moJan = data.frame(day_of_month=29,year=2024, jan=1, feb=0,march=0,april=0,may=0,june=0,july=0,aug=0,sept=0,oct=0,nov=0)
# 
# yr2024moFeb = data.frame(year=2024, jan=0, feb=1,march=0,april=0,may=0,june=0,july=0,aug=0,sept=0,oct=0,nov=0)
# 
# yr2024moMarch = data.frame(year=2024, jan=0, feb=0,march=1,april=0,may=0,june=0,july=0,aug=0,sept=0,oct=0,nov=0)
# 
# yr2024moMay = data.frame(year=2024, jan=0, feb=0,march=0,april=0,may=1,june=0,july=0,aug=0,sept=0,oct=0,nov=0)
# 
# yr2024moOct = data.frame(year=2024, jan=0, feb=0,march=0,april=0,may=0,june=0,july=0,aug=0,sept=0,oct=1,nov=0)
# 
# yr2024moNov = data.frame(year=2024, jan=0, feb=0,march=0,april=0,may=0,june=0,july=0,aug=0,sept=0,oct=0,nov=1)
# 
# predict(med0Mod, new = yr2024moJan, interval = "confidence")
# predict(med0Mod, new = yr2024moJan, interval = "prediction")
# 
# predict(med0Day, new = yr2024day29moJan, interval = "confidence")
# predict(med0Day, new = yr2024day29moJan, interval = "prediction")

# for (j in 2010:2030){
#   predict(med0Mod, new = data.frame(year=j, jan=1, feb=0,march=0,april=0,may=0,june=0,july=0,aug=0,sept=0,oct=0,nov=0predict(med0Mod, new = data.frame(year=2020, jan=1, feb=0,march=0,april=0,may=0,june=0,july=0,aug=0,sept=0,oct=0,nov=0), interval = "prediction")

predict(med0Mod, new = data.frame(year=2050, jan=1, feb=0,march=0,april=0,may=0,june=0,july=0,aug=0,sept=0,oct=0,nov=0), interval = "prediction")

