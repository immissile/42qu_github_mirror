from pyslideshare import pyslideshare
from os.path import basename

# Slideshow status : 0 if queued for conversion, 1 if converting , 2 if converted , 3 if conversion failed

def slideshare_upload(api_key, secret_key, username, password, filename, title=None):
    if title is None:
        title = basename(filename).rsplit('.', 1)[0]

    obj = pyslideshare.pyslideshare(
        {
            'api_key':api_key,
            'secret_key':secret_key
        },
        verbose=False
    )
    json = obj.upload_slideshow(username=username, password=password, slideshow_title=title, slideshow_srcfile=filename)
    slideshow_id = json.SlideShowUploaded.SlideShowID

    return slideshow_id

def slideshare_url(api_key, secret_key, id):
    obj = pyslideshare.pyslideshare(
        {
            'api_key':api_key,
            'secret_key':secret_key
        },
        verbose=False
    )
    json = obj.get_slideshow(slideshow_id=id)
    show = json['Slideshows']['Slideshow']
    status = int(show['Status']['value'])

    swf = None
    #print json 
    if status == 2:
        swf = show['EmbedCode']['value']
        begin = swf.find('data="')+6
        end = swf.find('"', begin)
        swf = swf[begin:end]

        begin = swf.find('doc=')+4
        swf = swf[begin:swf.find('&', begin)]

    return status, swf


if __name__ == '__main__':
    api_key = ''
    secret_key = ''
    username = ''
    password = ''

    id = slideshare_upload(api_key, secret_key, username, password, 'test.ppt')

    print slideshare_url(api_key, secret_key, id)
    print slideshare_url(api_key, secret_key, 10442155)


