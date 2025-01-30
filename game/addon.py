class ClickHandler:
    def __init__(self, canvas):
        self.canvas = canvas
        self.start_x = 0
        self.start_y = 0
        self.rect_id = None

        # イベントのバインド
        self.canvas.bind("<Button-1>", self.on_click_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_click_release)

    def on_click_press(self, event):
        # クリック押下時の座標を取得
        self.start_x = event.x
        self.start_y = event.y
        print()
        print(f"Pressed at: x={self.start_x}, y={self.start_y}")

        # 以前の矩形が存在する場合は削除
        if self.rect_id is not None:
            self.canvas.delete(self.rect_id)

        # 新しい矩形を描画
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="blue")

    def on_drag(self, event):
        # マウスがドラッグされたとき、矩形を更新
        current_x = event.x
        current_y = event.y

        # 矩形の座標を更新
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, current_x, current_y)

    def on_click_release(self, event):
        # クリックリリース時の座標を取得
        end_x = event.x
        end_y = event.y
        print(f"Released at: x={end_x}, y={end_y}")

        # 移動距離の計算
        dx = end_x - self.start_x
        dy = end_y - self.start_y
        print(f"Moved: dx={dx}, dy={dy}")
        if self.rect_id is not None:
            self.canvas.delete(self.rect_id)
            self.rect_id = None

if __name__ == "__main__":
    import tkinter as tk

    # テスト用のアプリケーションの設定
    root = tk.Tk()
    root.title("ClickHandler Test")

    # Canvas の作成
    canvas = tk.Canvas(root, width=600, height=400, bg="lightgray")
    canvas.pack()

    # ClickHandler のインスタンスを作成してテスト
    click_handler = ClickHandler(canvas)

    # メインループを開始
    root.mainloop()
