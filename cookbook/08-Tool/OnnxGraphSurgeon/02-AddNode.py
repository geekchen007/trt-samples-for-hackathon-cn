#
# Copyright (c) 2021-2022, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from collections import OrderedDict
import numpy as np
import onnx
import onnx_graphsurgeon as gs

tensor0 = gs.Variable("tensor0", np.float32, ["B", 3, 64, 64])
tensor1 = gs.Variable("tensor1", np.float32, None)
tensor2 = gs.Variable("tensor2", np.float32, None)

node0 = gs.Node("Identity", "myIdentity0", inputs=[tensor0], outputs=[tensor1])
node1 = gs.Node("Identity", "myIdentity1", inputs=[tensor1], outputs=[tensor2])

graph = gs.Graph(nodes=[node0, node1], inputs=[tensor0], outputs=[tensor2])
graph.cleanup().toposort()
onnx.save(gs.export_onnx(graph), "model-02-01.onnx")

for node in graph.nodes:
    if node.op == "Identity" and node.name == "myIdentity0":  # 遍历计算图找到需要添加节点的位置
        constant0 = gs.Constant(name="constant0", values=np.ones(shape=[1, 1, 1, 1], dtype=np.float32))  # 构造新节点和新张量
        tensor3 = gs.Variable("tensor3", np.float32, None)
        newNode = gs.Node("Add", "myAdd", inputs=[node.outputs[0], constant0], outputs=[tensor3])

        graph.nodes.append(newNode)  # 记得把新节点加入计算图中
        index = node.o().inputs.index(node.outputs[0])  # 小心地找到下一个节点中对应输入张量的位置
        node.o().inputs[index] = tensor3  # 替换为新张量

graph.cleanup().toposort()
onnx.save(gs.export_onnx(graph), "model-02-02.onnx")
