import config

# 加载标签文件，并构建标签字典 一
id2label = {}
with open(config.label_ids_file, 'r', encoding='utf-8') as txt:
    # 循环读取文件每一行
    for line in txt:
        # 去除左右空格并按\t分割
        ID, label = line.strip().split('\t')
        # 构建标签字典
        id2label[ID] = label

print(id2label)

# 循环读取训练集、验证集、测试集
for filepath in [config.train_raw_file, config.eval_raw_file, config.test_raw_file]:
    samples = []
    with open(filepath, 'r', encoding='utf-8') as txt:
        # 循环读取文件每一行
        for line in txt:
            # 去除左右空格并按\t分割得到分诊科室编码与病情文本描述
            ID, text = line.strip().split('\t')
            # 根据字典索引得到对应的科室
            label = id2label[ID]
            # 构建新的格式文件
            sample = label + '\t' + text
            samples.append(sample)

    # 训练集输出文件
    outfile = config.train_data_file
    # 验证集输出文件
    if 'eval' in filepath:
        outfile = config.eval_data_file
    # 测试集输出文件
    if 'test' in filepath:
        outfile = config.test_data_file
    # 将新的格式文件写入到输出文件中
    with open(outfile, 'w') as csv:
        # 表头
        csv.write('label\ttext\n')
        # 循环写入每一个病情及标签
        for sample in samples:
            csv.write(sample)
            # 一个文本一行
            csv.write('\n')
