# You will need to first install these packages
library(dplyr)
library(lubridate)


# Reading the date as a character preserves the leading 0's
# which simplifies date conversion later
oxford = read.csv("C:\\Users\\mikeb\\Documents\\R\\oxford_weather.csv",
    colClasses = c("integer", "character", "character", "integer"))

# Extract the day of the year
oxford %>%
    mutate(date = ymd(paste0(year, date))) %>%
  mutate(dayOfMonth = day(date)) ->
  oxford

# Extract the month
oxford %>%
  mutate(monthOfYear = month(date)) ->
  oxford

# Convert temperatures to Fahrenheit
oxford %>%
    filter(element %in% c("TMAX", "TMIN")) %>%
    mutate(temperature = (9/5) * (value/10) + 32) ->
    temps

# average max and min temperature each year
temps %>%
    group_by(year, element) %>%
    summarize(temperature = mean(temperature)) ->
    year_hilo_temps

# median of the midway point between high and low temperature
# each day
temps %>%
    group_by(date) %>%
    mutate(midtemp = mean(temperature)) %>%
    group_by(year) %>%
    summarize(temperature = median(midtemp)) ->
    year_mid_temps
    
# Looks like global warming is a real thing, at least in Oxford.
with(year_mid_temps, plot(year, temperature))

# temps %>%
#   group_by(element)  %>%
#  
datamtcars
data("mtcars")
