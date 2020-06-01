def normalize_image(image):
    image = image / 255.
    image -= 0.5
    image *= 2.
    image = np.expand_dims(image, axis=0)
    return image