import matplotlib.pyplot as plt
import numpy as np

# 假設你有一個 list 包含了你想要顯示的日期
dates = ['2022-07-01', '2022-07-02', '2022-07-03',
         '2022-07-04', '2022-07-05', '2022-07-09', '2022-07-10']
y = np.random.randn(len(dates))

fig, ax = plt.subplots()
ax.plot(dates, y)

# 設定 x 軸的刻度
ax.set_xticks(dates)

# 設定 x 軸的標籤旋轉 45 度
plt.xticks(rotation=45)

plt.show()


# 创建第一个图
plt.subplot(3, 3, 1)
plt.plot([1, 2, 3], [1, 2, 3])
plt.title('Plot 1')

# 创建第二个图
plt.subplot(3, 3, 2)
plt.plot([1, 2, 3], [3, 2, 1])
plt.title('Plot 2')

# 创建第三个图
plt.subplot(3, 3, 3)
plt.plot([1, 2, 3], [2, 3, 1])
plt.title('Plot 3')

# 创建第四个图
plt.subplot(3, 3, 4)
plt.plot([1, 2, 3], [2, 1, 3])
plt.title('Plot 4')

plt.subplot(3, 3, 5)
plt.plot([1, 2, 3], [2, 1, 3])
plt.title('Plot 4')

plt.subplot(3, 3, 6)
plt.plot([1, 2, 3], [2, 1, 3])
plt.title('Plot 4')

plt.subplot(3, 3, 7)
plt.plot([1, 2, 3], [2, 1, 3])
plt.title('Plot 4')

plt.subplot(3, 3, 8)
plt.plot([1, 2, 3], [2, 1, 3])
plt.title('Plot 4')

plt.subplot(3, 3, 9)
plt.plot([1, 2, 3], [2, 1, 3])
plt.title('Plot 4')

plt.tight_layout()  # 自动调整子图的布局，防止重叠
plt.show()
