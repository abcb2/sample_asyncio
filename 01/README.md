# 手探りの時期

特に何もしなければスクリプトはシングルプロセス上のシングルスレッド上で動作する。

- イベントループはスレッド上で動作する
- queueからタスクを取得する
- 各タスクはコルーチンの次のステップを呼び出す
- コルーチンが他のコルーチンを呼び出した場合は現在のコルーチンはサスペンドされ、context switchが発生する
- コルーチンがblocking状態(I/Oやsleepが発生した等)になった場合もコルーチンはサスペンドされコントロールはイベントループに戻される
- イベントループは次のタスクを取得する
- 以後繰り返し

# sample1.py

asyncioのハローワールド

イベントループに処理をhookさせるので、従来の書き方とは頭を切り替える必要がある。

とは言ってもハローワールドだけでは意味がわからないかも。

[引用](https://docs.python.jp/3/library/asyncio-eventloop.html#hello-world-with-call-soon)

# sample2.py

sample2を若干改変。

イベントループは1スレッドでユニークなものになっているはずなので、`asyncio.get_event_loop()`すればどこからでも取得できる。はず。

# sample100.py

asyncio.sleepを使わないと非同期処理にはならない。合計で7秒近くかかる(time.sleepを使った場合)
asyncio.sleepを使うと合計4秒近くで完了。


# 参考

- http://iuk.hateblo.jp/entry/2017/01/27/173449
- https://qiita.com/icoxfog417/items/07cbf5110ca82629aca0
- https://djangostars.com/blog/asynchronous-programming-in-python-asyncio/