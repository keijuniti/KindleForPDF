# KindleForPDF

macOS の Kindle アプリのウィンドウを 1 ページ (見開き) ずつ自動で撮影し、1 つの PDF にまとめるツールです。
Web 画面で撮影するウィンドウとページ数を指定すると、ローカルの API が撮影・ページめくり・PDF 化までを行います。

> [!Important]
> 個人が購入した書籍を、私的利用の範囲で PDF 化することを想定しています。
> DRM の解除は行いません (画面に表示された内容を撮影するだけです)。

## 特徴

- **ウィンドウを一覧から選ぶだけ**: 開いているウィンドウをサムネイル付きで一覧表示し、撮影対象を選択できます。
- **バックグラウンドでも動作**: 対象ウィンドウだけを直接撮影し、ページめくりのキー入力も Kindle のプロセスに直接送るため、撮影中に他のアプリを操作しても止まりません。
- **見開き対応**: Kindle は 2 ページ表示のため、撮影枚数は `ceil(ページ数 / 2)` 枚です。
- **事前検証**: 入力不備 (422)・対象ウィンドウ消失 (404)・画面収録の権限不足 (403) は、撮影を始める前にエラーとして返します。

## 使用技術

| 領域 | 技術 | 用途 |
|---|---|---|
| フロントエンド | TypeScript / Next.js 16 (App Router) / React 19 | 画面 (`apps/web`) |
| | React Compiler | 自動メモ化 |
| | Tailwind CSS v4 / shadcn/ui (Radix UI) / lucide-react | スタイリング・UI 部品 |
| | Biome | フォーマット・Lint |
| バックエンド | Python 3.9+ / FastAPI / uvicorn | REST API (`apps/api`) |
| | pyobjc-framework-Quartz | ウィンドウの列挙・権限確認・キー入力の送信 (macOS) |
| | `screencapture` (macOS 標準コマンド) | ウィンドウ単位の撮影 |
| | Pillow | 画像の加工 (グレースケール・縮小・サムネイル) |
| | img2pdf | 画像から PDF への変換 |
| | Pydantic | 入力値の検証 (camelCase 対応) |
| 開発支援 | AGENTS.md / Claude Code / Continue | AI 駆動開発のハーネス (後述) |

## 構成

```
KindleForPDF/
├── apps/
│   ├── web/                 # フロントエンド (Next.js)
│   │   └── src/
│   │       ├── app/                 # ページ (/capture)
│   │       ├── components/          # WindowPicker など
│   │       ├── presentation/hooks/  # useCapture
│   │       ├── domain/models/       # CaptureConfig
│   │       └── infrastructure/api/  # API クライアント
│   └── api/                 # バックエンド (FastAPI, クリーンアーキテクチャ)
│       └── src/
│           ├── interfaces/api/      # エンドポイント (main.py)
│           ├── application/usecases/# CaptureBookUseCase
│           ├── domain/models/       # CaptureConfig
│           └── infrastructure/services/ # OSScreenService (macOS 操作)
├── docs/
│   ├── specs/               # アーキテクチャ・API・画面フローの仕様
│   └── ai-harness/          # AI エージェントの使い方
├── .claude/commands/        # Claude Code 用スラッシュコマンド
├── .continue/prompts/       # Continue 用プロンプト
├── AGENTS.md                # AI への開発ルール
└── CLAUDE.md
```

## 処理の流れ

```
ブラウザ (localhost:3000)                    ローカル API (localhost:8000)

1. 「ウィンドウを選択」 ── GET /windows ──▶  Quartz で開いているウィンドウを列挙し、
                                             各ウィンドウをサムネイル化して返す
2. 一覧から選択 (画面には実名を表示、内部では id を保持)

3. 「キャプチャ実行開始」 ─ POST /capture ─▶ 入力検証 → 権限確認 → ウィンドウ確認
   (targetWindowId, pageCount, interval …)   → バックグラウンドで以下を繰り返す
                                               ・screencapture -l <id> で撮影
                                               ・Kindle に右矢印キーを送信
                                               ・interval 秒待機
                                             → img2pdf で apps/api/outputs/ に PDF を出力
```

### API

| メソッド | パス | 内容 |
|---|---|---|
| GET | `/windows` | 開いているウィンドウ一覧 (`id`・`name`・`title`・`width`・`height`・`preview`) |
| POST | `/capture` | 撮影を開始 (`targetWindowId`・`pageCount`・`interval`・`outputFilename` など) |
| GET | `/health` | 死活確認 |

詳細は [`docs/specs/`](docs/specs/README.md) を参照してください。

## 動作環境

- **macOS 専用** (Quartz・`screencapture` を使うため)
- Node.js 24 系 (LTS)、Python 3.9 以上
- API とブラウザは同じ Mac 上で動かします (撮影・キー入力を行うため)

## 環境構築

### フロントエンド

1. fnm のインストールと設定

```bash
brew install fnm
echo 'eval "$(fnm env --use-on-cd)"' >> ~/.zshrc
source ~/.zshrc
```

2. Node.js (LTS) のインストールと確認

```bash
fnm install --lts
node -v   # v24.x
npm -v    # 11.x
```

3. 依存関係のインストールと API の接続先設定

```bash
cd apps/web
npm install
echo 'NEXT_PUBLIC_API_BASE_URL=http://localhost:8000' > .env
```

> [!Note]
> このプロジェクトでは React Compiler が有効です。
> Biome は開発環境のみ・バージョン固定 (`--save-exact`) で導入しています。

### バックエンド

1. 仮想環境の作成とライブラリのインストール

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

> [!Important]
> サーバーを起動するたびに `source .venv/bin/activate` が必要です (`start-server.sh` は自動で実行します)。

### macOS の権限設定

システム設定 > プライバシーとセキュリティ で、**API を起動するターミナルアプリ** に次の権限を付与し、ターミナルを再起動してください。

| 権限 | 用途 |
|---|---|
| 画面収録 | ウィンドウの撮影・サムネイル表示 |
| アクセシビリティ | Kindle へのページめくりキー入力 |

> [!Note]
> 画面収録の権限がない場合、API は 403 とともに設定手順を返し、画面にも表示されます。

## 起動方法

```bash
# バックエンド (apps/api)
./start-server.sh
# または: source .venv/bin/activate && uvicorn src.interfaces.api.main:app --reload

# フロントエンド (apps/web)
npm run dev
```

1. Kindle アプリで撮影したい本を開き、1 ページ目を表示しておく
2. <http://localhost:3000> を開く (`/capture` に移動します)
3. 「ウィンドウを選択」で Kindle を選ぶ
4. 総ページ数・待機時間・保存ファイル名を入力して「キャプチャ実行開始」
5. 完了すると `apps/api/outputs/<ファイル名>.pdf` に保存されます

## 開発

```bash
# フロントエンドの型チェック・Lint
cd apps/web && npx tsc --noEmit && npx biome check src

# バックエンドのセルフチェック (ウィンドウ一覧・ファイル名の検証・見開き枚数)
cd apps/api && .venv/bin/python -m src.infrastructure.services.os_screen_service_selfcheck
```

## AI 駆動開発

このリポジトリは AI エージェントを使った開発を前提に、ルールと手順をリポジトリに含めています。

- **ルール**: [`AGENTS.md`](AGENTS.md) に「最小のコードで解決する」開発ルール (YAGNI・既存資産の再利用・根本原因の修正・最小限のチェック) を定義しています。
- **5 つの役割別エージェント**: 計画 (`/plan`) → 実装 (`/implement`) → レビュー (`/review`) → テスト (`/test`) → セキュリティ (`/security`) をスラッシュコマンドで呼び出せます。定義は `.claude/commands/` (Claude Code) と `.continue/prompts/` (Continue) にあります。
- **仕様書**: `docs/specs/` にアーキテクチャ・API・画面フローをまとめ、AI が文脈を把握できるようにしています。
- **フィードバックループ**: [`docs/ai-harness/`](docs/ai-harness/README.md) に使い方と、エージェントを改善する手順があります。

## 制限事項

- macOS 専用 (Windows / Linux は未対応)
- 認証なし。ローカル開発での利用のみを想定しています。
- 撮影の進捗表示はありません (バックグラウンドで実行され、完了すると PDF が出力されます)。
- 同時に撮影できるのは 1 件です。
- Kindle 側でキャプチャが保護されているウィンドウは、撮影できない場合があります。
