from PIL import Image, ImageDraw, ImageFont
from Consts import *

resampling = [Image.Resampling.NEAREST, Image.Resampling.BOX,
              Image.Resampling.BILINEAR, Image.Resampling.HAMMING,
              Image.Resampling.BICUBIC, Image.Resampling.LANCZOS]
resampling_index = 5
default_resampling = resampling[resampling_index]


def rescale(size_from, size_to, size):
    return ((size_to[0] * size_from[0]) // size[0],
            (size_to[1] * size_from[1]) // size[1])


def get_cords(pos, size):
    return pos[0], pos[1], pos[0] + size[0], pos[1] + size[1]


def clear_image(name_image, pos, size):
    if size == (0, 0):
        return
    with Image.open(name_image) as image:
        draw = ImageDraw.Draw(image)
        draw.rectangle(get_cords(pos, size), fill=TRANSPARENT)
        image.save(name_image)


class Paint:
    def __init__(self, size, background_dir, draft_dir=DEFAULT_DRAFT_DIR,
                 font=BASE_FONT_DIR, font_size=TAB_FONT_SIZE):
        self.size = size
        self.background_dir = background_dir
        self.draft_dir = draft_dir
        self.save_dir = ""
        self.font_small = ImageFont.truetype(font, font_size)
        # it rescales draft
        # self.quick_update_size()

    def cut_rectangle(self, pos, size):
        with (Image.open(self.background_dir).convert("RGBA") as background_image,
              Image.open(self.draft_dir).convert("RGBA") as draft):
            background_seg = background_image.crop(get_cords(pos, size))

            rescaled_pos = rescale(pos, draft.size, self.size)
            rescaled_size = rescale(size, draft.size, self.size)

            rescaled_background_seg = background_seg.resize(rescaled_size, default_resampling)

            draft.paste(rescaled_background_seg, rescaled_pos)
            draft.save(self.draft_dir)

    def clear_draft(self):
        self.cut_rectangle((0, 0), self.size)

######
    def reset_draft(self, draft_dir=DEFAULT_DRAFT_DIR):
        self.clear_draft()
        with (Image.open(self.draft_dir) as image,
              Image.open(self.background_dir) as background_image,
              Image.open(draft_dir) as draft):
            background_image = background_image.resize(draft.size, default_resampling)
            image = image.resize(draft.size, default_resampling)
            draft = Image.alpha_composite(background_image, image)
            draft.save(draft_dir)

######
    def merge_backgrounds(self):
        with (Image.open(self.draft_dir) as image,
              Image.open(self.background_dir) as background_image):
            final_image = Image.new("RGBA", self.size, TRANSPARENT)
            final_image.alpha_composite(background_image, image)
            return final_image

    def change_rectangle_background(self, paste_pos, paste_image_name):
        with (Image.open(self.draft_dir) as image,
              Image.open(paste_image_name) as paste_image):
            image.paste(paste_image, paste_pos)
            image.save(self.draft_dir)

    def paste_member(self, pos, paste_image):
        with (Image.open(self.background_dir) as background_image,
              Image.open(self.draft_dir) as draft):
            background_seg = background_image.crop(get_cords(pos, paste_image.size))
            rescaled_paste_image_size = rescale(draft.size, paste_image.size, self.size)
            rescaled_pos = rescale(draft.size, pos, self.size)
            rescaled_background_seg = background_seg.resize(rescaled_paste_image_size, default_resampling)
            rescaled_paste_image = paste_image.resize(rescaled_paste_image_size, default_resampling)
            draft_image = Image.alpha_composite(rescaled_background_seg, rescaled_paste_image)
            draft.paste(draft_image, rescaled_pos, draft_image)
            draft.save(self.draft_dir)

    def paste_member_by_dir(self, pos, paste_image_dir):
        with Image.open(paste_image_dir) as paste_image:
            self.paste_member(pos, paste_image)

    def draw_member(self, pos, paste_image):
        with (Image.open(self.background_dir) as background_image,
              Image.open(self.save_dir) as draft):
            background_seg = background_image.crop(get_cords(pos, paste_image.size))
            save_image = Image.alpha_composite(background_seg, paste_image)
            draft.paste(save_image, pos, save_image)
            draft.save(self.save_dir)

    def draw_member_by_dir(self, pos, paste_image_dir):
        with Image.open(paste_image_dir) as paste_image:
            self.draw_member(pos, paste_image)

### fucking bad


    def get_size(self):
        return self.size

    def get_draft_dir(self):
        return self.draft_dir

    def get_background_dir(self):
        return self.background_dir

    def set_size(self, new_size):
        self.size = new_size

    def set_draft_dir(self, draft_dir):
        self.draft_dir = draft_dir

######
    def change_name_image_global(self, new_name_image,
                                 draft_dir=DEFAULT_DRAFT_DIR):
        self.draft_dir = new_name_image
        self.reset_draft(draft_dir)

    def change_name_background_image(self,
                                     new_name_background_image):
        self.background_dir = new_name_background_image

#####
    def change_name_background_image_global(self,
                                            new_name_background_image):
        self.background_dir = new_name_background_image
        self.reset_draft(self.draft_dir)

#######
    def quick_update_size(self):
       with (Image.open(self.draft_dir) as image,
             Image.open(self.background_dir) as background):
           if self.size == image.size and self.size == background.size:
               return
           if self.size != image.size:
               (image.resize(self.size, Image.Resampling.LANCZOS)).save(self.draft_dir)
           if self.size != background.size:
               (background.resize(self.size, Image.Resampling.LANCZOS)).save(self.background_dir)


class PaintImage(Paint):
    def __init__(self, size, background_dir,
                 draft_dir, name_final_image):
        super().__init__(size, background_dir, draft_dir)
        self.background_image = Image.open(name_final_image)
        self.image = Image.open(draft_dir)
        self.final_image = Image.open(name_final_image)