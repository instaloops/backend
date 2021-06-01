from django.db import models
from django.contrib.auth.models import User
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import os
import datetime
import random
import pytz


class Niche(models.Model):
    name = models.CharField(max_length=56)

    def __str__(self):
        return self.name


class Influencer(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    min_budget = models.PositiveIntegerField(default=0)
    max_budget = models.PositiveIntegerField()
    niche = models.ForeignKey(to=Niche, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to="Influencer/Pic/", blank=True, null=True)
    banner = models.ImageField(upload_to="Influencer/Banner/", blank=True, null=True)
    bio = models.CharField(max_length=64, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(default=0, blank=True, null=True)
    insta_username = models.CharField(max_length=54, blank=True, null=True)
    insta_posts = models.CharField(max_length=6, blank=True, null=True)
    insta_followers = models.CharField(max_length=6, blank=True, null=True)
    insta_following = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def username(self):
        return self.user.username

    def email(self):
        return self.user.email

    def reviews(self):
        return Review.objects.filter(influencer__pk=self.pk)

    def review_count(self):
        return Review.objects.filter(influencer__pk=self.pk).count()

    def ig_scrape(self):
        pass
        '''
            Selenium webdriver is not working on heroku...
            just need to fix the driver rest code is working fine.
        '''
        # if not self.insta_username:
        #     return None
        # options = Options()
        # options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
        #
        # options.add_argument("--headless")
        # options.add_argument('--disable-gpu')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--remote-debugging-port=9222')
        #
        # driver = webdriver.Chrome(
        #     executable_path=str(os.environ.get('CHROMEDRIVER_PATH')),
        #     chrome_options=options
        # )
        # driver.get(f"https://www.instagram.com/{self.insta_username}/")
        # posts = driver.find_element_by_xpath(
        #     "/html/body/div[1]/section/main/div/header/section/ul/li[1]/a/span").text
        # followers = driver.find_element_by_xpath(
        #     "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span").text
        # following = driver.find_element_by_xpath(
        #     "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span").text
        # self.insta_posts = posts
        # self.insta_following = following
        # self.insta_followers = followers
        # self.save()
        # driver.quit()
        # return [posts, following, followers]


    # def get_insta_posts(self):
    #     if not self.insta_username:
    #         return None
    #     return self.ig_scrape()[0]
    #
    # def get_insta_following(self):
    #     if not self.insta_username:
    #         return None
    #     return self.ig_scrape()[1]
    #
    # def get_insta_followers(self):
    #     if not self.insta_username:
    #         return None
    #     return self.ig_scrape()[2]


class Consumer(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to="Consumer/pic/", blank=True, null=True)

    def __str__(self):
        return self.user.username


class Review(models.Model):
    consumer = models.ForeignKey(
        to=Consumer, on_delete=models.CASCADE, blank=True, null=True
    )
    influencer = models.ForeignKey(to=Influencer, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def consumer_username(self):
        return self.consumer.user.username


class Order(models.Model):
    influencer = models.ForeignKey(to=Influencer, on_delete=models.CASCADE)
    consumer = models.ForeignKey(to=Consumer, on_delete=models.CASCADE)
    accepted_amount = models.FloatField()
    date_created = models.DateTimeField(auto_created=True)
    is_accepted = models.BooleanField(default=False)
    has_responded = models.BooleanField(default=False)

    def __str__(self):
        return self.influencer.user.username


class SubOrder(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    title = models.CharField(max_length=24)
    subject = models.TextField()
    price = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.order.consumer.user.username


def makehex():
    return hex(random.randint(2863311530, 4294967295)).replace("0x", "")


class Token(models.Model):
    token = models.CharField(max_length=12, default=makehex)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        now = datetime.datetime.now(tz=pytz.UTC)
        return now.day == self.datetime.day and now.hour - self.datetime.hour <= 1
