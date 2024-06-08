# AIoT_three
AIoT class three

適用於 Espressif 晶片組的 TensorFlow Lite Micro


安裝 ESP IDF
------------
依照 ESP-IDF 入門指南的說明設定工具鏈和 ESP-IDF 本身。接下來的步驟假設此安裝成功且 IDF 環境變數已設定。具體來說，
設定 IDF_PATH 環境變數
```
install.sh
. .export.sh
```

使用組件
------------

在 ESP-IDF 專案中執行以下命令來安裝此元件：
```
cd esp-idf
idf.py add-dependency "esp-tflite-micro"
```

相依套件
------------

在console中執行以下命令來安裝此元件：
```
pip install 
```



建構範例 1 : hello_world
------------

若要取得範例，請執行以下命令：
```
idf.py create-project-from-example "esp-tflite-micro:hello_world"
```
```
cd hello_world
idf.py set-target esp32s3
```
```
idf.py build
```

About Tensorflow
------------
* Tensorflow
  <img width="754" alt="image" src="https://github.com/itemhsu/AIoT_three/assets/25599185/114a8de1-478b-4569-a708-f66a3a43daa6">
  <img width="499" alt="image" src="https://github.com/itemhsu/AIoT_three/assets/25599185/d095e23e-1306-4eed-ae2d-dbd5ca2aae6b">
  <img width="735" alt="image" src="https://github.com/itemhsu/AIoT_three/assets/25599185/d1ddf900-aa76-4de4-af65-65dee0aa6f94">
![image](https://github.com/itemhsu/AIoT_three/assets/25599185/67db8b2b-662b-4d96-95cb-595900a29774)



* Tensorflow lite
  <img width="789" alt="image" src="https://github.com/itemhsu/AIoT_three/assets/25599185/313a7449-5a9d-4b64-ad62-a1ce83e7e498">

<img width="686" alt="image" src="https://github.com/itemhsu/AIoT_three/assets/25599185/7f47a6e8-1b76-4ab0-bcd9-acc69e995ee4">

<img width="772" alt="image" src="https://github.com/itemhsu/AIoT_three/assets/25599185/7399a010-68cc-40ee-947c-fb597e9e565e">

* Tensorflow micro
![image](https://github.com/itemhsu/AIoT_three/assets/25599185/6159352a-cf2d-45c1-b66a-2ed386141c0b)


建構範例 2 : micro_speech
------------

若要取得範例，請執行以下命令：
```
idf.py create-project-from-example "esp-tflite-micro:micro_speech"
```
```
cd micro_speech
idf.py set-target esp32s3
```
```
idf.py build
```

About ESP-NN
------------
 * 分離網路實做及量化實做，專注在神經算子開發
 * 有google 提供大量的tflite 模型可用
 * 效能比較:在各種晶片組上測量的 ESP-NN 優化的快速總結

|   Target  |   TFLite Micro Example  | without ESP-NN  | with ESP-NN | CPU Freq  |
| --------- | ----------------------- | --------------- | ----------- |-----------|
| ESP32-S3  |   Person Detection      |     2300ms      |     54ms    |  240MHz   |
| ESP32     |   Person Detection      |     4084ms      |    380ms    |  240MHz   |
| ESP32-C3  |   Person Detection      |     3355ms      |    426ms    |  160MHz   |


### Kernelwise performance for s8 versions:

  * Kernelwise performance on ESP32-S3 chip
    * Numbers are ticks taken for kernel to execute
    * Chip config: 240MHz, SPI: QPI 80MHz, Data cache: 64KB

    | Function        | ANSI C  | Optimized | Opt Ratio | Data info   | Memory    |
    | ----------------| --------|---------|---------|-------------|-----------|
    | elementwise_add | 312327  | 71644   | 4.36    | size = 1615 | External  |
    | elementwise_mul | 122046  | 30950   | 3.95    | size = 1615 | External  |
    | convolution     | 4642259 | 461398  | 10.06   | input(10,10), filter(64x1x1x64), pad(0,0), stride(1,1) | External |
    | convolution     | 300032  | 43578   | 6.9    | input(8,8), filter(16x1x1x16), pad(0,0), stride(1,1) | External |
    | convolution     | 2106801 | 643689 | 3.27    | input(10,10), filter(64x3x3x3), pad(0,0), stride(1,1) | External |
    | depthwise conv  | 1192832 | 191931  | 6.2    | input (18, 18), pad(0,0), stride(1,1) filter: 1x3x3x16 | External |
    | depthwise conv  | 1679406  | 366102  | 4.59    | input (12, 12), pad(1,1), stride(1,1)  filter: 8x5x5x4 | External |
    | max pool        | 485714  | 76747   | 6.33    | input(16,16), filter (1x3x3x16) | Internal |
    | avg pool        | 541462  | 160580  | 3.37    | input(16,16), filter (1x3x3x16) | Internal |
    | fully connected | 12290   | 4439    | 2.77    | len: 265, ch = 3 | Internal |
    | prelu (relu6)   | 18315   | 1856    | 9.87    | size, 1615  | Internal  |


## Configuration

  * To configure, please use `idf.py menuconfig` and under `ESP-NN` select `NN_OPTIMIZATIONS`
  * There are two options presented:
     * Optimized versions
     * ANSI C

  * Default selection is for `Optimized versions`. For ESP32-S3, assembly versions are automatically selected, whereas for other chips (viz., ESP32, ESP32-C3), generic optimisations are selected.
  * For debugging purposes, you may want to select `ANSI C` reference versions.


建構範例 3 : person_detection
------------

若要取得範例，請執行以下命令：
```
idf.py create-project-from-example "esp-tflite-micro:person_detection"
```
```
cd person_detection
idf.py set-target esp32s3
```
```
idf.py build
```
更新TFLite Micro 
------------

同步到最新的 TFLite Micro 上游,根據上游儲存庫策略，tflite-lib 會複製到此儲存庫中的元件目錄中。我們會不時將其更新到最新的上游版本。在任何情況下，如果您希望在本地更新它，您可以執行
```
scripts/sync_from_tflite_micro.sh
```
學習資源
------------
https://dejazzer.com/eece4710/
https://dejazzer.com/eece4710/index.html#3_resources
