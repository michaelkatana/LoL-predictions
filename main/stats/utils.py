"""

collection of all the functions to perform specialized tasks:

1. save and load generic data with pickle
2. get the ids of all games in the database
3. get the json of a single match given its id
4. 

"""
import pickle

# save and load file:

def save_obj(obj, name ):
    """ save object to file with python in binary format """ 
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, 0)


def load_obj(name):
    """ load a file in binary format from path=name with pickle """
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
    
    



def listDict_to_dictList(listDict):
    """ returns a dict of lists from a list of dicts """
    dictList = {}
    for cli in listDict:
        for k,v in cli.items():
            if k not in dictList.keys():
                dictList[k] = [v]
            else:
                dictList[k].append(v)
    return dictList






################## get the players positions -no event type- ##################
# 1. get all player ids with an absolute position in each timeframe
# 2. for each player id, get the list of positions
# 3. store all players' positions


def getPlayerIds(timelines_frames):
    """ gets the playerIds 
        returns a list of player ids for which the position is recorded"""
    playerIds = []
    for frame in timelines_frames:
        playerIds.extend(frame['participantFrames'].keys())
    return [str(pl) for pl in sorted(list(set([int(p) for p in playerIds])))]



# get the positions for a single player in a match
def getPosition(player,timelines_frames):
    """ get the positions for a single player in a match
    timelines_frames: g['timeline']['frames']
    """
    xs = []
    ys = []
    ts = []
    for frame in timelines_frames:
        if 'position' in frame['participantFrames'][player]:
            position = frame['participantFrames'][player]['position']
            timestamp = frame['timestamp']
            xs.append(position['x'])
            ys.append(position['y'])
            ts.append(timestamp)
    return xs,ys,ts




# def get positions of the players from a match:
def getAllPlayersPositions(game, playerIds):
    """ get all players positions and returns the positions and the relative playerId
        game: a single game
        playerIds: list of player ids for which to extract their position 
        
        returns: a list of tuples with values:
            p: playerId
            xs: X coordinates
            ys: Y coordinates
            ts: timestamp
    """
    xs,ys,ts = [],[],[]
    positions = []
    for p in playerIds:
        xs,ys,ts = getPosition(p,game['timeline']['frames'])
        positions.append((p,xs,ys,ts))
    return positions





def dataFramefromAllPositions(playerpositions,playerids):
    import pandas as pd
    """ transform the list of playerids, xcoord and ycoord into dataframe
        returns a dataframe with columns: playerid, x, y"""
    poslist = []
    for plid in playerids:
        plid = int(plid)-1
        dictpos_ = {'playerid':[playerpositions[plid][0]]*len(playerpositions[plid][1]),
                    'x':playerpositions[plid][1],
                    'y':playerpositions[plid][2],
                    'timestamp': playerpositions[plid][3]}
        poslist.append(pd.DataFrame(dictpos_))

    posdataframe = pd.concat(poslist)
    return posdataframe






# extract contextual info about the players in each timestamp
def getPlayersGlobalStats(game,playerids,contextinfo = ['currentGold','totalGold','level','xp','minionsKilled','jungleMinionsKilled','dominionScore']):
    """
    from the playerids of a single match
    returns a list of statuses for each player for each timestamp
    """
    allcontextslist = list()
    

    for frame in game['timeline']['frames']:
        contextdict = {}

        for pid in playerids:
            contextdict['p'] = pid
            contextdict['timestamp'] = frame['timestamp']
            #contextdict['x'] = frame['participantFrames'][pid]['position']['x']
            #contextdict['y'] = frame['participantFrames'][pid]['position']['y']
            for c in contextinfo:

                if(c in frame['participantFrames'][pid]):
                    contextdict[c] = frame['participantFrames'][pid][c]

                else:
                    contextdict[c] = 0
            allcontextslist.append(contextdict.copy())
    return allcontextslist





def getGameEventsSequences(game, playername = ['participantId','creatorId','killerId']):

    """ for a game, extract all player positions and the relative event
        returns: a list of dictionaries """
    allevents = []
    for frame in game['timeline']['frames']:


        eventsdict = {}
        for event in frame['events']:

            # get the playerid
            for k in playername: # loop the player name list
                if(k in event):
                    if (event[k] in range(1,11)): # there is an error in the playerid assigned at an event, is 0
                        playerid = str(event[k]) # get the playerId

            # get the position of the player in that frame
            if 'position' in frame['participantFrames'][playerid]:
                position = frame['participantFrames'][playerid]['position']            



            eventsdict = {'playerId': playerid,
                          'eventtype': event['type'],
                         'x': position['x'],
                         'y': position['y'],
                         'timestamp': event['timestamp']//60000,
                         'gametimestamp': frame['timestamp']}


            allevents.append(eventsdict.copy())
    return allevents     