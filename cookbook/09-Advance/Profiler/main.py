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

from cuda import cudart
import numpy as np
import tensorrt as trt

nHeight = 28
nWidth = 28
data = np.random.rand(1, 1, nHeight, nWidth).astype(np.float32).reshape(1, 1, nHeight, nWidth) * 2 - 1
trtFile = "./model.plan"
np.random.seed(31193)
np.set_printoptions(precision=3, linewidth=200, suppress=True)
cudart.cudaDeviceSynchronize()

class MyProfiler(trt.IProfiler):

    def __init__(self):
        super(MyProfiler, self).__init__()

    def report_layer_time(self, layerName, ms):
        print("Timing: %8.3fus -> %s" % (ms * 1000, layerName))

def run(bEmitProfile):
    logger = trt.Logger(trt.Logger.ERROR)
    builder = trt.Builder(logger)
    network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
    profile = builder.create_optimization_profile()
    config = builder.create_builder_config()
    config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 6 << 30)

    inputTensor = network.add_input("inputT0", trt.float32, [-1, 1, nHeight, nWidth])
    profile.set_shape(inputTensor.name, (1, 1, nHeight, nWidth), (4, 1, nHeight, nWidth), (8, 1, nHeight, nWidth))
    config.add_optimization_profile(profile)

    w = np.ascontiguousarray(np.random.rand(32, 1, 5, 5).astype(np.float32))
    b = np.ascontiguousarray(np.random.rand(32, 1, 1).astype(np.float32))
    _0 = network.add_convolution_nd(inputTensor, 32, [5, 5], trt.Weights(w), trt.Weights(b))
    _0.padding_nd = [2, 2]
    _1 = network.add_activation(_0.get_output(0), trt.ActivationType.RELU)
    _2 = network.add_pooling_nd(_1.get_output(0), trt.PoolingType.MAX, [2, 2])
    _2.stride_nd = [2, 2]

    w = np.ascontiguousarray(np.random.rand(64, 32, 5, 5).astype(np.float32))
    b = np.ascontiguousarray(np.random.rand(64, 1, 1).astype(np.float32))
    _3 = network.add_convolution_nd(_2.get_output(0), 64, [5, 5], trt.Weights(w), trt.Weights(b))
    _3.padding_nd = [2, 2]
    _4 = network.add_activation(_3.get_output(0), trt.ActivationType.RELU)
    _5 = network.add_pooling_nd(_4.get_output(0), trt.PoolingType.MAX, [2, 2])
    _5.stride_nd = [2, 2]

    _6 = network.add_shuffle(_5.get_output(0))
    _6.reshape_dims = (-1, 64 * 7 * 7)

    w = np.ascontiguousarray(np.random.rand(64 * 7 * 7, 1024).astype(np.float32))
    b = np.ascontiguousarray(np.random.rand(1, 1024).astype(np.float32))
    _7 = network.add_constant(w.shape, trt.Weights(w))
    _8 = network.add_matrix_multiply(_6.get_output(0), trt.MatrixOperation.NONE, _7.get_output(0), trt.MatrixOperation.NONE)
    _9 = network.add_constant(b.shape, trt.Weights(b))
    _10 = network.add_elementwise(_8.get_output(0), _9.get_output(0), trt.ElementWiseOperation.SUM)
    _11 = network.add_activation(_10.get_output(0), trt.ActivationType.RELU)

    w = np.ascontiguousarray(np.random.rand(1024, 10).astype(np.float32))
    b = np.ascontiguousarray(np.random.rand(1, 10).astype(np.float32))
    _12 = network.add_constant(w.shape, trt.Weights(w))
    _13 = network.add_matrix_multiply(_11.get_output(0), trt.MatrixOperation.NONE, _12.get_output(0), trt.MatrixOperation.NONE)
    _14 = network.add_constant(b.shape, trt.Weights(b))
    _15 = network.add_elementwise(_13.get_output(0), _14.get_output(0), trt.ElementWiseOperation.SUM)

    _16 = network.add_softmax(_15.get_output(0))
    _16.axes = 1 << 1

    _17 = network.add_topk(_16.get_output(0), trt.TopKOperation.MAX, 1, 1 << 1)

    network.mark_output(_17.get_output(1))

    engineString = builder.build_serialized_network(network, config)

    if engineString == None:
        print("Failed building serialized engine!")
        exit()
    print("Succeeded building serialized engine!")

    engine = trt.Runtime(logger).deserialize_cuda_engine(engineString)
    if engine == None:
        print("Failed building engine!")
        exit()
    print("Succeeded building engine!")

    context = engine.create_execution_context()
    context.set_binding_shape(0, [1, 1, nHeight, nWidth])
    context.enqueue_emits_profile = bEmitProfile  # 默认该开关为 True，即所有 execute 均被 profiler 记录，可以手动关闭该开关以指定哪些 execute 才要被记录

    context.profiler = MyProfiler()  # 需要向 context 传入一个自定义的 Profile
    nInput = np.sum([engine.binding_is_input(i) for i in range(engine.num_bindings)])
    nOutput = engine.num_bindings - nInput
    for i in range(nInput):
        print("Bind[%2d]:i[%2d]->" % (i, i), engine.get_binding_dtype(i), engine.get_binding_shape(i), context.get_binding_shape(i), engine.get_binding_name(i))
    for i in range(nInput, nInput + nOutput):
        print("Bind[%2d]:o[%2d]->" % (i, i - nInput), engine.get_binding_dtype(i), engine.get_binding_shape(i), context.get_binding_shape(i), engine.get_binding_name(i))

    bufferH = []
    bufferH.append(np.ascontiguousarray(data))
    for i in range(nInput, nInput + nOutput):
        bufferH.append(np.empty(context.get_binding_shape(i), dtype=trt.nptype(engine.get_binding_dtype(i))))
    bufferD = []
    for i in range(nInput + nOutput):
        bufferD.append(cudart.cudaMalloc(bufferH[i].nbytes)[1])

    for i in range(nInput):
        cudart.cudaMemcpy(bufferD[i], bufferH[i].ctypes.data, bufferH[i].nbytes, cudart.cudaMemcpyKind.cudaMemcpyHostToDevice)

    context.execute_v2(bufferD)  # 当 execute 被调用后， Profile 的 report_layer_time 方法会被调用

    if not bEmitProfile:
        context.report_to_profiler()  # 手动模式下使用该 API 来要求 Profiler 汇报数据，否则 profiler 无动作

    for i in range(nInput, nInput + nOutput):
        cudart.cudaMemcpy(bufferH[i].ctypes.data, bufferD[i], bufferH[i].nbytes, cudart.cudaMemcpyKind.cudaMemcpyDeviceToHost)

    #for i in range(nInput + nOutput):
    #print(engine.get_binding_name(i))
    #print(bufferH[i])

    for b in bufferD:
        cudart.cudaFree(b)

if __name__ == "__main__":
    run(True)
    run(False)
