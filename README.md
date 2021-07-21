# LinkedIn_Web-Scraper_and_Classify
Scrape LinkedIn posts and content based on keywords.
Please see config.txt for full details and usage instructions to add the username and password.
Also,set the variable no_pages to specify the number of pages you want to scrape.
For classification,please check out the ML approaches in :https://drive.google.com/drive/folders/15sZ2WDjGlKx74e60Km0JTyY1xSADPEHe?usp=sharing 's
Classification_New_Approach.ipnyb.
or the string search operations in KeyWordSearch.py .
# The glove.6B.50d.txt file dependency can be downloaded from here:https://www.kaggle.com/watts2/glove6b50dtxt

To do :->
1.Fine tune the model further and also label the train.csv 's examples from 501 to 1818 so that the training size can be increased.
2.Save the final model.
3.Load the final model in Scrape_and_Classify.py and filter the relevant posts into the output excel file.

