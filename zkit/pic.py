#coding:utf-8
from cStringIO import StringIO
import Image

def picopen(image):
    if not image:return

    if hasattr(image, 'getim'): # a PIL Image object
        im = image
    else:
        if not hasattr(image, 'read'): # image content string
            image = StringIO(image)
        try:
            im = Image.open(image) # file-like object
        except IOError, e:
            return

    if im.mode == 'RGBA':
        p = Image.new('RGBA', im.size, 'white')
        try:
            x, y = im.size
            p.paste(im, (0, 0, x, y), im)
            im = p
        except:
            pass
        del p

    if im.mode == 'P':
        need_rgb = True
    elif im.mode == 'L':
        need_rgb = True
    elif im.mode == 'CMYK':
        need_rgb = True
    else:
        need_rgb = False

    if need_rgb:
        try:
            im = im.convert('RGB', dither=Image.NONE)
        except IndexError:
            pass
    return im


def pic_resize_width_cut_height_if_large(image, width, max_height=None):
    if not image:return
    if max_height == None:
        max_height = width*2.5

    x, y = image.size
    if x != width:
        image = image.resize((width, (width*y)/x), Image.ANTIALIAS)

    if max_height:
        x, y = image.size
        if y > max_height:
            image = image.crop((0, 0, x, max_height))
    return image


def pic_fit_width_cut_height_if_large(image, width, max_height=None):
    if not image:return

    x, y = image.size
    if x > width:
        image = image.resize((width, (width*y)/x), Image.ANTIALIAS)

    if max_height:
        x, y = image.size
        if y > max_height:
            image = image.crop((0, 0, x, max_height))
    return image


def pic_zoom_outer(image, width, height, max_width, max_height):
    x, y = image.size
    if x < width:
        image = image.resize((width, (width*y)/x), Image.ANTIALIAS)

    if y > max_height:
        image = image.crop((0, 0, x, max_height))
    elif y < height:
        image = image.resize(((height*x)/y, height), Image.ANTIALIAS)

    x, y = image.size

    if x > max_width:
        image = image.crop((0, 0, max_width, y))

    return image


def pic_zoom_inner(image, width, height=None):
    if height == None:
        height = width

    x, y = image.size
    if x > width or y > height:
        #x*height > width*y 缩放到height,剪裁掉width
        x_h = x*height
        w_y = width*y

        if x_h <= w_y:
            cuted_height = height
            cuted_width = x*height//y
        else:
            cuted_height = y*width//x
            cuted_width = width
        image = image.resize((cuted_width, cuted_height), Image.ANTIALIAS)

    return image


def pic_fit(image, width, height=None):
    if height == None:
        height = width

    x, y = image.size
    if x != width or y != height:
        #x*height > width*y 缩放到height,剪裁掉width
        x_h = x*height
        w_y = width*y

        if x_h != w_y:
            if x_h > w_y:
                cuted_height = height
                cuted_width = x*height//y
            else:
                cuted_height = y*width//x
                cuted_width = width
        else:
            cuted_width = width
            cuted_height = height
        image = image.resize((cuted_width, cuted_height), Image.ANTIALIAS)

        x, y = image.size

        if x_h != w_y:
            if x_h > w_y:
                width_begin = (x-width)//4
                height_begin = 0
            else:
                width_begin = 0
                height_begin = (y-height)//4

            image = image.crop((width_begin, height_begin, width_begin+width, height_begin+height))

    return image


def pic_fit_height_if_high(image, width, height=None):
    if height == None:
        height = width

    x, y = image.size
    if x < y:
        p = Image.new('RGBA', (y, y), 'white')
        p.paste(image, ((y-x)//2, 0))
        image = p
        del p

    return pic_fit(image, width, height)


def _calc_square(x, y, width, top_left, size, zoom_out):
    height_delta = width
    default = True # 是否使用默认缩放策略
    if top_left is not None:
        try:
            ax, ay = top_left
            if ax < 0 or ay < 0:
                default = True
            elif size <= 0:
                default = True
            elif ax + size > x:
                default = True
            elif ay + size > y:
                default = True
            else:
                # 用户指定了合法的参数，则使用用户指定缩放策略
                default = False
        except:
            pass

    resize = None
    if default:
        zoom_in = (x > width and y > width)
        background = (x < width or y < width)

        # 如果图过小，需要粘贴在一个白色背景的图片上
        px, py = (width-x)/2, (width-y)/2
        if px < 0:
            px = 0
        if py < 0:
            py = 0
        paste = (px, py)

        # 如果允许放大，就不再需要往白色背景图片上粘贴
        if zoom_out and background:
            zoom_out = x < y and 'x' or 'y'
            if zoom_out == 'x':
                nx = width
                ny = width*y/x
            else:
                nx = width*x/y
                ny = width
            resize = (nx, ny)

            x, y = resize
            ax, ay = (x-width)/2, (y-width)/2
            if ax < 0:
                ax = 0
            if ay < 0:
                ay = 0
            bx = ax + width
            by = ay + width
        else:
            # 计算如何缩小
            if x > width and y > width:
                if x > y:
                    ax, bx = (x-y)/2, (x+y)/2
                    ay, by = 0, y
                else:
                    ax, bx = 0, x
                    ay, by = (y-x)/2, (y+x)/2
                    height_delta = x
            else:
                ax, ay, bx, by = (x-width)/2, (y-width)/2, (x+width)/2, (y+width)/2
                if ax < 0:
                    bx += ax
                    ax = 0
                if ay < 0:
                    by += ay
                    ay = 0

        # 高 > 宽时，需要调整，上方、下方切掉的区域高度比例要是 1:3。
        if y > x and y > width:
            ay -= (y - height_delta) / 4
            by -= (y - height_delta) / 4
        if bx > x:
            bx = x
        if by > y:
            by = y
        crop = [ax, ay, bx, by]
    else:
        zoom_in = (size != width)
        crop = [ax, ay, ax + size, ay + size]
        background = False
        paste = (0, 0)
    return zoom_out, resize, crop, zoom_in, background, paste


def pic_square(im, width, top_left=None, size=0, zoom_out=True):

    x, y = im.size
    zoom_out, resize, crop, zoom_in, background, paste =      \
            _calc_square(x, y, width, top_left, size, zoom_out)

    if zoom_out and resize:
        im = im.resize(resize, Image.ANTIALIAS)

    (ax, ay, bx, by) = crop
    if not ((ax, ay) == (0, 0) and (bx, by) == im.size):
        im = im.crop(crop)

    if not (zoom_out and resize):
        if zoom_in:
            try:
                im = im.resize((width, width), Image.ANTIALIAS)
            except:
                raise PictureError
        if background:
            p = Image.new('RGBA', (width, width), 'white')
            p.paste(im, paste)
            im = p
            del p

    return im


def pic_merge(im1, im2):
    x1, y1 = im1.size
    x2, y2 = im2.size
    bg = Image.new('RGB', ((max(x1, x2), y1+y2+10)), (255, 255, 255))
    bg.paste(im1, (0, 0, x1, y1))
    bg.paste(im2, (0, y1+10, x2, 10+y1+y2))
    return bg
