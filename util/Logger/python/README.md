# Sample code of Logger

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