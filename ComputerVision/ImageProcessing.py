import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ImageProcessing():

    def __init__(self, path: str, is_gray_scale=False) -> None:
        self.img = cv2.imread(path)
        if is_gray_scale: self.img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    def get_img(self):
        """画像を取得する"""
        return self.img

    def show(self, name):
        """opencvで画像を出力する"""
        cv2.imshow(name, self.img)
        cv2.waitKey()

    def contrast_transform(self, alpha=1, beta=0):
        """ コントラストの変換
        dst(x, y) = alpha * src(x, y) + beta
        :params alpha: コントラスト値
        :params beta: バイアス
        """
        self.img = alpha * self.img + beta
        self.img = np.clip(self.img, 0, 255).astype(np.uint8)

    def gamma_transform(self, gamma=1):
        """ ガンマ変換
        dst(x, y) = 255 * (src(x, y) / 255) ^ (1/gamma)
        :params gamma: ガンマ値
        """
        table = (np.arange(256) / 255) ** gamma * 255
        table = np.clip(table, 0, 255).astype(np.uint8)
        self.img = cv2.LUT(self.img, table)

    def median_blur(self, ksize):
        """メジアンフィルタをかける
        :params ksize: フィルタリングサイズ
        """
        self.img = cv2.medianBlur(self.img, ksize=ksize)

    def reverse(self):
        """画像を反転する（グレースケール）"""
        mask = np.zeros(self.img.shape, np.uint8)
        mask[:,:] = 255
        self.img = cv2.bitwise_xor(self.img, mask)

    def to_gray_scale(self):
        """カラー画像をグレースケールに変換する"""
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

    def to_color_scale_JET(self):
        """グレースケールをJETでカラースケールに変換する"""
        self.img = cv2.applyColorMap(self.img, cv2.COLORMAP_JET)
    
    def to_color_scale_HSV(self):
        """グレースケールをHSVでカラースケールに変換する"""
        self.img = cv2.applyColorMap(self.img, cv2.COLORMAP_HSV)

    def to_color_scale_HSV(self):
        """グレースケールをHOTでカラースケールに変換する"""
        self.img = cv2.applyColorMap(self.img, cv2.COLORMAP_HOT)

    def to_HSV(self):
        """HSV形式に変換する"""
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
    
    def to_LAB(self):
        """LAB形式に変換する"""
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2LAB)

    def threshold_adaptive_gaussian(self, max=255, block_size=5, c=3):
        """ガウスの適応的二値化を行う
        :params max: 閾値よりも大きい時に変換する値
        :params block_size: 適応的二値化をするのに利用するフィルタサイズ
        :params c: バイアス
        """
        self.img = cv2.adaptiveThreshold(self.img, max, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize=block_size, C=c)
    
    def threshold_adaptive_thresh_mean(self, max=255, block_size=5, c=3):
        """平均値を利用した適応的二値化を行う
        :params max: 閾値よりも大きい時に変換する値
        :params block_size: 適応的二値化をするのに利用するフィルタサイズ
        :params c: バイアス
        """
        self.img = cv2.adaptiveThreshold(self.img, max, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=block_size, C=c)

    def threshold_adaptive_clahe(self):
        """claheによる適応的二値化をする"""
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        self.img = clahe.apply(self.img)

    def threshold_otsu(self):
        """大津の二値化をする"""
        ret, self.img = cv2.threshold(self.img, 0, 255, cv2.THRESH_OTSU)

    def threshold_arbitary(self, threshold):
        """任意の閾値で二値化処理を行う"""
        ret, self.img = cv2.threshold(self.img, threshold, 255, cv2.THRESH_BINARY)

    def morphlozy_opening(self, kernel_shape=cv2.MORPH_ELLIPSE, kernel_size=(3, 3), iterations=5):
        """ openingをする
        :params shape: cv.MORPH_ELLIPSE(楕円), cv.MORPH_CLOSE(十字), cv.MORPH_RECT(長方形)から選択する
        :params size: カーネルのサイズ
        :params iterations: イテレーション数
        """
        kernel = cv2.getStructuringElement(shape=kernel_shape, ksize=kernel_size)
        self.img = cv2.morphologyEx(self.img, cv2.MORPH_OPEN, kernel, iterations=iterations)
    
    def morphlozy_closing(self, kernel_shape=cv2.MORPH_ELLIPSE, kernel_size=(3, 3), iterations=5):
        """ closingをする
        :params shape: cv.MORPH_ELLIPSE(楕円), cv.MORPH_CLOSE(十字), cv.MORPH_RECT(長方形)から選択する
        :params size: カーネルのサイズ
        :params iterations: イテレーション数
        """
        kernel = cv2.getStructuringElement(shape=kernel_shape, ksize=kernel_size)
        self.img = cv2.morphologyEx(self.img, cv2.MORPH_CLOSE, kernel, iterations=iterations)

    def display_brightness_value_histgram(self):
        """グレースケールの輝度値ヒストグラムをmatplotlib.pyplotにより出力"""
        data = self.img.flatten()
        section = np.linspace(0,255,255)
        hist, section = np.histogram(data, bins=section)
        section = section[:len(hist)]
        plt.xlabel("brightness", fontsize=18)
        plt.ylabel("number", fontsize=18)
        plt.bar(section, hist, width=8.0)
        plt.show()

    def IoU(self, target):
        """グレースケールのtarget画像とのIoUを取得
        :params target: 画像データ
        :return: IoUの値
        :rtype: float型
        """
        bitwize_and = cv2.bitwise_and(self.img, target)
        bitwize_or = cv2.bitwise_or(self.img, target)
        intersection_size = cv2.countNonZero(bitwize_or)
        union_size = cv2.countNonZero(bitwize_and)
        return intersection_size / union_size

    def all_255_mask(self):
        """全ての輝度値が255のマスクを作成
        :return: マスクされた画像
        """
        mask = np.zeros(self.img.shape, np.uint8)
        mask[:,:] = 255
        return mask

    def change_value(self, idx, value):
        """カラースケール画像の画素値を変更する
        :params idx: 変更する3次元imgのどこの次元を変更するか指定する(idx: 0-3)
        :params value: 変更後の値
        """
        self.img[:,:,idx] = value

    def plot_3D(self, figsize=(16, 8)):
        """カラースケール画像の成分ごとに値を出力する(3次元plot)
        :params figsize: 画像のサイズ
        """
        fig = plt.figure(figsize=figsize)
        axes = {
            0: fig.add_subplot(131, projection='3d'),
            1: fig.add_subplot(132, projection='3d'),
            2: fig.add_subplot(133, projection='3d')
        }
        color = {0: 'blue', 1: 'green', 2: 'red'}
        for idx in range(3):
            x, y, z = [], [], []
            ax = axes[0]
            ax.set_xlabel('x', size=14)
            ax.set_ylabel('y', size=14)
            ax.set_zlabel('z', size=14)
            for i in range(len(self.img[:,:,idx])):
                for j in range(len(self.img[:,:,idx][i])):
                    x.append(i)
                    y.append(j)
                    z.append(self.img[:,:,idx][j])
            ax.plot(x, y, z, color=color[idx])
        plt.show()
