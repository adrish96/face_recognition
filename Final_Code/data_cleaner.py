##############################################################
#  This will delete all the images which are not jpeg type.  #
#  This accounts for less than 1% of the total database      #
##############################################################


import os

deleted_images=0
path=('training_photos\\')
images=os.listdir(path)
for image_names in images:
    l=len(image_names)
    if image_names[l-5:]!='.jpeg':
        os.remove(path+image_names)
        deleted_images=deleted_images+1

print('done..  images deleted=',deleted_images)
