from PIL import Image


def watermark(img_post, img_wm, position):
    img_post_p = Image.open(img_post)
    img_wm = Image.open(img_wm)
    position = int(position)
    if position == 1:
        img_wm = img_wm.resize((img_post_p.size[1] // 6, img_post_p.size[1] // 6))
        img_post_p.paste(
            img_wm,
            (img_post_p.size[0] // 15, img_post_p.size[1] // 15),
            img_wm.convert("RGBA"),
        )
    elif position == 2:
        img_wm = img_wm.resize((img_post_p.size[1] // 6, img_post_p.size[1] // 6))
        img_post_p.paste(
            img_wm,
            (
                img_post_p.size[0] - img_post_p.size[0] // 15 * 3,
                img_post_p.size[1] // 15,
            ),
            img_wm.convert("RGBA"),
        )
    elif position == 3:
        img_wm = img_wm.resize((img_post_p.size[1] // 6, img_post_p.size[1] // 6))
        img_post_p.paste(
            img_wm,
            (
                img_post_p.size[0] // 15,
                img_post_p.size[1] - img_post_p.size[1] // 15 * 3,
            ),
            img_wm.convert("RGBA"),
        )
    elif position == 4:
        img_wm = img_wm.resize((img_post_p.size[1] // 6, img_post_p.size[1] // 6))
        img_post_p.paste(
            img_wm,
            (
                img_post_p.size[0] - img_post_p.size[0] // 15 * 3,
                img_post_p.size[1] - img_post_p.size[1] // 15 * 3,
            ),
            img_wm.convert("RGBA"),
        )
    img_post_p.save(f'photos_gen/{img_post.split("/")[-1]}')
    return f'photos_gen/{img_post.split("/")[-1]}'
