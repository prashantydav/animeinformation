# importing required libraries (bs4 , requests , openpyxl) 
from bs4 import BeautifulSoup
import requests
import openpyxl


# this class defines method for scrapping of data 
class AnimeManga:
    # this method will scrape the list of all genre with their links
    def get_genre():
        lname = []
        link = []
        url = requests.get("https://myanimelist.net/anime.php")  
        soup = BeautifulSoup(url.content , 'lxml')
        genre_link = soup.find_all('div' , class_="genre-link")
        genres = genre_link[0].find_all('div' , class_="genre-list al")
        
        for genre in genres:
            name = genre.a.text
            lname.append(name)
            link.append(genre.a['href'])
        
        return lname,link

    
    # this method will take a links of all anime from a specific genre and returns a BeautifulSoup object  
    def getbsoup(aList , choice):
        ptr = 1
        for i in aList:
            if ptr == choice:
                link = "https://myanimelist.net" + i
                print("scrapping: "+link)
                print(type(i))
                url = requests.get("https://myanimelist.net" + str(i))
                soup = BeautifulSoup(url.content,"lxml")
                return soup
            ptr += 1
    

    # this method will take link of first page and and scrape imformation of all the anime from all pages 
    def get_all_list(pagelink):
        mylist = []
        slist = []
        dlist = []
        episodes = []
        ctr = 1
        url = requests.get(pagelink)
        soup2 = BeautifulSoup(url.content , 'lxml')
        ref = soup2.find('a',class_="link-title")
        flag = True
        while(flag):
            
            url1 = requests.get(pagelink + "?page=" + str(ctr))
            soup2 = BeautifulSoup(url1.content , 'lxml')
            ref = soup2.find_all('a',class_="link-title")
            stitle = soup2.find_all('span',class_="producer")
            episode = soup2.find_all('div',class_="eps")
            disc = soup2.find_all("span",class_="preline")

            if not ref:
                break
                
            for i in ref:
                mylist.append(i.text)
            
            for i in stitle:
                sn = i.a
                if sn is None:
                    sn = "not known"
                    slist.append(sn)
                else:
                    slist.append(sn.text)

            for i in episode:
                ep = i.a.span
                episodes.append(ep.text) 

            for i in disc:
                dlist.append(i.text)
            
            print(f'page {ctr} scrapped')         
            ctr += 1

        print('data appended in lists')
        return mylist,slist,episodes,dlist
    

if __name__ == '__main__':

    # making an object of class AnimeManga          
    a = AnimeManga  

    # generating list of all anime on the basis of genre
    print("genre of anime list")
    ctr = 1
    for i in a.get_genre()[0]:
        print(f'{ctr}-{i}')
        ctr+=1
    choice = int(input("enter your choice: "))
    ctr = 1
    filename = ""
    fields = ["name","studio","episodes","discription"]
    row = []
    title = ''
    for i in range(len(a.get_genre()[0])):
        print('searching...')
        
        # taking input of choice from the users
        # user have to input choice in integers
        # 1-Action (4,008)
        # 2-Adventure (3,063)     
        # 3-Cars (136)
        # 4-Comedy (6,224)  
        # for choosing action type 1
        
        if choice == i:
            title = a.get_genre()[0][i-1]
            filename = f'{a.get_genre()[0][i-1]}.xlsx'
            link = "https://myanimelist.net" + a.get_genre()[1][choice - 1]
            print("scrapping "+link)
            l = a.get_all_list(link)
            count = 0
            for i in range(len(l[1])):
                row.append([l[0][i],l[1][i],l[2][i],l[3][i]])
                count+=1
            print(f'{count} rows.')
            break
        ctr+=1

    
# Storing all scrapped data into an excel file
    
    wb = openpyxl.Workbook()

    sheet = wb.active

    sheet.cell(row = 1,column = 1).value = title

    sheet.append(fields)

    
    sheet.column_dimensions['D'].width = 200

    for i in range(len(row)):
        sheet.row_dimensions[i+3].height = 30


    for i in row:
        sheet.append(i)
    wb.save("scrapped data/"+filename)
    print('excel file saved..')


