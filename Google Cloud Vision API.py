#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from google.cloud import vision
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/mydrive/repositories/ml/cs231n-goog-vision-svc-acct.json"
client = vision.ImageAnnotatorClient ()


# In[ ]:


import io

path = '/Users/sheetal/Desktop/ml notes/Conv Sets.jpg'
with io.open(path, 'rb') as image_file:
        content = image_file.read()


# In[ ]:


image = vision.types.Image(content=content)


# In[ ]:


response = client.document_text_detection(image=image)


# In[ ]:


response

