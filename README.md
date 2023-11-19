# Python Pinball Game

## 概要
このプログラムはPythonを使用して作成されたシンプルなピンボールゲームです。Tkinterライブラリを用いてGUIを実装し、基本的な物理法則を適用しています。プレイヤーはボールを操作してスコアを獲得し、ゲームの挑戦を楽しむことができます。

## 特徴
- **基本操作**: プランジャーでボールを発射し、パドルでボールを操作します。
- **スコアシステム**: ターゲットに当たるとスコアが増加し、特定のターゲットをすべて消去するとスコアが大幅に増加します。
- **物理的な挙動**: ボールは壁やパドルからの反射によって運動します。衝突の位置によってボールの反射角度が変わります。

## ゲームプレイ
- **パドルの操作**: 右・左の矢印キーでパドルを動かし、ボールを跳ね返します。
- **ボールの発射**: スペースバーでボールを発射します。
- **スコアの獲得**: ゲームフィールド内のターゲットにボールが当たるとスコアが加算されます。

## インストール方法
1. Pythonがインストールされていることを確認してください。
2. Tkinterライブラリがインストールされていない場合は、以下のコマンドでインストールしてください。
    ```bash
    pip install tk
    ```

3. ゲームのスクリプトを実行してプレイを開始します。
    ```bash
    python [スクリプトのファイル名]
    ```

## 注意点
- このゲームは教育目的で作成されました。商用利用は避けてください。
- ゲームの改善やバグの修正は随時行われる予定です。
