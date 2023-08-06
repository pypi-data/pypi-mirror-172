参考サイト
https://zenn.dev/sikkim/articles/490f4043230b5a

ライブラリの反映手順
setup.py のバージョンを更新
python setup.py sdist で配布物のビルド
python setup.py bdist_wheel Wheelパッケージをビルド

テスト環境にアップロード(依存関係などでエラーが出ないか)
twine upload --repository testpypi dist/*

本番環境にアップロード
twine upload --repository pypi dist/*

依存関係にあるライブラリは勝手に追加される訳では無いが､
このライブラリを使うときに一括でインストールができるように
requirement を作っておいて上げるほうがいい
エラー文として出るが｡


パッケージに必要なライブラリの書き出し
cd で対象のフォルダに移動
(なければ pip install pipreqs)
pipreqs --encoding UTF8 .
で必要なライブラリを書き出してくれる

pipenv にも適応したい場合
pipenv install -r requirements.txt
上記で[requirements.txt]の内容を出力

pipenv graph
で依存関係が表示されるので､大本のライブラリのみ抜き出して記載