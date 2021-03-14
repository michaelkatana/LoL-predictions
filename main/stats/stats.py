# file that contains the statistics
import utils # contains handy functions
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns




# utils functions for figures:

def setupHeatmap(size=15):
    """ setup parameters for the heatmap """
    img = plt.imread("images/map.png")
    fig, ax = plt.subplots(figsize=(size,size))
    plt.axis('off')

    ax = plt.gca()
    return img,fig,ax



def saveImage(imagename):
    """ saves the figure to file """
    plt.savefig('images/'+imagename+'.png', bbox_inches='tight')
    
    

    

############# HEATMAPS PLOTS ##############

def genHeatmap_allpositions(posdf, save=False, imgname=''):
    """ generate heatmap for all positions and optionally save to file """
    img,fig,ax = setupHeatmap()

    sns.kdeplot(posdf.x, posdf.y, 
                cmap='inferno', shade=True, 
                shade_lowest=False, cut=5, 
                ax=ax, alpha=0.7,bw=300)
    
    ax.imshow(img, extent=[0, 15000, 0, 15000])
    ax.grid(b=True, which='major', color='#666666', linestyle='-')
    if save:
        saveImage(imgname+'.png')






def genHeatmap_allTeamPositions(posdfr,posdfb, eventname=None, eventdf=None, bw=300, save=False, imgname=''):
    """ heatmap of all positions for each team
        in: df_red, df_blue, kernel size
        out: image """
    img,fig,ax = setupHeatmap()
    #ax.set_title(title)
    sns.kdeplot(posdfr.x, posdfr.y, 
                color="#eb0000", shade=True, 
                shade_lowest=False, cut=5, ax=ax, 
                alpha=0.7,bw=bw)    
    
    sns.kdeplot(posdfb.x, posdfb.y, 
                color="#1800cc", shade=True, 
                shade_lowest=False, cut=5, 
                ax=ax, alpha=0.7,bw=bw)
    
    if(eventdf is not None):   
        sns.kdeplot(eventdf[eventdf.team=='red'].x, 
                    eventdf[eventdf.team=='red'].y, 
                    color='#eb9d00', shade=True, 
                    shade_lowest=False, cut=5, 
                    ax=ax, alpha=0.7,bw=bw)
        
        sns.kdeplot(eventdf[eventdf.team=='blue'].x, 
                    eventdf[eventdf.team=='blue'].y, 
                    color='#00c0eb', shade=True, 
                    shade_lowest=False, cut=5, 
                    ax=ax, alpha=0.7,bw=bw)
        
    ax.imshow(img, extent=[0, 15000, 0, 15000])
    ax.grid(b=True, which='major', color='#666666', linestyle='-')
    if save:
        saveImage(imgname+'.png')
    if save and (eventname is not None):
        saveImage(imgname+'_'+eventname+'.png')
    



def genHeatmap_allTeamPositions_withEvent(posdfr,posdfb, eventname=None, eventdf=None, bw=300, save=False, imgname=''):
    """ heatmap of all positions for each team
        in: df_red, df_blue, kernel size
        out: image """
    img,fig,ax = setupHeatmap()
    #ax.set_title(title)
    sns.scatterplot(posdfr.x, posdfr.y, color="#eb0000", ax=ax)    
    sns.scatterplot(posdfb.x, posdfb.y, color="#1800cc", ax=ax)
    
    if(eventdf is not None):   
        sns.kdeplot(eventdf[eventdf.team=='red'].x, 
                    eventdf[eventdf.team=='red'].y, 
                    color='#eb9d00', shade=True, 
                    shade_lowest=False, cut=5, 
                    ax=ax, alpha=0.7,bw=bw)
        
        sns.kdeplot(eventdf[eventdf.team=='blue'].x, 
                    eventdf[eventdf.team=='blue'].y, 
                    color='#00c0eb', shade=True, 
                    shade_lowest=False, cut=5, ax=ax, 
                    alpha=0.7,bw=bw)
        
    ax.imshow(img, extent=[0, 15000, 0, 15000])
    ax.grid(b=True, which='major', color='#666666', linestyle='-')
    if save:
        saveImage(imgname+'.png')
    if save and (eventname is not None):
        saveImage(imgname+'_'+eventname+'.png')

