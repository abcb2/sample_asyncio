# 手探りの時期

特に何もしなければスクリプトはシングルプロセス上のシングルスレッド上で動作する。

- イベントループはスレッド上で動作する
- queueからタスクを取得する
- 各タスクはコルーチンの次のステップを呼び出す
- コルーチンが他のコルーチンを呼び出した場合は現在のコルーチンはサスペンドされ、context switchが発生する
- コルーチンがblocking状態(I/Oやsleepが発生した等)になった場合もコルーチンはサスペンドされコントロールはイベントループに戻される
- イベントループは次のタスクを取得する
- 以後繰り返し

# sample01.py

asyncioのハローワールド

イベントループに処理をhookさせるので、従来の書き方とは頭を切り替える必要がある。

とは言ってもハローワールドだけでは意味がわからないかも。

[引用](https://docs.python.jp/3/library/asyncio-eventloop.html#hello-world-with-call-soon)

# sample02.py

sample2を若干改変。

イベントループは1スレッドでユニークなものになっているはずなので、`asyncio.get_event_loop()`すればどこからでも取得できる。はず。

# sample03.py

`call_soon`と`call_later`の使い方

# sample04.py

色々なイベントハンドラーが存在する。

# sample05.py

タスクとコルーチン

`async def`という関数定義はv3.5以降から以前の`@asyncio.coroutine`と同等で互換性もある？

`コルーチン関数`と呼び、呼び出しの結果取得されるオブジェクトは`コルーチンオブジェクト`。いつかは完了する処理のことを表す。

コルーチン関数は呼び出すだけでは実行されない。スケジューリングする必要がある。

`loop.ensure_future()`や`loop.create_task()`などを使う。

[参照](https://docs.python.jp/3/library/asyncio-task.html#example-hello-world-coroutine)

# sample06.py

あまりアリガタミを感じないコルーチンの例

[参照](https://docs.python.jp/3/library/asyncio-task.html#example-coroutine-displaying-the-current-date)

# sample07.py

コルーチンのチェーン

`await`でコルーチンの処理を待つ。

その感イベントループは他の処理をすることができるがこのサンプルではそこまで明らかにはなっていない。

# sample08.py

`Future`を使ったサンプル

[参照]（https://docs.python.jp/3/library/asyncio-task.html#example-future-with-run-until-complete）

# sample09.py

`run_forever()`とFutureを使ったサンプル

[参照](https://docs.python.jp/3/library/asyncio-task.html#example-future-with-run-until-complete)

# sample10.py

socketpairを使う

# sample11.py

リズムの悪いsocketpairを使ったping-pong

# sample12.py

コルーチン使って`asyncio.sleep`を使う

# sample13.py

リズムのいいPing-pongを書きたいが、ようわからず。

公式のサンプルを写経

https://docs.python.jp/3/library/asyncio-stream.html#register-an-open-socket-to-wait-for-data-using-streams

# sample14.py

デコレータ使わず書きたいがようわからん


# sample100.py

asyncio.sleepを使わないと非同期処理にはならない。合計で7秒近くかかる(time.sleepを使った場合)

asyncio.sleepを使うと合計4秒近くで完了。


# 参考

- http://iuk.hateblo.jp/entry/2017/01/27/173449
- https://qiita.com/icoxfog417/items/07cbf5110ca82629aca0
- https://djangostars.com/blog/asynchronous-programming-in-python-asyncio/

