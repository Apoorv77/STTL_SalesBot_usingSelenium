import os, random, sys, time, re
from datetime import datetime
from urllib.parse import urlparse
from selenium import webdriver
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sklearn import tree
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
import pickle
import nltk
from nltk.tokenize import ToktokTokenizer
nltk.download('stopwords')
#Helper Functions
def read_glove_vecs(glove_file):
    with open(glove_file, 'r',encoding="utf8") as f:
        words = set()
        word_to_vec_map = {}
        for line in f:
            line = line.strip().split()
            curr_word = line[0]
            words.add(curr_word)
            word_to_vec_map[curr_word] = np.array(line[1:], dtype=np.float64)
        
        i = 1
        words_to_index = {}
        index_to_words = {}
        for w in sorted(words):
            words_to_index[w] = i
            index_to_words[i] = w
            i = i + 1
    return words_to_index, index_to_words, word_to_vec_map
tokenizer = ToktokTokenizer()
stopword_list = nltk.corpus.stopwords.words('english')
stopword_list.remove('not')
def remove_stopwords(text):
    # convert sentence into token of words
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    # check in lowercase 
    t = [token for token in tokens if token.lower() not in stopword_list]
    text = ' '.join(t)    
    return text
def remove_special_characters(text):
    # define the pattern to keep
    pat = r'[#]'
    t=re.sub(pat,',',text)
    pat = r'[^a-zA-z0-9.,!?/:;\"\'\s]' 
    return re.sub(pat, '', t)
def sentences_to_indices(X, word_to_index, max_len):
    """
    Converts an array of sentences (strings) into an array of indices corresponding to words in the sentences.
    The output shape should be such that it can be given to `Embedding()` (described in Figure 4). 
    
    Arguments:
    X -- array of sentences (strings), of shape (m, 1)
    word_to_index -- a dictionary containing the each word mapped to its index
    max_len -- maximum number of words in a sentence. You can assume every sentence in X is no longer than this. 
    
    Returns:
    X_indices -- array of indices corresponding to words in the sentences from X, of shape (m, max_len)
    """
    
    m = X.shape[0]                                   # number of training examples
    # Initialize X_indices as a numpy matrix of zeros and the correct shape (≈ 1 line)
    X_indices =np.zeros((m,max_len))
    
    for i in range(m):                               # loop over training examples
        
        # Convert the ith training sentence in lower case and split is into words. You should get a list of words.
        sentence_words = X[i].lower().split()
        
        # Initialize j to 0
        j = 0
        
        # Loop over the words of sentence_words

        for w in sentence_words:
            # if w exists in the word_to_index dictionary
            if w in word_to_index:
                # Set the (i,j)th entry of X_indices to the index of the correct word.
                X_indices[i, j] = word_to_index[w]
                # Increment j to j + 1
                j =  j+1
                if(j>=maxLen):
                    return X_indices
            
    
    return X_indices




browser = webdriver.Chrome(executable_path=r"./chromedriver.exe")
browser.get("https://www.linkedin.com/uas/login")
file = open("config.txt")
lines = file.readlines()
username = lines[0]
password = lines[1]
elementID = browser.find_element_by_id("username")
elementID.send_keys(username)
elementID = browser.find_element_by_id("password")
elementID.send_keys(password)
# link = 'https://www.linkedin.com/feed/hashtag/internships/'
# link = 'https://www.linkedin.com/search/results/content/?keywords=research%2C%20intern'
list_1 = [
    "developer recommendations",
    "app developer recommendations",
    "RPA Consultant recommendations",
    "Ecommerce solutions",
    "SAP support recommendations",
    "Magento solution provider",
   "Digitial Transformation Experts",
]
list_1 = ["looking for "+ i  for i in list_1]
list_2=["Software",
    "Application",
    "Product",
    "Customize application",
    "Customize product",
    ".net application",
    "bespoke dot net",
    "custome dot net",
    "enterprise dotnet application",
    "Angular",
    "React",
    "Native",
    "Full Stack",
    "Mobile application",
    "iOS",
    "android",
    "app developer",
    "enterprise mobile application",
    "enterpise mobility solution",
    "Magento multistore",
    "open source",
    "php application",
    "drupal",
    "custom cms",
    "joomla",
    "website",
    "web developer",
    "SAP B1 Support",
    "SAP Business One Support",
    "SAP B1 Add On",
    "SAP Business One Add On",
    "SAP B1 Implementation",
    "SAP Business One Implementation",
    "RPA Implementation",
    "Digital Transformation Consultants"]
list_2 = [i+" required"  for i in list_2]
search_list=list_1+list_2
link = "https://www.linkedin.com/search/results/content/?keywords="
no_pages = 5
a = []
for search in search_list:
    search = re.sub("\s", "%20", search)
    search_url = link + search
    browser.get(search_url)

    SCROLL_PAUSE_TIME = 3
    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")
    for i in range(10):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    browser.find_element_by_tag_name("body").send_keys(Keys.CONTROL + Keys.HOME)

    browser.find_element_by_tag_name("body").send_keys(Keys.CONTROL + Keys.HOME)
    connect_buttons = browser.find_elements_by_class_name(
        "feed-shared-inline-show-more-text__see-more-less-toggle"
    )

    timestamp = str(datetime.now().date())
    src = browser.page_source
    soup = BeautifulSoup(src, "lxml")

    master_data = soup.find_all("div", {"class": "feed-shared-update-v2"})
    info = soup.find_all("div", {"class": "feed-shared-actor__meta"})

    base_link = browser.current_url
    for j in range(1, no_pages + 1):
        if j > 1:
            curr_link = base_link + "&page=" + str(j)
            browser.get(curr_link)
        for i in range(1, 11):
            try:
                path = (
                "//div[@id='search-marvel-srp-scroll-container']/div[1]/div[1]/ul[1]/li["
                + str(i)
                + "]/div[1]/div[1]"
                )
                browser.find_element_by_xpath(path).click()
                src = browser.page_source
                soup = BeautifulSoup(src, "lxml")
                master_data = soup.find_all("div", {"class": "feed-shared-update-v2"})
                info = soup.find_all("div", {"class": "feed-shared-actor__meta"})
                post_obj = {}
                Name = (
                    master_data[0]
                    .find_all("div", {"class": "feed-shared-actor__meta relative"})[0]
                    .find("span", {"dir": "ltr"})
                    .get_text()
                    .strip()
                )
                post_obj["Name"] = Name
                Post_Designation = (
                    master_data[0]
                    .find_all("span", {"class": "feed-shared-actor__description"})[0]
                    .get_text()
                    .strip()
                )
                Content = (
                    master_data[0]
                    .find_all(
                        "div", {"class": "feed-shared-update-v2__description-wrapper"}
                    )[0]
                    .get_text()
                    .strip()
                )
                post_obj["Content"] = Content
                # print(Post)
                post_obj["Post_Designation"] = Post_Designation
                # print(Content)
                Profile_URL = (
                    master_data[0]
                    .find(
                        "div",
                        {
                            "class": "feed-shared-actor display-flex feed-shared-actor--with-control-menu"
                        },
                    )
                    .find(
                        "a",
                        {
                            "class": "app-aware-link feed-shared-actor__container-link relative display-flex flex-grow-1"
                        },
                    )
                )
                Profile_URL = str(Profile_URL)
                start_index = 179
                end_index = Profile_URL.find('"', start_index)
                Profile_URL = Profile_URL[start_index:end_index]
                post_obj["Profile_URL"] = Profile_URL
                a.append(post_obj)
            except:
                pass
print(
    "$$$$$$$$$$$$$$$$$$$$$$$$$*******************************************************************$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
)
#print(len(a))
# Filter the posts -- to do
maxLen=300 #max length to consider for classification
clf_nb = pickle.load(open('model_nb.sav', 'rb'))
clf_lr=pickle.load(open('model_lr.sav','rb'))
clf_dt= pickle.load(open('model_dt.sav', 'rb'))
clf_svc = pickle.load(open('model_svc.sav', 'rb'))
word_to_index, index_to_word, word_to_vec_map = read_glove_vecs('glove.6B.50d.txt')
text_to_filter=[]
for i in range(len(a)):
    text_to_filter.append(a[i]['Content'])
text_to_filter=np.array(text_to_filter)
for i in range(len(text_to_filter)):
    text_to_filter[i]=remove_stopwords(text_to_filter[i].lower())
for i in range(len(text_to_filter)):
    text_to_filter[i]=remove_special_characters(str(text_to_filter[i]))
text_converted = sentences_to_indices(text_to_filter, word_to_index, max_len = maxLen)
pred_lr=clf_lr.predict(text_converted)
pred_DT=clf_dt.predict(text_converted)
pred_svc =clf_svc.predict(text_converted)
pred_nb=clf_nb.predict(text_converted)
pred_tot=[sum(x) for x in zip(3*pred_lr,pred_DT,pred_svc,pred_nb)]
pred=[int(x>1) for x in pred_tot]
filtered_posts=[]
for i in range(len(pred)):
    if pred[i]==1:
        filtered_posts.append(a[i])

# Write to file
df = pd.DataFrame(filtered_posts)
df.index = np.arange(1, len(df) + 1)
filename = f"Linked_Data_Leads_{timestamp}.xlsx"
df.to_excel(filename, sheet_name="sheet1")

