for (i in 2:ncol(cat_df)) {
  ## count no of observations in each subgroup
  obs <- cat_df[,c(1,i)]
  obs <- obs %>% group_by(Attrition,obs[2]) %>% summarise(count=n()) %>% as.data.frame()
  obs <- obs %>% mutate(obs_or_exp = "expt", Variable = names(obs[2]))
  obs <- obs[,c(1,4,5,2,3)]
  
  ## calculate number of expected observations for each subgroup
  expt <- table(cat_df[,c(1,i)])
  chisq <- chisq.test(expt)
  expt <- as.data.frame(chisq$expected)
  expt <- expt %>% mutate(Attrition = c("No","Yes"), obs_or_exp = "expt", Variable = names(obs[4]))
  expt <- data.frame(expt[4:6],stack(expt[1:3]))
  expt[,c(4:5)] = expt[,c(5:4)]
  
  ##rename columns for both df for consistency and union
  names(expt)[c(4:5)] <- c("var_group","cnt")
  names(obs)[c(4:5)] <- c("var_group","cnt")
  var_combined <- rbind(obs,expt)
  
  ## bind to final df "collated" used for visualization
  ifelse(i == 2, collated <- var_combined, collated <- rbind(collated,var_combined))
}