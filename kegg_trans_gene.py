#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import argparse
def read_params(args):
    parser = argparse.ArgumentParser(description='KO列表样式转换对应基因id')
    parser.add_argument('-k','--keg',dest='kegfile',metavar='FILE',type=str,help='KO注释列表')
    parser.add_argument('-l','--list',dest='genelist',metavar='FILE',type=str,help='基因列表')
    parser.add_argument('-o','--outdir',dest='outdir',metavar='FOLDER',type=str,help='输出文件夹')
    parser.add_argument('-m','--mapdir',dest='mapdir',metavar='FOLDER',default=False,type=str,help='输出通路图片文件夹')
    args = parser.parse_args()
    params = vars(args)
    return params

params = read_params(sys.argv)
#读取gene和protein的对应关系列表
#一个基因id对应多个蛋白id，真核生物一个基因编码多种蛋白
gene = {}
with open(params['genelist'],'r') as gene_list:
    for line in gene_list:
        line = line.strip()
        if 'http://www.genome.jp' in line:
            lst = line.split('\t')
            gen = lst[0]
            ko = lst[1].split('|')[0]
            gene[ko]=gen

#整理注释列表，得到表格样式，添加基因、蛋白和KEGG的对应关系
kegg = {}
gene_anno = open(params['outdir']+'/gene_anno.result','w')
gene_anno.write('gene_id\tko4_id\tko4_gene\tEC\tko3_id\tko3_pathway\tko2_id\tko2_name\tko1_id\tko1_name\n')
with open(params['kegfile'],'r') as keg:
    for line in keg:
        line = line.strip()
        if len(line) != 0:
            if line[0] == 'A' and len(line) >1:
                ko1_id = line[1:6]
                ko1_name = line[7:len(line)]
            elif line[0] == 'B' and len(line) > 1:
                ko2_id = line[3:8]
                ko2_name = line[9:len(line)]
            elif line[0] == 'C' and len(line) > 1:
                ko3_id = line[5:10]
                ko3_pathway = line[11:len(line)]
                if ' [' in ko3_pathway:
                    ko3_pathway = ko3_pathway.split(' [')[0]
            elif line[0] == 'D' and len(line) > 1:
                ko_detail = line[7:len(line)].split('; ')
                #protein_id = ko_detail[0]
                ko4_id = line[7:len(line)].split('\t')[1][0:6]
                ko_detail = ko_detail[-1]
                if ' [' in ko_detail:
                    ko_detail = ko_detail.split(' [')
                    ko4_gene = ko_detail[0]
                    EC = '[' + ko_detail[1]
                else:
                    ko4_gene = ko_detail
                    EC = ''
                if ko4_id in gene:
                    gene_anno.write(f'{gene[ko4_id]}\t{ko4_id}\t{ko4_gene}\t{EC}\t{ko3_id}\t{ko3_pathway}\t{ko2_id}\t{ko2_name}\t{ko1_id}\t{ko1_name}\n')
        else:
            continue
gene_anno.close()

#统计注释到各通路的基因数量，以及编辑通路图链接
gene_anno = open(params['outdir']+'/gene_anno.result', 'r')
gene_anno.readline()
pathway = {}
for line in gene_anno:
    line = line.strip().split('\t')
    if line[4] not in pathway:
        ko_class = '\t'.join([line[8],line[9],line[6],line[7],line[4],line[5]])
        pathway[line[4]] = [ko_class, [line[0]], [line[1]]]
    else:
        if line[1] not in pathway[line[4]][2]:
            pathway[line[4]][2].append(line[1])
        if line[0] not in pathway[line[4]][1]:
            pathway[line[4]][1].append(line[0])
gene_anno.close()

pathway_anno = open(params['outdir']+'/pathway_anno.result', 'w')
pathway_anno.write('ko1_id\tko1_name\tko2_id\tko2_name\tko3_id\tko3_pathway\tgene_number\tpathway_link\n')
for key,values in pathway.items():
    gene_number = len(values[1])
    pathway_link = f'https://www.genome.jp/kegg-bin/show_pathway?ko{key}/reference%3dwhite/'
    for ko in values[2]:
        pathway_link += f'{ko}%09orange/'
    pathway_anno.write(f'{values[0]}\t{gene_number}\t{pathway_link}\n')
pathway_anno.close()

#生成所有通路的img文件
import urllib
import urllib.request
import re,os
if params['mapdir']:
    Pathway = open(params['outdir']+'/pathway_anno.result', 'r')
    Pathway.readline()
    os.makedirs(params['mapdir'], exist_ok = True)
    os.chdir(params['mapdir'])
    for line in Pathway:
        line = line.strip().split('\t')
        url = line[-1]
        html = urllib.request.urlopen(url).read()
        img = re.findall(re.compile('src="(.+?\.png)"'), html.decode('utf-8'))
        if img:
            urllib.request.urlretrieve('https://www.genome.jp' + img[0], line[-4] + '.png')
    Pathway.close()
