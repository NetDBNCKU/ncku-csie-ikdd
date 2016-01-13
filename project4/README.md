# [Prudential Life Insurance Assessment](https://www.kaggle.com/c/prudential-life-insurance-assessment)

### 所用程式語言
* Python

### 所用模組
* numpy
* MLPClassifier

### 流程
1. 讀入測試資料，並對缺漏資料填補`0.0`
2. 計算各變數間的相關係數
3. 將各變數依相對於`Response`的相關係數絕對值由大至小排序
4. 選取前`37`個變數以類神經網路的方式對測試資料進行學習

### 成績
> [0.517462](https://www.kaggle.com/ikdd112/results)

### 心得
在實作簡化的神經網路時發現，雖然相對大的學習比率會造成學習過程產生振盪的現象，但也因此可以找到一個比較好的初始向量，然後在進一步降低學習比率，來取得收斂的結果。否則，一開始即用相當小的學習比率，不但造成學習效率緩慢，且初始向量影響結果的程度也相對大。
