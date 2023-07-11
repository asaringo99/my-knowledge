### ESLint Configuration (.eslintrc.js)

以下のプロパティを持つESLintの設定ファイル:

- `root`: このプロパティが`true`に設定されている場合、ESLintはこの設定ファイルのディレクトリを設定のルートとして認識します。デフォルトは`false`です。

- `env`: プロジェクトがサポートする環境を指定します。例えば、`browser: true`はブラウザーグローバル変数を使用できることを意味します。

- `extends`: 使用する共有設定のリストを指定します。

- `parser`: 使用するパーサーを指定します。通常は、BabelまたはTypeScriptパーサーが使用されます。

- `parserOptions`: パーサーのオプションを指定します。通常、`ecmaVersion`と`sourceType`の2つのオプションが指定されます。

- `plugins`: 使用するESLintプラグインを指定します。

- `rules`: プロジェクト固有のルールを上書きまたは追加します。
