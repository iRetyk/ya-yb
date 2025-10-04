from PIL import Image,ImageOps


# Reload the uploaded image
image_path = "/Users/Idan/Downloads/help_lihi2.jpeg"
image = Image.open(image_path)

# convert to black and white.
image = image.convert("L")

reds = ["#FF0000", "#B22222", "#FF6347", "#DC143C", "#8B0000"]
greens = ["#00FF00", "#006400", "#32CD32", "#228B22", "#7CFC00"]

i = 0
for red in reds:
    for green in greens:
        new_image = ImageOps.colorize(image, black=green, white=red)

        # save
        edited_image_path = f"helped_lihi{i}.png"
        new_image.save(edited_image_path)
        i += 1