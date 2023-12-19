

# Run

```bash
# 首先生成测试样例
python generateTestSample.py

# 然后对测试用例进行交叉最小化处理，并绘图
python main.py
```



# 文件说明

1.生成测试样例 generateTestSample.py

会将生成的层次图记录到csv文件中



2.读取csv文件，read_csv.py

得到一个字典结构的图G



3.sugiyama.py

包括：

```
解循环（去除回边）
再次插入回边
节点分层
虚拟节点
交叉最小化
坐标分配（归一化的坐标）
```

因为图的层次分配已经固定，所以可以只调用“交叉最小化”和“坐标分配”模块即可



4.graph.py 绘制层次图

节点少的可以绘制成png图，而节点多、层次多的最好调大画布，并绘制为SVG图



5.graphLib.py

处理图网络的一些小功能



networkx图的属性：

```python
for node in G.nodes():
    print(node, G.nodes()[node]['pos'])
```

pygraphviz图的属性：

```python
 for node in G.nodes():
    print(node, node.attr['pos'])
```

