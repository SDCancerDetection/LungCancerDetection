from PIL import Image
import matplotlib.pyplot as plt

# For a given image, generate a pie chart of body substance based on HU.


patch = ".\\test_patches\\test_patch_0.05_R0.tiff"


# Show the plot of the image
def show_image(image):
    plt.imshow(image, cmap="gray")
    plt.show()


def bin_values(array):

    values = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    labels = ["air", "Lung", "Fat", "Gray Matter", "Soft Tissue", "Bone", "Other", "White Matter", "Muscle"]

    for i in range(len(array)):
        pixel = array[i]
        if pixel < 54:                # air:         pixel < -700
            values[0] += 1
        elif 54 <= pixel < 100:        # lung:        -700 < pixel < -450
            values[1] += 1
        elif 154 <= pixel < 173:      # fat:         -120 < pixel < -50
            values[2] += 1
        elif 188 <= pixel < 191:      # blood:       37 < pixel < 50
            values[3] += 1
        elif 185 <= pixel < 187:      # White Matter: 20 < pixel < 30
            values[7] += 1
        elif 183 <= pixel < 189:      # Muscle:       10 < pixel < 45
            values[8] += 1
        elif 200 <= pixel < 236:      # soft tissue: 100 < pixel < 300
            values[4] += 1
        elif pixel >= 236:            # bone:        300 < pixel
            values[5] += 1
        else:
            values[6] += 1

    return values, labels

def generate_hugraph(path):
    img = Image.open(patch)
    pix_val = list(img.getdata())
    bins, label = bin_values(pix_val)

    fig1, ax1 = plt.subplots()
    ax1.pie(bins, labels=label, autopct='%1.1f%%')
    ax1.axis('equal')

    plt.savefig(path + "\\tempdata\\piechart_HU.png")
    return path + "\\tempdata\\piechart_HU.png"
