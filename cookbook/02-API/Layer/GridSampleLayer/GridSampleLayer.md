# Grid Sample Layer

+ Simple example

---

## Simple example

+ Refer to SimpleExample.py

```txt
[ 0]Input -> DataType.FLOAT (1, 3, 4, 5) (1, 3, 4, 5) inputT0
[ 1]Input -> DataType.FLOAT (1, 6, 10, 2) (1, 6, 10, 2) inputT1
[ 2]Output-> DataType.FLOAT (1, 3, 6, 10) (1, 3, 6, 10) (Unnamed Layer* 0) [GridSample]_output
inputT0
[[[[  0.   1.   2.   3.   4.]
   [ 10.  11.  12.  13.  14.]
   [ 20.  21.  22.  23.  24.]
   [ 30.  31.  32.  33.  34.]]

  [[100. 101. 102. 103. 104.]
   [110. 111. 112. 113. 114.]
   [120. 121. 122. 123. 124.]
   [130. 131. 132. 133. 134.]]

  [[200. 201. 202. 203. 204.]
   [210. 211. 212. 213. 214.]
   [220. 221. 222. 223. 224.]
   [230. 231. 232. 233. 234.]]]]
inputT1
[[[[ 0.33333334  0.        ]
   [-1.         -0.5       ]
   [-0.33333334 -0.5       ]
   [-0.33333334 -0.5       ]
   [ 1.         -0.5       ]
   [ 1.          0.5       ]
   [ 0.33333334 -0.5       ]
   [ 1.         -1.        ]
   [-1.         -1.        ]
   [ 1.          0.        ]]

  [[ 1.         -0.5       ]
   [ 0.33333334  0.5       ]
   [-0.33333334 -1.        ]
   [-0.33333334  0.        ]
   [ 1.          0.        ]
   [-0.33333334  1.        ]
   [ 0.33333334 -1.        ]
   [-1.         -0.5       ]
   [ 0.33333334 -1.        ]
   [-1.          0.5       ]]

  [[ 0.33333334  1.        ]
   [-0.33333334  0.        ]
   [-0.33333334 -0.5       ]
   [ 0.33333334  0.5       ]
   [-1.         -1.        ]
   [ 0.33333334 -1.        ]
   [-1.         -1.        ]
   [ 1.          0.        ]
   [ 1.          1.        ]
   [-1.         -1.        ]]

  [[ 1.          1.        ]
   [-1.          0.5       ]
   [-0.33333334 -1.        ]
   [-0.33333334  0.        ]
   [-1.         -0.5       ]
   [-1.          1.        ]
   [ 0.33333334 -1.        ]
   [ 0.33333334 -1.        ]
   [-1.         -1.        ]
   [-1.         -1.        ]]

  [[ 0.33333334 -0.5       ]
   [-0.33333334 -1.        ]
   [-1.         -1.        ]
   [-1.          1.        ]
   [-1.         -1.        ]
   [-1.          1.        ]
   [ 0.33333334  1.        ]
   [ 1.         -0.5       ]
   [ 0.33333334  0.        ]
   [ 1.         -1.        ]]

  [[ 1.          0.        ]
   [-0.33333334 -0.5       ]
   [-0.33333334  1.        ]
   [-0.33333334  0.5       ]
   [ 1.          0.        ]
   [-0.33333334  0.5       ]
   [ 1.          1.        ]
   [ 0.33333334  1.        ]
   [-0.33333334  1.        ]
   [-1.          1.        ]]]]
(Unnamed Layer* 0) [GridSample]_output
[[[[ 17.833334     2.5          6.166666     6.166666     4.5         14.5          7.833334     1.           0.           9.5       ]
   [  4.5         27.833332     0.58333325  16.166668     9.5         15.583333     1.4166667    2.5          1.4166667   12.5       ]
   [ 16.416666    16.166668     6.166666    27.833332     0.           1.4166667    0.           9.5          8.5          0.        ]
   [  8.5         12.5          0.58333325  16.166668     2.5          7.5          1.4166667    1.4166667    0.           0.        ]
   [  7.833334     0.58333325   0.           7.5          0.           7.5         16.416666     4.5         17.833334     1.        ]
   [  9.5          6.166666    15.583333    26.166668     9.5         26.166668     8.5         16.416666    15.583333     7.5       ]]

  [[117.833336    52.5        106.166664   106.166664    54.5         64.5        107.833336    26.          25.          59.5       ]
   [ 54.5        127.83333     50.583332   116.166664    59.5         65.583336    51.416668    52.5         51.416668    62.5       ]
   [ 66.416664   116.166664   106.166664   127.83333     25.          51.416668    25.          59.5         33.5         25.        ]
   [ 33.5         62.5         50.583332   116.166664    52.5         32.5         51.416668    51.416668    25.          25.        ]
   [107.833336    50.583332    25.          32.5         25.          32.5         66.416664    54.5        117.833336    26.        ]
   [ 59.5        106.166664    65.583336   126.16667     59.5        126.16667     33.5         66.416664    65.583336    32.5       ]]

  [[217.83333    102.5        206.16667    206.16667    104.5        114.5        207.83333     51.          50.         109.5       ]
   [104.5        227.83333    100.583336   216.16667    109.5        115.58333    101.416664   102.5        101.416664   112.5       ]
   [116.416664   216.16667    206.16667    227.83333     50.         101.416664    50.         109.5         58.5         50.        ]
   [ 58.5        112.5        100.583336   216.16667    102.5         57.5        101.416664   101.416664    50.          50.        ]
   [207.83333    100.583336    50.          57.5         50.          57.5        116.416664   104.5        217.83333     51.        ]
   [109.5        206.16667    115.58333    226.16666    109.5        226.16666     58.5        116.416664   115.58333     57.5       ]]]]
```
