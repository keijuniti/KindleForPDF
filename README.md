# KindleForPDF
## フロントエンド環境構築
1. fnmをinstall
```bash
brew install fnm
```

2. シェルにfnmを追加
```bash
echo 'eval "$(fnm env --use-on-cd)"' >> ~/.zshrc
source ~/.zshrc
```

3. Node.jsの最新LTS（v24.12.0）のインストール
```bash
fnm install --lts
```

4. バージョンの確認
```bash
node -v
v24.12.0
npm -v
11.6.2
```

> [!Note]
> 上記バージョンになってればOK

todo：これを記述するか検討
5. biomeのセットアップ
```bash
npm install --save-dev --save-exact @biomejs/biome
npx biome init
```

> [!Note]
> biomeは下記コマンドでインストールしてます。そのため開発環境のみ＋バージョンの固定を行ってます。
> ```bash
> npm install --save-dev --save-exact @biomejs/biome
> ```



> [!Note]
> このプロジェクトではReact CompilerがONになってます。
> ✔ Would you like to use React Compiler? … No / **Yes**

## バックエンド環境構築
1.  仮想環境を作成して有効化

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

TODO 下記の表示を直す

> [!Note]
> venvnについて
> https://docs.python.org/3/library/venv.html

> [!Important]
> `source .venv/bin_activate`は動かすときに必ず実行してください

2. 必要なライブラリをtomlからインストール

```bash
pip install .
```

TODO 上記ライブラリのリンクは貼る

## サーバーの起動
```bash
uvicorn src.interfaces.api.main:app --reload
```


## 実行時の注意事項
1. 画面全体のスクリーンショットを撮るため、メニューバーを非表示にしてください。

> [!Tip]
> ### macの場合は下記の設定で非表示にします。
> 1. 「設定」を開き、[メニューバー]を選択する。
> 2. 「メニューバーを自動的に表示/非表示」の項目を[常に]を選択する。

# TODOタスク
- [] pip freeze > requirements.txtについて調べる
- [] uvicornについて調べる
- [] fastapiについて調べる_
- [] npmが叩けない問題があった。これはsource ~/.zshrcを叩いたらうまくいったが、そもそもeval fnm envが悪い？？
    - .venvは一度作成したら空の箱みたいな状態。それにpip install .で詰め込むイメージ
- [] shadcn/uiを調べる
- 逆にkindleを開いているとページめくりしてくれない

# 質問すること
- fastapiのパスが通ってない
- __init__.py使ってないし邪魔くさいので消したい

