mytheme <- function(base_size = 12, base_family = "") {
  library(ggthemes)
  opts <- options()
  options(ggplot2.continuous.color="viridis")
  options(ggplot2.continuous.fill="viridis")
  theme_gray() %+replace%
    theme(
      panel.grid =element_line(color="aquamarine3",linetype="dotted"),
      panel.grid.minor = element_blank(),
      panel.background = element_rect(fill="#FBF0FF"),
      plot.background = element_rect(fill="#FFFBF0"),
      panel.border = element_rect(colour = "#FBF0FF",fill=NA,size=1),
      plot.title = element_text(color="black",size=rel(1.7),
                                hjust=0.5,vjust=2.5,
                                family = "serif"),
      axis.text = element_text(size = rel(1.2),colour="black",
                               family="serif"),
      axis.title = element_text(size = rel(1.3),colour="black",
                                family="serif"),
      plot.margin = margin(t=rel(20),b=rel(3),r=rel(8),l=rel(5)),
      legend.background = element_rect(fill = "#F0FFFB"),
      legend.text = element_text(family="serif"),
      legend.title = element_text(family="serif"),
      legend.position = "right",
      legend.justification = "top",
      axis.ticks.length = unit(6,"pt"),
      complete=TRUE
    )
}
