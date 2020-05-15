from google_images_download import google_images_download   #importing the library

# ynm_word_list_txt=open("ynm_word_list.txt","r")


# with open("ynm_word_list.txt", 'rb') as f:
#   contents = f.read()

response = google_images_download.googleimagesdownload()   #class instantiation

arguments = {
    # "keywords_from_file":"ynm_word_list.txt",
    'keywords':"apple2",
    "limit":100,
    "print_urls":True
}   #creating list of arguments

paths = response.download(arguments)   #passing the arguments to the function
print(paths)   #printing absolute paths of the downloaded images