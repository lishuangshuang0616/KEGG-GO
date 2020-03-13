#帮助文件
library(getopt)
spec <- matrix(c(
  'gene_anno','gene_anno',1,'character',
  'outdir','outdir',1,'character',
  'help', 'help', 0, 'numeric'
  ),byrow = TRUE, ncol = 4)
opt <- getopt(spec)
print_usage <- function(spec = NULL){
  getopt(spec, usage = TRUE)
  cat('
用法参考：
Rscript gene_anno_plot.R --gene_anno --outdir
      ')
  q('no')
}
if (!is.null(opt$help) & is.null(opt$gene_anno)) print_usage(spec)
gene_anno <- opt$gene_anno
outdir <- opt$outdir

#生成通路的gene number文件
library(doBy)
library(ggplot2)
path <- read.delim(gene_anno, stringsAsFactors = FALSE)
stat <- summaryBy(gene_id~ko2_name+ko1_name, data = path, FUN = function(x) length(unique(x)))
names(stat)[3] <- 'gene_number'
stat <- merge(stat, summaryBy(gene_number~ko1_name, data = stat, FUN = sum), by = 'ko1_name', all.x = TRUE)
stat <- stat[order(stat$gene_number.sum, stat$gene_number, decreasing = TRUE), ]
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
setwd(outdir)
#stat['backgroud'] <- nrow(unique(path['gene_id']))
write.table(stat[c('ko1_name', 'ko2_name', 'gene_number')], 'ko2_stat.txt', sep = '\t', row.names = FALSE, quote = FALSE)

#ggplot2 作图
stat$ko2_name <- factor(stat$ko2_name, levels = rev(stat$ko2_name))
stat$ko1_name <- factor(stat$ko1_name, levels = unique(stat$ko1_name))
cols<-rainbow(24)[(1:length(stat$ko1_name))*3]

p <- ggplot(stat, aes(ko2_name, gene_number, fill = ko1_name, label = gene_number)) +
  geom_col() +
  #scale_fill_manual(values = c('#FB8072', '#80B1D3', '#FDB462', '#8DD3C7', '#FFFFB3', '#BEBADA','#B3DE69', '#FCCDE5')) +
  scale_fill_manual(values = cols) +
  coord_flip() +
  labs(title = 'KEGG annotation', y = 'Number of annotated genes', x = 'Function class', fill = '') +
  theme(panel.grid = element_blank(), panel.background = element_rect(color = 'black', fill = 'transparent'), plot.title = element_text(hjust = 0.5)) +
  geom_text(hjust = -0.3, size = 2)

ggsave('ko2_stat.pdf', p, width = 10, height = 8)
ggsave('ko2_stat.png', p, width = 10, height = 8)
