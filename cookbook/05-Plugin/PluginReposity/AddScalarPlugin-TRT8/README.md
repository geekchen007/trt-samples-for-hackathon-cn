# AddScalarPlugin
+ 给输入张量所有元素同时加上一个标量值
+ 输入张量:
    - [0]: (nBatchSize, n1, n2, ...,nK) int32, K>=0
+ 输入参数:
    - [0]: scalar                       int32,
+ 输出张量:
    - [0]: (nBatchSize, n1, n2, ...,nK) float32/float16
+ Steps to run：`make test`
+ Output for reference: ./result.log
