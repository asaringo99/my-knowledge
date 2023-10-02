# git clone
ローカルの.ssh/configが以下のようなときは
```
Host github-asaringo
  HostName github.com
  IdentityFile ~/.ssh/id_rsa2
  User git
```
以下のようにクローンする必要しなければならない時がある
```
git clone git@<sshconfigで登録してるhost名>:asaringo99/repo.git
```