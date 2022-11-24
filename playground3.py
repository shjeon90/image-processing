import cv2

def main():
    img = cv2.imread('/Users/shjeon/tmp/image.jpeg', cv2.IMREAD_GRAYSCALE)
    print(type(img))
    print(img.shape)
    print(img.min(), img.max())

if __name__ == '__main__':
    main()