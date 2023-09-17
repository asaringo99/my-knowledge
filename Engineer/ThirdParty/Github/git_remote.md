# git remote add

参照するremoteリポジトリを追加する時に利用  
git remote add <エイリアス名> <リンク>  
エイリアスはデフォルトでoriginとなっている  
**例**
```
git remote add dev https://github.com/asaringo99/my-knowledge.git
```
```
git remote add origin git@github.com:asaringo99/my-knowledge.git
```
ローカルの.ssh/configが以下のようなときは
```
Host github-asaringo
  HostName github.com
  IdentityFile ~/.ssh/id_rsa2
  User git
```
```
git remote set-url origin git@<ssh configに登録されてるhost名>:<account>/<repo>.git
```
に倣わなければならなく、以下のようにしなければならない
```
git remote add origin git@github-asaringo:asaringo99/my-knowledge.git
```

# git remote set-url
初めてリモートリポジトリを登録する際には`set-url`を利用する。  
git remote set-url <エイリアス名> <リンク>  
例
```
git remote set-url dev https://github.com/asaringo99/my-knowledge.git
```
```
git remote set-url origin git@github-asaringo:asaringo99/task-management-api.git
```