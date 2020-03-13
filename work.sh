python kegg_trans.py -k /opt/work/user/lishuangshuang/learning/GOKEGG/KASS/result/1.keg -l /opt/work/user/lishuangshuang/learning/GOKEGG/KASS/gene.list.txt -o /opt/work/user/lishuangshuang/bin/KEGG
python kegg_trans_gene.py -k hsa00001.keg -l gene.annote -o /opt/work/user/lishuangshuang/bin/KEGG/test
Rscript gene_anno_plot.R --gene_anno /opt/work/user/lishuangshuang/bin/KEGG/test/gene_anno.result --outdir /opt/work/user/lishuangshuang/bin/KEGG/stats
