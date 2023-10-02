### ESLint Configuration (.eslintrc.js)

以下のプロパティを持つESLintの設定ファイル:

- `root`: このプロパティが`true`に設定されている場合、ESLintはこの設定ファイルのディレクトリを設定のルートとして認識します。デフォルトは`false`です。

- `env`: プロジェクトがサポートする環境を指定します。例えば、`browser: true`はブラウザーグローバル変数を使用できることを意味します。

- `extends`: 使用する共有設定のリストを指定します。

- `parser`: 使用するパーサーを指定します。通常は、BabelまたはTypeScriptパーサーが使用されます。

- `parserOptions`: パーサーのオプションを指定します。通常、`ecmaVersion`と`sourceType`の2つのオプションが指定されます。

- `plugins`: 使用するESLintプラグインを指定します。

- `rules`: プロジェクト固有のルールを上書きまたは追加します。

## example

```
module.exports = {
  parser: '@typescript-eslint/parser',  // Specifies the ESLint parser
  extends: [
    'plugin:@typescript-eslint/recommended',  // Uses the recommended rules from @typescript-eslint/eslint-plugin
    'prettier',  // Uses eslint-config-prettier to disable ESLint rules from @typescript-eslint/eslint-plugin that would conflict with prettier
    'plugin:prettier/recommended',  // Enables eslint-plugin-prettier and eslint-config-prettier. This will display prettier errors as ESLint errors. Make sure this is always the last configuration in the extends array.
  ],
  parserOptions: {
    ecmaVersion: 2020,  // Allows for the parsing of modern ECMAScript features
    sourceType: 'module',  // Allows for the use of imports
    ecmaFeatures: {
      jsx: true,  // Allows for the parsing of JSX
    },
  },
  rules: {
    // Place to specify ESLint rules. Can be used to overwrite rules specified from the extended configs
    // e.g. "@typescript-eslint/explicit-function-return-type": "off",
    'no-unused-vars': 'warn',
    "react/react-in-jsx-scope": "off",
  },
  settings: {
    react: {
      version: 'detect',  // Tells eslint-plugin-react to automatically detect the version of React to use
    },
  },
};

```