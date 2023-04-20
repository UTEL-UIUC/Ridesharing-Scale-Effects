library(binsreg)
library(ggplot2)
library(ggpubr)
library(patchwork)
library("gridExtra")
library('grid')
library(svglite)


line_add <- function(df,pred_var){
  y_pred = df[pred_var]
  return(geom_line(aes(x=df$count_shared_realized, y = y_pred),color ='red',size =3))
}

df_od = read.delim('od_Jan_Sep.txt',sep=',')
df_detour = read.delim('detour_data_Jan_Sep.txt',sep=',')
plot_OD <- function(i){
  od_int = df_od$OD[i]
  df <- df_detour[df_detour$OD == od_int ,]
  ## Add random noise to increase unique values
  df$count_shared_realized = df$count_shared_realized + rnorm(nrow(df),0,0.01)
  df$y <- df$detour_dis_actual
  df$x <- 1/df$count_shared_realized
  
  df_pre_sep <- df[df$pickup_month <=9,]
  
  pre_min <- floor(min(df_pre_sep$count_shared_realized))
  pre_max <- ceiling(max(df_pre_sep$count_shared_realized))
  x_pre <- seq(pre_min,pre_max,0.1)
  
  r1_pre = lm(y ~ x,data = df_pre_sep)
  print(max(df_pre_sep$count_shared_realized))
  
  
  df_pre_sep$x_pred1 = predict(r1_pre)
  
  # return( c(r1,r2,r3,r4))
  colors <- c("y=x" = "blue", "y=1/x" = "red", "y=sqrt(x)" = "orange", "y=1/sqrt(x)" = "green")
  
  bin_plot1 <- binsreg(data = df_pre_sep,x = count_shared_realized, y = detour_dis_actual,ci = c(1,0),cb = c(0,0),nbins = 8)
  plot1<- bin_plot1$bins_plot+
    geom_line(aes(x=df_pre_sep$count_shared_realized, y = df_pre_sep$x_pred1,color ='y=1/x'),size =1)+
    labs(title = paste0(" OD Pair ", i, "; Jan-Sep;" ," RMSE=", round(sqrt(mean(r1_pre$residuals^2)),3)),x = expression(paste("Matched shared trips "*"n"[sm]^"O,D"*"(h,d,m)")),y = expression(paste("Detour distance "*"de"^"O,D"*"(h,d,m)"*" (mile)")))+
    scale_color_manual(name ='Regression Fit',values = colors)+ 
    theme(axis.text = element_text(size = 12),axis.title = element_text(size = 16),plot.title = element_text(size = 14))
  ggsave(paste0("detour_plots_all/Pre_Sep_OD_Pair_",i,".pdf"),plot1,width = 8 , height = 4, dpi =320)
  
}

table_grob = lapply(1:16, function(i) plot_OD(i))
