from pyslideshare import pyslideshare
from os.path import basename

def slideshare_upload(username, password, api_key, secret_key, filename, title=None):
    if title is None:
        title = basename(filename).rsplit('.', 1)[0]

    obj = pyslideshare.pyslideshare(
        {  
            "api_key":api_key, 
            "secret_key":secret_key
        }, 
        verbose=False
    )
    json = obj.upload_slideshow(username=username, password=password, slideshow_title=title, slideshow_srcfile=filename)
    slideshow_id = json.SlideShowUploaded.SlideShowID

    return slideshow_id

def slideshare_url(id):
    obj = pyslideshare.pyslideshare(
        {  
            "api_key":api_key, 
            "secret_key":secret_key
        }, 
        verbose=False
    )
    json = obj.get_slideshow(slideshow_id=slideshow_id)
    json.get_slideshow(slideshow_id=10442155)



if __name__ == '__main__':
    api_key = 'WcxW55e6'
    secret_key = 'L7bFrKKX'
    username = 'zuroc'
    password = '198662'
    showId = slideshare_upload(username, password, api_key, secret_key, 'test.ppt')
    print showId
    print slideshare_url(10442155)
