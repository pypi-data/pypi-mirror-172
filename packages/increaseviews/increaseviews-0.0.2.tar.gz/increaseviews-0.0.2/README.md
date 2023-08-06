# IncreaseViews
A python package that can be used to increase the views of any youtube channel.

This python package cab be used to increase youtube views of any channel by automating the web browser.

All the functions in the module are:-

use_chrome(path,link,repetition,sleeptime_1,sleeptime_2)

use_edge(path,link,repetition,sleeptime_1,sleeptime_2)

chr_morethanone(path,number_of_videos,link_list,repetition,sleeptime_1,sleeptime_2)

edge_morethanone(path,number_of_videos,link_list,repetition,sleeptime_1,sleeptime_2)



parameters:

path -> path where your webdriver is in 

link -> link of the video that you need to increase the views of

repetition -> number of views you need to increase

sleeptime_1 and sleeptime_2 -> your video will repeat after random second

number_of_videos -> number of videos that you need to increase views of

link_list -> the links of all the videos that you need to increase the views of. Remember to put the link inside python list



Code Example:

    from increaseviews import *

    use_chrome("D:\system\chromedriver_win32\chromedriver","https://www.youtube.com/watch?v=R-PO2xeyNI8",1000,10,20) 

    use_edge("D:\system\edgedriver_win64\msedgedriver","https://www.youtube.com/watch?v=R-PO2xeyNI8",1000,10,20) 

    chr_morethanone("D:\system\chromedriver_win32\chromedriver", 2, ['https://www.youtube.com/watch?v=8iqL7yVU2Y4','https://www.youtube.com       /watch?v=pHh8ef2bdEI'], 3, 5, 10)

    edge_morethanone("D:\system\edgedriver_win64\msedgedriver", 2, ['https://www.youtube.com/watch?v=8iqL7yVU2Y4','https://www.youtube.com/watch?v=pHh8ef2bdEI'], 3, 5, 10)

