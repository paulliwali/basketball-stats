from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

# function for extracting college stats
def weird_scrape(mstr, substr):
    cs_tag1, cs_tag2 = '<td class="right " data-stat="', '" >'
    found = mstr.split(cs_tag1 + substr + cs_tag2)[1].split('<')[0]
    return 0 if found == '' else int(found)

# function for extracting hyperlink
def agethref(pl):
    try:
        ret = pl.a.get('href')
    except:
        ret = 'Not Available'
    return ret

# functions for defining isSuccessful
def isAllstar(soup):
    return None != soup.find('div', attrs={'id':'all_all_star'})

def isStarter(soup):
    try:
        Gs = soup.find('tbody').find_all('td',attrs={'data-stat':'g'})
        GSs = soup.find('tbody').find_all('td',attrs={'data-stat':'gs'})
        MPs = soup.find('tbody').find_all('td',attrs={'data-stat':'mp_per_g'})
        Tm = soup.find('tbody').find_all('td',attrs={'data-stat':'team_id'})
    except:
        return False
    try:
        isStar = 'True, True, True' in str([
                 int(GS.text)/int(G.text) > 0.75 or float(MP.text) > 29
                 for G, GS, MP, T in zip(Gs, GSs, MPs, Tm) if T.text != 'TOT'])
    except:
        isStar = 'True, True, True' in str([float(MP.text) > 29 and int(G.text) > 20
                 for G, MP, T in zip(Gs, MPs, Tm) if T.text != 'TOT'])
    return isStar

# Get College Pace stats. Returns an array
def get_col_pace(soup):
    colsum = soup.body.find('div', attrs={'id':'meta'})
    if 'ORtg:' in colsum.text:
        ortg = float(colsum.text.split('ORtg: ')[1].split(' ')[0])
        drtg = float(colsum.text.split('DRtg: ')[1].split(' ')[0])
        ptsg = float(colsum.text.split('PS/G: ')[1].split(' ')[0])
        return [ptsg/ortg * 100, ortg, drtg]
    else:
        tmpace = soup.find('table', attrs={'id':'team_stats'}).tbody.find_all('tr')
        if tmpace == None:
            return 'No Stats Found'
        tFG = int(tmpace[0].find('td',attrs={'data-stat':'fg'}).text or 0)
        tFGA = int(tmpace[0].find('td',attrs={'data-stat':'fga'}).text or 0)
        tFTA = int(tmpace[0].find('td',attrs={'data-stat':'fta'}).text or 0)
        tORB = int(tmpace[0].find('td',attrs={'data-stat':'orb'}).text or 0)
        tDRB = int(tmpace[0].find('td',attrs={'data-stat':'drb'}).text or 0)
        tTRB = int(tmpace[0].find('td',attrs={'data-stat':'trb'}).text or 0)
        tTOV = int(tmpace[0].find('td',attrs={'data-stat':'tov'}).text or 0)
        tPTS = int(tmpace[0].find('td',attrs={'data-stat':'pts'}).text or 0)
        Gms = int(tmpace[0].find('td',attrs={'data-stat':'g'}).text or 0)

        opp = int(len(tmpace)/2)
        opp_ = ''
        try:
            oFG = int(tmpace[opp].find('td',attrs={'data-stat':'fg'}).text or 0)
        except:
            oFG = int(tmpace[opp].find('td',attrs={'data-stat':'opp_fg'}).text or 0)
            opp_ = 'opp_'
        
        oFGA = int(tmpace[opp].find('td',attrs={'data-stat':opp_+'fga'}).text or 0)
        oFTA = int(tmpace[opp].find('td',attrs={'data-stat':opp_+'fta'}).text or 0)
        oORB = int(tmpace[opp].find('td',attrs={'data-stat':opp_+'orb'}).text or 0)
        oDRB = int(tmpace[opp].find('td',attrs={'data-stat':opp_+'drb'}).text or 0)   
        oTRB = int(tmpace[opp].find('td',attrs={'data-stat':opp_+'trb'}).text or 0)
        oTOV = int(tmpace[opp].find('td',attrs={'data-stat':opp_+'tov'}).text or 0)
        oPTS = int(tmpace[opp].find('td',attrs={'data-stat':opp_+'pts'}).text or 0)

        (tORB, tDRB) = (tORB, tDRB) if tORB != 0 else (0.3*tTRB, 0.7*tTRB)
        (oORB, oDRB) = (oORB, oDRB) if oORB != 0 else (0.3*oTRB, 0.7*oTRB)
        poss = 0.5*((tFGA + 0.4*tFTA - 1.07*(tORB/(tORB + oDRB))*(tFGA - tFG) 
               + tTOV) + (oFGA + 0.4*oFTA - 1.07*(oORB / (oORB + tDRB))
               *(oFGA - oFG) + oTOV)) / Gms
        return [poss, tPTS/Gms/poss * 100, oPTS/Gms/poss * 100]
    

# MAIN #######################################################################
# inputs
##############################################################################
start_year = 2018
end_year = 2018
pl_per = 30
base_url = 'https://www.basketball-reference.com'
base_url2 = 'https://www.sports-reference.com/cbb/schools/'

cs_cats = ['mp','fg','fga','fg3','fg3a','ft','fta','orb','trb',
           'ast','stl','blk','tov','pf','pts']
data = []
data.append(('Draft','Pick','Player Name','IsSuccessful','Height','Weight',
             'MP','FG','FGA','3P','3Pa','FT','FTA','ORB','TRB','AST',
             'STL','BLK','TOV','PF','PTS','All Star','Starter3','College Pace','OffRtg','DefRtg'))
#data.append(('Draft','Pick','Player Name','College Pace','OffRtg','DefRtg'))

random_col = {'University of California, Los Angeles':'ucla',
              'California State University, Fresno':'fresno-state',
              'St. John\'s University':'st-johns-ny',
              'University of North Carolina at Charlotte':'charlotte',
              'Austin Peay State University':'austin-peay',
              'University of Miami':'miami-fl',
              'University of Illinois at Urbana-Champaign':'illinois',
              'Boston College':'boston-college',
              'University of Nevada, Reno':'nevada',
              'Indiana University-Purdue University Indianapolis':'iupui'}

# Prepare dictionary of college name : hyperlink
soup = BeautifulSoup(urlopen(base_url2),'html.parser')
allcols = soup.find_all('td', attrs={'data-stat':'school_name'})
colurls = [agethref(col) for col in allcols]
colnames = [col.text for col in allcols]
col_dict = dict(zip(colnames, colurls))

# loop through years
for year in range(start_year, end_year + 1):
    year_page = base_url + '/draft/NBA_' + str(year) + '.html'

    # Extract Drafted Players
    # query the website and return the html to the variable ‘page’
    page = urlopen(year_page)

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    allpls = soup.find_all('td', attrs={'data-stat':'player'},
                           limit = pl_per)

    plnames = [pl.text for pl in allpls]
    plurls = [agethref(pl) for pl in allpls]
    
    allcols = soup.find_all('td', attrs={'data-stat':'college_name'},
                            limit = pl_per)
    plcols = [col.text for col in allcols]

    # loop through players
    pl_pick = 0
    for plname, plurl, plcol in zip(plnames, plurls, plcols):

        if plcol == '':
            pl_pick += 1
            data.append(tuple([year, pl_pick, plname] + ['Did Not Attend College']))
            continue
        page = urlopen(base_url + plurl)
        soup = BeautifulSoup(page, 'html.parser')

        # Name
        #pl_name = soup.title.text.split(' Stats')[0]
        pl_name = plname
        pl_pick += 1
        print(year, pl_pick, pl_name, plurl, plcol)

        # Height
        ht_s = soup.find('span',attrs={'itemprop':'height'}).text
        ht = round((int(ht_s[0]) * 12 + int(ht_s[2:])) * 2.54)

        # Weight
        wt_s = soup.find('span',attrs={'itemprop':'weight'}).text
        wt = round(int(wt_s[:-2]) * 0.453592)

        # College stats (cs) (weird scrape)
        col_html = soup.find('div',attrs={'id':'all_all_college_stats'})
        if col_html != None:            
            cs_str = col_html.contents[5].split('<tfoot>',1)[1] #maybe not 5?
            col_stats = [weird_scrape(cs_str, cat) for cat in cs_cats]
        else:
            col_stats = [0] * len(cs_cats)

        # Success
        allstar = int(isAllstar(soup))
        starter = int(isStarter(soup))
        suc = allstar if pl_pick < 15 else starter

        # College Pace, OffRtg, DefRtg, NetRtg Based on
        # inputs(Draft Year, Player Name, College Name)        
        if plcol in random_col:
            col_str = random_col[plcol]
        else:
            col_str = plcol.lower().replace('university of ','')\
                  .replace(' university','').replace('.','')\
                  .replace(' college','').replace('college of ','')\
                  .replace(',','').replace('& ','').replace(' at austin','')\
                  .replace(' amherst','').replace(' at','').replace('\'','')\
                  .replace(' institute of technology',' tech').replace('&','')\
                  .replace(' ','-')

        col_pace = [0, 0, 0]
        for col_yr in range(4):
            try:
                page2 = urlopen(base_url2 + col_str + '/' + str(year - col_yr)
                                + '.html')
                soup2 = BeautifulSoup(page2, 'html.parser')
            except:
                col_pace = ['College Not Found'] if col_yr == 0 else col_pace
                break
            else:
                colteam = soup2.find_all('th',attrs={'data-stat':'player'},
                                         limit = 16)
                teammates = [mate.text for mate in colteam]
                if pl_name in teammates or {pl_name.replace('Wesley','Wes'),
                                        pl_name.replace('MarShon','Marshon'),
                                        pl_name.replace(' Jr.',''),
                                        pl_name.replace(' Jr',''),
                                        pl_name + ' Jr.',
                                        pl_name + ' Jr',
                                        pl_name.replace('.','')
                                        }.intersection(set(teammates)):
                    col_pace = [a+b for a,b in zip(col_pace, get_col_pace(soup2))]
                    col_yr = 4 if col_yr == 3 else col_yr
                else:
                    # if name not in 1st yr its wrong col. else hes left
                    col_pace = col_pace if col_yr else ['Wrong College Found']
                    break
                    
        col_pace = [round(a/col_yr,1) for a in col_pace] if col_yr else col_pace
       
        # save the data in tuple
        data.append(tuple([year, pl_pick, pl_name, suc, ht, wt] + col_stats
                          + [allstar, starter] + col_pace + [col_str, col_yr]))
        # data.append(tuple([year, pl_pick, pl_name] + col_pace + [col_str, col_yr]))
        
# open a csv file with append, so old data will not be erased
csvn = str(start_year)+'-'+str(end_year)+'Top'+str(pl_per)+'CollegePace.csv'
with open(csvn, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    for d in data:
        writer.writerow(d)