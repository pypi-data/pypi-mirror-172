## 执行步骤

1. 安装
```bash
pip install tunas2dsdl-c
```

2. 该代码可以统一将tunas 0.3版本的数据集转换为dsdl所需的yaml文件
   ```bash
   tunas2dsdl_c convert -s "/XXX/tunas_data_demo/CIFAR10-tunas" -o "/XXX/tunas_data_demo/CIFAR10-tunas_dsdl/" -l
   ```
     每个参数的意义为：

   | 参数简写 | 参数全写  | 参数解释                                                                                                                      |
   | ----- |---------------------------------------------------------------------------------------------------------------------------| :----------------------------------------------------------- |
   | -s   | `--src_dir`  | tunas 0.3版本的文件的路径                                                                                                         |
   | -o   | `--out_dir` | 可选，生成的yaml的根路径（可以不写，不写默认为和src_dir为同一个根目录但是文件夹名字加上后缀_dsdl）                                                                 |
   | -c   | `--unique_cate` | 可选，这个参数一般不用管，除非你的数据集的category_name是有重复的（目前只有Imagenet是这样的， 所以Imagenet此处要）设置成`wordnet_id`                                   |
   | -l    |  `--local`  | 可选，是否将数据集中的samples单独存储到一个json文件中还是存储在同一个文件中，当样本数量不大的情况下可以使用该选项，默认存储的文件名为XXX_samples.json，保存在同一个目录下（如果使用`-l`则存在同一个yaml文件中） |

   然后就会生成yaml文件。