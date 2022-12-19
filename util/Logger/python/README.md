# ロガーのサンプルコード

## 利用したデザインパターン
- Singleton pattern  
log start を一度のみ呼び出すためにsingletonを採用しています。

## decoratorの利用
decoratorの利用によって
```
main():
  log.info("start")

  --- 処理 ---

  log.info("end")
```

という処理を書くのではなく

```
@log
main():
  --- 処理 ---
```

というようなスッキリとした形を実現させています。

## 得られるlog
以下のようなlogが得られます。
```
------------ START LOGGER [2022-12-19 21:46:39] ------------
2022-12-19 21:46:39.857 [INFO]	sample.py - main:17 -> main: START
2022-12-19 21:46:39.857 [INFO]	sample.py - roop:13 -> roop: START
2022-12-19 21:46:40.070 [INFO]	sample.py - roop:13 -> roop: END(process time : 0.210586)
2022-12-19 21:46:40.070 [WARNING]	sample.py - main:14 -> END ---> func: roop
2022-12-19 21:46:40.070 [INFO]	sample.py - main:17 -> main: END(process time : 0.211286)
```