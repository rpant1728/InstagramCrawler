import sys, re, os, selenium, time, getpass, json, argparse
from time import sleep
from urllib.request import urlopen, urlretrieve
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from collections import OrderedDict

profile = dict()  

class InstagramCrawler(object):
    def __init__(self, headless=True):
        options = Options()
        if headless:
            options.add_argument("--headless")
        self.driver = webdriver.Firefox(firefox_options=options)
        self.baseURL = "https://www.instagram.com"
        self.authURL = self.baseURL + '/accounts/login/'

    def login(self, authentication):
        driver = self.driver
        with open(authentication,"r") as f:
            data = f.read()
            auth_dict = json.loads(data)
            if(auth_dict['username'] == "" or auth_dict['password'] == ""):
                print("Please enter your Instagram credentials in 'auth.json' file")
            else:
                my_username =  auth_dict['username']
                my_password = auth_dict['password']

        # my_username = input("Enter your Username : ")
        # my_password = getpass.getpass("Enter your Password : ")

        driver.get(self.authURL)
        sleep(5)

        inp_username = driver.find_element(By.NAME, "username")
        inp_password = driver.find_element(By.NAME, "password")

        inp_username.send_keys(my_username)
        inp_password.send_keys(my_password)

        driver.find_element_by_css_selector("._5f5mN").click()
        sleep(5)

    def getDetails(self, query, profile_url, directory):
        driver = self.driver
        name = driver.find_element(By.CLASS_NAME, "rhpdm").text
        details = driver.find_elements(By.CLASS_NAME, "g47SY")
        posts_count = details[0].text
        followers_count = details[1].get_attribute("title")
        following_count = details[2].text 
        prof_pic = driver.find_element(By.CSS_SELECTOR, "._6q-tv").get_attribute("src")
        urlretrieve(prof_pic, directory + "/ProfilePicture.jpg")
        print("Name : " + name)    
        print("Posts : " + posts_count)
        print("Followers : " + followers_count)
        print("Following : " + following_count)
        profile = {
            'username' : query,
            'name' : name,
            'details' : details,
            'posts_count' : posts_count,
            'followers_count' : followers_count,
            'following_count' : following_count
        }
        if(driver.find_element_by_css_selector(".-vDIg > span:nth-child(3)")):
            description = driver.find_element_by_css_selector(".-vDIg > span:nth-child(3)").text
            profile['description'] = description
            print("Description : " + description)

        return posts_count, followers_count, following_count

    def get_followers(self, followers_count, profile_url):
        driver = self.driver
        followers = list()
        driver.find_element(By.CSS_SELECTOR, "li.Y8-fY:nth-child(2) > a:nth-child(1)").click()
        sleep(2)
        scroll_downs = int(int(followers_count)/5) 
        for i in range(scroll_downs):
            followers_list = driver.find_elements(By.CSS_SELECTOR, ".zsYNt")
            driver.find_element_by_css_selector(".j6cq2").send_keys(Keys.PAGE_DOWN)
            sleep(1)
            for follower in followers_list:
                if follower.text not in followers:
                    followers.append(follower.text)
        
        profile['followers'] = followers
        driver.get(profile_url)

    def get_following(self, following_count, profile_url) :
        driver = self.driver
        following = list()
        driver.find_element(By.CSS_SELECTOR, "li.Y8-fY:nth-child(3) > a:nth-child(1)").click()
        sleep(2)
        scroll_downs = int(int(following_count)/5)
        for i in range(scroll_downs):
            following_list = driver.find_elements(By.CSS_SELECTOR, ".zsYNt")
            driver.find_element_by_css_selector(".j6cq2").send_keys(Keys.PAGE_DOWN)
            sleep(1)
            for person_following in following_list:
                if person_following.text not in following:
                    following.append(person_following.text)

        profile['following'] = following
        driver.get(profile_url)

    def get_post_urls(self, query, post_count):
        post_urls = list()
        driver = self.driver
        scroll_downs = int(int(post_count)/12+1)
        
        for i in range(scroll_downs):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(5)
            eles = driver.find_elements(By.CSS_SELECTOR, '.v1Nh3 a')
            for ele in eles:
                post = ele.get_attribute('href')
                if post not in post_urls:
                    post_urls.append(post)

        return post_urls        

    def get_post_details(self, query, post_urls, directory, post_dir, number): 
        driver = self.driver
        post_dict = OrderedDict()
        num = 0
        for post in post_urls:
            num = num+1
            if(num == number+1):
                break
            image = list()
            comments = list()
            tagged_people = list()
            driver.get(post)
            driver.find_element(By.CSS_SELECTOR, "._97aPb > div:nth-child(1)").click()
            sleep(1)

            if(driver.find_elements_by_css_selector(".gElp9 > span:nth-child(2)")):
                caption = driver.find_element(By.CSS_SELECTOR, ".gElp9 > span:nth-child(2)").text
            else: 
                caption = "" 

            if(driver.find_elements_by_css_selector(".TlrDj")):
                commenters = driver.find_elements_by_css_selector(".TlrDj")
                comms = driver.find_elements_by_css_selector("li.gElp9 > span:nth-child(2)")
                for commenter, comm in zip(commenters, comms):
                    comment = {
                        'commenter' : commenter.text,
                        'comment' : comm.text,                   
                    }
                    comments.append(comment)

            if(driver.find_elements_by_css_selector(".JYWcJ")):           
                tagged = driver.find_elements_by_css_selector(".JYWcJ")
                tagged_urls = list()
                for person in tagged:
                    if person.get_attribute('href') not in tagged_urls:
                        tagged_urls.append(person.get_attribute('href')) 
                for tagged_url in tagged_urls:
                    driver.get(tagged_url)
                    if(driver.find_element(By.CLASS_NAME, "rhpdm")):
                        tagged_person = driver.find_element(By.CLASS_NAME, "rhpdm").text
                    driver.get(post)
                    tagged_people.append(tagged_person)

            if(driver.find_elements_by_css_selector(".coreSpriteRightChevron")):
                while(driver.find_elements_by_css_selector(".SWk3c") or driver.find_elements_by_css_selector(".coreSpriteRightChevron")):
                    if(driver.find_elements(By.CLASS_NAME, "FFVAD")):
                        image.append(driver.find_element(By.CLASS_NAME, "FFVAD").get_attribute("src"))
                    elif(driver.find_elements(By.CSS_SELECTOR, ".tWeCl")):
                        image.append(driver.find_element(By.CSS_SELECTOR, ".tWeCl").get_attribute("src"))                    
                    if(driver.find_elements_by_css_selector(".coreSpriteRightChevron")):
                        driver.find_element_by_css_selector(".coreSpriteRightChevron").click()
                    else:
                        break    
            else:        
                if(driver.find_elements(By.CLASS_NAME, "FFVAD")):
                        image.append(driver.find_element(By.CLASS_NAME, "FFVAD").get_attribute("src"))
                elif(driver.find_elements(By.CSS_SELECTOR, ".tWeCl")):
                    image.append(driver.find_element(By.CSS_SELECTOR, ".tWeCl").get_attribute("src"))   

            if(driver.find_elements_by_css_selector(".O4GlU")):
                location = driver.find_element(By.CSS_SELECTOR, ".O4GlU").text
                names = re.findall(r'[A-Za-z]+', location)
                for name in names:
                    location = name
                    break
                if(location == "Indian"):
                    location = "India"
            else:
                location = "" 

            date = driver.find_element(By.CSS_SELECTOR, "._1o9PC").get_attribute('title')

            if(driver.find_elements(By.CSS_SELECTOR, ".zV_Nj > span:nth-child(1)")):
                likes = driver.find_element(By.CSS_SELECTOR, ".zV_Nj > span:nth-child(1)").text
            elif(driver.find_elements(By.CSS_SELECTOR, ".cqXBL")):
                likes = len(driver.find_elements(By.CSS_SELECTOR, ".cqXBL"))

            self.save_and_download(num, query, post, caption, likes, date, location, image, comments, tagged_people, post_dir, post_dict)
        return post_dict
            
            
    def save_and_download(self, num, query, post, caption, likes, date, location, image, comments, tagged_people, post_dir, post_dict):
        driver = self.driver 
        post_dict[post] = {
            'caption' : caption.split('#')[0].replace("\n", " ").replace("""\"""", " "), 
            'likes' :  likes,
            'month' : date.split(' ')[0],
            'date' : date.split(' ')[1].split(',')[0],
            'year' : date.split(' ')[2],    
            'time' : driver.find_element(By.CSS_SELECTOR, "._1o9PC").get_attribute('datetime').split('T')[1].split('.')[0],
            'location' : location,
            'images' : len(image),
            'creator' : query,
            'comments' : comments,
            'tagged_people' : tagged_people
        }
        num1 = 0
        for img in image:
            if(len(image) > 1):
                num1 = num1 + 1
                if ".mp4" in img:
                    urlretrieve(img, post_dir + "/" + str(num) + "_" + str(num1) + ".mp4")
                else:
                    urlretrieve(img, post_dir + "/" + str(num) + "_" + str(num1) + ".jpg")
            else:
                if ".mp4" in img:
                    urlretrieve(img, post_dir + "/" + str(num) + ".mp4")
                else:
                    urlretrieve(img, post_dir + "/" + str(num) + ".jpg")
            

    def make_directories(self, query, directory):
        direct = os.path.dirname(os.path.join(directory, query))
        if not os.path.exists(direct):
            os.makedirs(direct)
        else:
            direct = os.path.join(directory, query)  

        post_dir = os.path.dirname(os.path.join(direct, "Posts"))
        if not os.path.exists(post_dir):
            os.makedirs(post_dir)
        else:
            post_dir = os.path.join(direct, "Posts")

        return direct, post_dir

    def load_data(self, directory):
        data = json.dumps(profile)
        with open(os.path.join(directory, "profile.json"), "w") as f:
            f.write(data)

    def crawl(self, authentication, query, crawl_type, number, profile_status, directory):
        driver = self.driver
        direct, post_dir = self.make_directories(query, directory)
        profile_url = self.baseURL + "/" + query
        if(profile_status == "private"):
            self.login(authentication)
        driver.get(profile_url)
        post_count, followers_count, following_count = self.getDetails(query, profile_url, direct)
        if "," in post_count:
            post_count = post_count.split(',')[0]+post_count.split(',')[1]
        if(crawl_type == "followers" or crawl_type == "all"):
            self.get_followers(followers_count, profile_url)
        if(crawl_type == "following" or crawl_type == "all"):
            self.get_following(following_count, profile_url)
        if(crawl_type == "posts" or crawl_type == "all"):
            if(number == -1):
                number = post_count
            post_urls = self.get_post_urls(query, post_count) 
            post_dict = self.get_post_details(query, post_urls, direct, post_dir, number)
            profile['posts'] = post_dict
        self.load_data(directory)

def main():
    parser = argparse.ArgumentParser(description='Instagram Crawler')
    parser.add_argument('-q', '--query', type=str, default='instagram', help="Username of target to be crawled")
    parser.add_argument('-a', '--authentication', type=str, default='./auth.json', help='Path to authentication json file')
    parser.add_argument('-t', '--crawl_type', type=str, default='posts', help="Options: 'details' | 'posts' | 'followers' | 'following' | 'all'")
    parser.add_argument('-n', '--number', type=int, default=0, help='Number of posts to download: integer, -1 to download all')
    parser.add_argument('-p', '--profile_status', type=str, default='public', help="Options: 'public' | 'private'")
    parser.add_argument('-d', '--directory', type=str, default='./Profiles/', help='Directory to save results')
    parser.add_argument('-l', '--headless', action='store_true', help='If set, script will be run headless')
    args = parser.parse_args()
    crawler = InstagramCrawler(headless=args.headless)
    crawler.crawl(authentication=args.authentication, 
                  query=args.query,
                  crawl_type=args.crawl_type,
                  number=args.number,
                  profile_status=args.profile_status,
                  directory=args.directory)

if __name__ == "__main__":
    main()






   


            