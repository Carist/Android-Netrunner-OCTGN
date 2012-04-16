Advance = ("Advance", "73b8d1f2-cd54-41a9-b689-3726b7b86f4f")
Bits = ("Bits", "19be5742-d233-4ea1-a88a-702cfec930b1")
Scored = ("Scored", "10254d1f-6335-4b90-b124-b01ec131dd07")
Not_rezzed = ("Not rezzed", "8105e4c7-cb54-4421-9ae2-4e276bedee90")
#Derezzed = ("Derezzed", "ae34ee21-5309-46b3-98de-9d428f59e243")
Trace_value = ("Trace value", "01feb523-ac36-4dcd-970a-515aa8d73e37")
Link_value = ("Link value", "3c429e4c-3c7a-49fb-96cc-7f84a63cc672")
PlusOne= ("+1", "aa261722-e12a-41d4-a475-3cc1043166a7")
MinusOne= ("-1", "48ceb18b-5521-4d3f-b5fb-c8212e8bcbae")
#---------------------------------------------------------------------------
# Global variables
#---------------------------------------------------------------------------
ds = ""
global TurnAutomation
TraceValue = 0

turnIdx = 0
DifficultyLevels = { }

TypeCard = {}

MemoryRequirements = { }
InstallationCosts = { }
ileActions = {'Runr': 4, 'Corp': 3}
#---------------------------------------------------------------------------
# Constants
#---------------------------------------------------------------------------
import re

turns = [
	'Start of Game',
	"It is now Corporation's Turn",
	"It is now Runner's Turn",
	"It is now End of Turn"]

ScoredColor = "#009900"
SelectColor = "#009900"
MakeRunColor = "#ff0000"

#---------------------------------------------------------------------------
# General functions
#---------------------------------------------------------------------------

def num (s):
   if not s: return 0
   try:
      return int(s)
   except ValueError:
      return 0

#---------------------------------------------------------------------------
# Actions indication
#---------------------------------------------------------------------------

def useAction0(group, x=0, y=0):
	if ( ds == "corp"):
		notify("{} takes the Mandatory draw".format(me))
		drawMany(me.piles['R&D/Stack'],1)

def useAction1(group, x=0, y=0):
	notify("{} takes Action #1".format(me))

def useAction2(group, x=0, y=0):
	notify("{} takes Action #2".format(me))

def useAction3(group, x=0, y=0):
	notify("{} takes Action #3".format(me))

def useAction4(group, x=0, y=0):
	notify("{} takes Action #4".format(me))

def useExtraAction(group, x=0, y=0):
	notify("{} takes an Extra Action".format(me))

#------------------------------------------------------------------------------
# Table group actions
#------------------------------------------------------------------------------

def turnAutomationOff (group,x=0,y=0):
	global TurnAutomation
	notify ("{}'s automations are OFF.".format(me))
	TurnAutomation = -1


def turnAutomationOn (group,x=0,y=0):
	global TurnAutomation
	notify ("{}'s automations are ON.".format(me))
	TurnAutomation = 0

def create3DataForts(group):
	table.create("2a0b57ca-1714-4a70-88d7-25fdf795486f", 0, 0, 1)
	table.create("181de100-c255-464f-a4ed-4ac8cd728c61", 100, 100, 1)
	table.create("59665835-0b0c-4710-99f7-8b90377c35b7", 200, 200, 1)

def intJackin(group, x = 0, y = 0):
	global ds
	ds = ""

	stack = me.piles['R&D/Stack']
	if ( len(stack) == 0):
		whisper ("Please load a deck first!")
		return
	mute()
	TopCard = stack[0]
	TopCard.moveTo(me.piles['Archives'])
	ds = TopCard.Player
	TopCard.moveTo(me.piles['R&D/Stack'])

	if ( checkDeckNoLimit (me.piles['R&D/Stack']) <> 0): notify ("SHOULD RETURN")

	me.counters['Bit Pool'].value =5
	me.counters['Max Hand Size'].value =5
	me.counters['Tags'].value =0
	me.counters['Brain damage'].value =0
	me.counters['Agenda Points'].value =0
	me.counters['Bad Publicity'].value =0
	
	if ds == "corp":
		me.counters['Actions'].value =3
		me.counters['Memory'].value =0
		NameDeck = "R&D"
		create3DataForts(group)
		notify("{} is playing as Corporation".format(me))
		
	else:
		me.counters['Actions'].value =4
		me.counters['Memory'].value =4
		NameDeck = "Stack"
		notify("{} is playing as Runner".format(me))

	table.create("c0f18b5a-adcd-4efe-b3f8-7d72d1bd1db8", 0, 200, 1 ) #trace card

	turnAutomationOn (group,x,y)
	shuffle(me.piles['R&D/Stack'])
	notify ("{}'s {} is shuffled ".format(me,NameDeck) )

	drawMany (me.piles['R&D/Stack'], 5) 

def declare_side(group, x = 0, y = 0):
	global ds
	ds = ""
	if confirm("Are you playing Corporation?") == True:
		ds = "corp"
		notify("{} is playing as Corporation".format(me))
	else:
		ds = "runner"
		notify("{} is playing as Runner".format(me))
	intJackin (group, x = 0, y = 0)

def whoami(group, x = 0, y = 0):
#	whisper("to moje id: {}".format(me._id))
	if ds == "corp":
		whisper("You're playing as Corporation")
	elif ds == "runner":
		whisper("You're playing as Runner")
	else:
		whisper("You did not choose any side yet")

def start_token(group, x = 0, y = 0):
    card, quantity = askCard("[Type] = 'Setup'")
    if quantity == 0: return
    table.create(card, x, y, quantity)

def showCurrentTurn(group, x = 0, y = 0):
    notify(turns[turnIdx])

#def nextTurn(group, x = 0, y = 0):
#	global turnIdx
#	if turnIdx == 3:
#		turnIdx = 1
#	else:
#		turnIdx += 1
#	showCurrentTurn(group)

def goToCsTurn(group, x = 0, y = 0):
	global turnIdx
	turnIdx = 1
	showCurrentTurn(group)
	mute()
	if (ds == "corp" and (me.counters['Actions'].value == 0)):
		me.counters['Actions'].value = ileActions['Corp']

def endOfCsTurn(group, x = 0, y = 0):
	notify("End of Corporation's Turn")

def goToNrTurn(group, x = 0, y = 0):
	global turnIdx
	turnIdx = 2
	showCurrentTurn(group)
	mute()
	if (ds == "runner" and (me.counters['Actions'].value == 0)):
		me.counters['Actions'].value = ileActions['Runr']

def endOfNrTurn(group, x = 0, y = 0):
	notify("End of Runner's Turn")

def goToEndTurn(group, x = 0, y = 0):
	if ( ds == "" ):
		whisper ("choose a side first")
		return
	elif (ds == "corp"): notify ("This is Corporation End of Turn.")
	else: notify ("This is Runner End of Turn.")

	global turnIdx
	turnIdx = 3
	showCurrentTurn(group)

def goToSot (group, x=0,y=0):
	if (ds == "" ):
		whisper ("choose a side first")
		return
	elif (ds == "corp"): notify ("This is Corporation Start of Turn.")
	else: notify ("This is Runner Start of Turn.")


#def addActionsR(group, x = 0, y = 0):
#	ileActions['Runr'] += 1

#def delActionsR(group, x = 0, y = 0):
#	ileActions['Runr'] -= 1

#------------------------------------------------------------------------------
# Run...
#------------------------------------------------------------------------------
def intRun(Name):
	notify ("{} declares a run on {}.".format(me,Name))

def runHQ(group, x=0,Y=0):
	if ds == "runner": intRun("HQ")

def runRD(group, x=0,Y=0):
	if ds == "runner": intRun("R&D")

def runArchives(group, x=0,Y=0):
	if ds == "runner": intRun ("the Archives")

def runSDF(group, x=0,Y=0):
	if ds == "runner": intRun("a subsidiary data fort")

#------------------------------------------------------------------------------
# Tags...
#------------------------------------------------------------------------------
def addTag(group, x = 0, y = 0):
	mute()
	if ds == "runner":
		me.counters['Tags'].value +=1
		notify ("{} gets 1 tag.".format(me))

def pay2andDelTag(group, x = 0, y = 0):
	mute()
	if ds == "runner":
		if me.counters['Tags'].value >= 1:
			me.counters['Tags'].value -=1
			me.counters['Bit Pool'].value -=2
			notify (" {} pays (2) and loose 1 tag.".format(me))
		else: whisper("You don't have any tags")

def delXTag ( group, x=0,Y=0):
	NBTags = me.counters['Tags'].value
	mute()
	if ds == "runner":
		if NBTags >= 1:
			count = askInteger("Remove how many tags?", 1)
			if ( count >= NBTags): count = NBTags

			me.counters['Tags'].value -=count
			notify ("{} removes {} tag(s).".format(me,count))
		else:
			whisper("You don't have any tags")

def addXTag ( group, x=0,Y=0):
	mute()
	if ds == "runner":
		count = askInteger("add how many tags?", 1)
		me.counters['Tags'].value +=count
		notify ("{} gets {} tag(s).".format(me,count))

def delAllTag (group, x=0,Y=0):
	mute()
	if ds == "runner":
		if me.counters['Tags'].value >= 1:
			me.counters['Tags'].value = 0
			notify ( "{} removes all tags.".format(me))
		else:
			whisper("You don't have any tags")
#------------------------------------------------------------------------------
# Markers
#------------------------------------------------------------------------------
def intAddBits ( card, count):
	mute()
	if ( count > 0):
		card.markers[Bits] += count
		if ( card.isFaceUp == True): notify("{} adds {} bits from the bank on {}.".format(me,count,card))
		else: notify("{} adds {} bits on a card.".format(me,count))

def addBits(card, x = 0, y = 0):
	mute()
	count = askInteger("Add how many Bits?", 1)
	intAddBits ( card, count)
	

def remBits(card, x = 0, y = 0):
	mute()
	count = askInteger("Remove how many Bits?", 1)
	if ( count > card.markers[Bits]): count = card.markers[Bits]

	card.markers[Bits] -= count
	if ( card.isFaceUp == True): notify("{} removes {} bits from {}.".format(me,count,card))
	else: notify("{} removes {} bits from a card.".format(me,count))

def remBits2BP (card, x = 0, y = 0):
	mute()
	count = askInteger("Remove how many Bits?", 1)
	if ( count > card.markers[Bits]): count = card.markers[Bits]

	card.markers[Bits] -= count
	me.counters['Bit Pool'].value += count 
	if ( card.isFaceUp == True): notify("{} removes {} bits from {} to Bit Pool.".format(me,count,card))
	else: notify("{} takes {} bits from a card to BitPool.".format(me,count))

def addPlusOne(card, x = 0, y = 0):
	mute()
	card.markers[PlusOne] += 1
	notify("{} adds one +1 marker on {}.".format(me,card))

def addMinusOne(card, x = 0, y = 0):
	mute()
	card.markers[MinusOne] += 1
	notify("{} adds one +1 marker on {}.".format(me,card))
#------------------------------------------------------------------------------
# advancing cards
#------------------------------------------------------------------------------
def advanceCardP(card, x = 0, y = 0):
	mute()
	me.counters['Actions'].value -=1
	me.counters['Bit Pool'].value -=1
	card.markers[Advance] += 1
	if ( card.isFaceUp == True): notify("{} payed 1 and advanced {}.".format(me,card))
	else: notify("{} payed 1 and advanced a card.".format(me))

def addXadvancementCounter(card, x=0, y=0):
	mute()
	count = askInteger("Add how many counters?", 1)
	card.markers[Advance] += count
	if ( card.isFaceUp == True): notify("{} adds {} advancement counters on {}.".format(me,count,card))
	else: notify("{} adds {} advancement counters on a card.".format(me,count))

def delXadvancementCounter(card, x = 0, y = 0):
	mute()
	count = askInteger("Remove how many counters?", 1)
	if ( count > card.markers[Advance] ): count=card.markers[Advance]
	card.markers[Advance] -= count
	if ( card.isFaceUp == True): notify("{} removes {} advancement counters on {}.".format(me,count,card))
	else: notify("{} adds {} advancement counters on a card.".format(me,count))

def advanceCardM(card, x = 0, y = 0):
	mute()
	card.markers[Advance] -= 1
	if ( card.isFaceUp == True): notify("{} removes 1 advancement counter on {}.".format(me,card))
	else: notify("{} removes 1 advancement counter on a card.".format(me))

#---------------------
# Trace
#----------------------

def inputTraceValue (card, x=0,y=0):
	global TraceValue
	if (card.properties['Type'] <> "Tracing"): return
	TraceValue = askInteger("Bet How Many?", 0)
	card.markers[Bits] = 0
	card.isFaceUp = False
	notify ("{} chose a Trace Value.".format(me))
	TypeCard[card] = "Tracing"
	
def revealTraceValue (card, x=0,y=0):
	global TraceValue
	if ( TypeCard[card] <> "Tracing"): return
	mute()
	card.isFaceUp = True
	card.markers[Bits] = TraceValue
	notify ( "{} reveals a Trace Value of {}.".format(me,TraceValue))
	TraceValue = 0

def payTraceValue (card, x=0,y=0):
	if (card.properties['Type'] <> "Tracing"): return
	mute()
	me.counters['Bit Pool'].value -= card.markers[Bits]
	notify ("{} pays {} bits for the Trace Value.".format(me,card.markers[Bits]))
	card.markers[Bits] = 0

def cancelTrace ( card, x=0,y=0):
	card.isFaceUp = True
	TraceValue = 0
	card.markers[Bits] = 0
	notify ("{} cancels the Trace Value.".format(me) )

#------------------------------------------------------------------------------
# Other functions
#-----------------------------------------------------------------------------

def intdamageDiscard(group,x=0,y=0):
	mute()
	if ( len(group) == 0 ):
		notify ( "{} cannot discard at random.".format(me) )
	else:
		card = group.random()
    		notify("{} discards {} at random.".format(me,card))
    		card.moveTo(me.Archives)

def addBrainDmg(group, x = 0, y = 0):
    me.counters['Brain Damage'].value +=1
    me.counters['Max Hand Size'].value -=1
    notify ("{} suffers 1 Brain Damage.".format(me) )
    intdamageDiscard(me.hand)


def addMeatNetDmg(group, x = 0, y = 0):
    notify ("{} suffers 1 Net or Meat Damage.".format(me) )
    intdamageDiscard(me.hand)



#------------------------------------------------------------------------------
# Other functions on card
#------------------------------------------------------------------------------
def scrAgenda(card, x = 0, y = 0):
	#if DifficultyLevels[card] >= 1:
	if ( TypeCard[card] == "Agenda" ):
		if confirm("Do you want to score this agenda?") == True:
			mute()
			card.isFaceUp = True
			ap = num(card.Stat)
			card.markers[Advance] = 0
			card.markers[Not_rezzed] = 0
			card.highlight = ScoredColor
			card.markers[Scored] += 1
#			card.moveToTable(270, 90)
			me.counters['Agenda Points'].value += ap
			
			if ds == "runner": agendaTxt = "liberates"
			else: agendaTxt = "scores"

			notify("{} {} {} and receives {} agenda point(s)".format(me, agendaTxt, card, ap))

			if ( me.counters['Agenda Points'].value >= 7) : notify("{} wins the game!".format(me))
			else: executeAutomations ( card, agendaTxt)

		else:
			whisper (" you decided not to score.")
	else:
		whisper ("You can't score this card")

def isRezzable (card):
	mute()
	Type = TypeCard[card]
	
	if ( Type == "Ice" or Type == "Node" or Type == "Upgrade"): return 0
	else: return -1

def intRez (card,Cost):

	if ( isRezzable(card) == -1):
		whisper ("Not a rezzable card")
		return
	else:
		mute()
		card.isFaceUp = True
		card.markers[Not_rezzed] -= 1
		if Cost != "free":
			rc = num(card.Cost)
			me.counters['Bit Pool'].value -= rc
			notify("{} payed {} and rezzed {}.".format(me, rc, card))
		else:
			notify("{} rezzed {} at no cost.".format(me, card))

		executeAutomations ( card, "rez" )

def rez(card, x = 0, y = 0):
	if card.markers[Not_rezzed] != 0:
      		intRez(card, "not free")
   	else:
      		notify ( "you can't rez a rezzed card")

def rezForFree (card, x = 0, y = 0):
	if card.markers[Not_rezzed] != 0:
      		intRez(card, "free")
	else:
      		notify ( "you can't rez a rezzed card")

def derez(card, x = 0, y = 0):
   if (card.markers[Not_rezzed] == 0):
	if ( isRezzable(card) == -1):
		whisper ("Not a rezzable card")
		return
	else:
      		mute()
		card.markers[Bits] = 0
      		card.markers[Not_rezzed] += 1
      		notify("{} derezzed {}".format(me, card))
      		executeAutomations ( card, "derez" )
   else:
      notify ( "you can't derez a unrezzed card")

def expose(card, x = 0, y = 0):
	if not card.isFaceUp:
		mute()
		card.isFaceUp = True
		notify("{} exposed {}".format(me, card))
	else:
		notify("You can't expose this card")

def rolld6(group, x = 0, y = 0):
    mute()
    n = rnd(1, 6)
    notify("{} rolls {} on a 6-sided die.".format(me, n))

def selectAsTarget (card, x = 0, y = 0):
    card.target(True)

def clear(card, x = 0, y = 0):
    notify("{} clears {}.".format(me, card))
    card.highlight = None
    card.target(False)

def intTrashCard (card, cost):
	mute()
	
	if (card.properties['Type'] == "Tracing"): return
	
	cardowner = card.owner
	if card.isFaceUp:
		
		if ( cost == "free") : notify("{} trash {} at no cost.".format(me, card))
		else: notify("{} payed {} and trash {}.".format(me, cost, card))
		executeAutomations ( card, "trash" )
		card.moveTo(cardowner.piles['Archives'])

	elif (ds == "runner" and cardowner == me) or (ds == "corp" and cardowner != me ): #i'm the runner and i trash my card or i 'm the corp and i trash a runner card
		card.moveTo(cardowner.piles['Archives'])
		if ( cost == "free") : notify ( "{} trashed {} at no cost.".format(me,card))
		else: notify("{} payed {} and trash {}.".format(me, cost, card))
		
	else: #i'm the corp and i trash my card or i'm the runner and i trash a corp's card
		card.moveTo(cardowner.piles['Archives H'])
		if ( cost == "free" ): notify("{} trashed a hidden card at no cost.".format(me))
		else: notify("{} payed {} and trashed a hidden card.".format(me,cost))
	
	

	#if MemoryRequirements[card] > 0: me.counters['Memory'].value += MemoryRequirements[card]

def trash_it(card, x = 0, y = 0):
	mute()
	cost = num(card.Stat)
	me.counters['Bit Pool'].value -= cost
	intTrashCard(card, cost)

def trashForFree (card, x = 0, y = 0):
	intTrashCard(card, "free")

def pay2AndTrash ( card, x=0, y=0):
	mute()
	me.counters['Bit Pool'].value -=2
	intTrashCard(card, 2 )

def useCardAbility(card,x=0,y=0):
	card.highlight = SelectColor
	notify ( "{} uses the ability of {}.".format(me,card) )
#------------------------------------------------------------------------------
# Hand Actions
#------------------------------------------------------------------------------
def intPlay(card, cost):
    global TypeCard
    mute() 
    TypeCard[card] = card.Type
    if card.Type == 'Resource' and (card.properties["Keyword 1"] == "Hidden" or card.properties["Keyword 2"] == "Hidden"): hiddenresource = 'yes'
    else: hiddenresource = 'no'
    if card.Type == 'Ice' or card.Type == 'Agenda' or card.Type == 'Node':
        card.moveToTable(0, 0, True) # I removed the different table positions for each type of card. Otherwise you signify what kind of card it is to the opponent!
        if card.Type == 'Ice': card.orientation ^= Rot90
        card.markers[Not_rezzed] += 1
        me.Actions -=1 
        notify("{} plays a card.".format(me))
    elif card.Type == 'Upgrade':
        if card.properties["Keyword 1"] != "Region":
            card.moveToTable(0, 0, True)
            card.markers[Not_rezzed] += 1
            notify("{} plays a card.".format(me))
        else:
            card.moveToTable(90, 0, False)
            if ( cost == "free"): notify("{} plays {} at no cost.".format(me, card))
            else:
                me.counters['Bit Pool'].value -= num(card.Cost)
                notify("{} paid {} and plays {}.".format(me, card.Cost, card))
        me.Actions -=1
    elif card.Type == 'Program' or card.Type == 'Prep' or card.Type == 'Resource' or card.Type == 'Hardware':
        me.Memory -= num(card.properties["MU Required"])
        me.Actions -=1
        if card.Type == 'Program': card.moveToTable(-180, 90, False)
        if card.Type == 'Prep': card.moveToTable(0, 0, False)
        if card.Type == 'Hardware': card.moveToTable(-180, 180, False)
        if card.Type == 'Resource' and hiddenresource == 'no': card.moveToTable(-180, 270, False)
        if card.Type == 'Resource' and hiddenresource == 'yes':
            card.moveToTable(-180, 270, True)
            notify("{} installs a card.".format(me))
            executeAutomations(card,"play")
            return
        if cost == "not_free":
            me.counters['Bit Pool'].value -= num(card.Cost)
            notify("{} pays {} and plays {}.".format(me, card.Cost, card))
        else: notify("{} plays {} at no cost.".format(me, card))
    else:
        card.moveToTable(0, 0, False)
        me.Actions -=1
        if cost == "not_free":
            me.counters['Bit Pool'].value -= num(card.Cost)
            notify("{} pays {} and plays {}.".format(me, card.Cost, card))
        else: notify("{} plays {} at no cost.".format(me, card))               
    executeAutomations ( card, "play" )

def playForFree(card, x = 0, y = 0):
	intPlay(card,"free")

def play(card, x = 0, y = 0):
	intPlay(card,"not_free")

def movetoTopOfStack (card):
	mute()
	Stack = me.piles['R&D/Stack']
	card.moveTo(Stack)
	if ( ds == "runner"): nameStack = "Stack"
	else: nameStack = "R&D"

	notify ( "{} moves a card to top of {}.".format(me,nameStack) )

def movetoBottomOfStack (card):
	mute()
	Stack = me.piles['R&D/Stack']
	card.moveToBottom(Stack)
	if ( ds == "runner"): nameStack = "Stack"
	else: nameStack = "R&D"

	notify ( "{} moves a card to Bottom of {}.".format(me,nameStack) )

def handtoArchivesH (card):

	if ( ds == "runner"): return
	mute()
	Stack = me.piles['Archives H']
	card.moveTo(Stack)
	
	notify ("{} moves a card to Archives H.".format(me))

def handDiscard(group):
	mute()
	card = group.random()
	if card == None: return
	if ds == "corp" :
		card.moveTo(me.piles['Archives H'])
    		notify("{} discards a card at random.".format(me))
    		
	else:
		card.moveTo(me.Archives)
		notify("{} discards {} at random.".format(me,card))
    		
def showatrandom(group):
	mute()
	card = group.random()
	if card == None: return
	card.moveToTable(0, 0, False)
	notify("{} show {} at random.".format(me,card))

def handtoStack (group):
	mute()
	Stack = me.piles['R&D/Stack']
	for c in me.hand: c.moveTo(Stack)
	#Archives.shuffle()
	if ( ds == "runner"):
		nameHand = "Hand"
		nameStack = "Stack"
	else:
		nameHand = "HQ"
		nameStack = "R&D"

	notify ("{} moves {} to {}.".format(me,nameHand,nameStack))


#------------------------------------------------------------------------------
# Pile Actions
#------------------------------------------------------------------------------
def shuffle(group):
	group.shuffle()

def draw(group, x = 0, y = 0):
	if len(group) == 0: return
	mute()
	group[0].moveTo(me.hand)
	notify("{} draws a card.".format(me))

def drawManySilent(group, count):
	SSize = len(group)
	if SSize == 0: return 0
	mute()
	if ( count > SSize) : count=SSize
	for c in group.top(count): c.moveTo(me.hand)
	return count

def drawMany(group, count = None):
	SSize = len(group)
	if SSize == 0: return
	mute()
	if count == None: count = askInteger("Draw how many cards?", 5)
	if ( count > SSize) : count=SSize
	for c in group.top(count): c.moveTo(me.hand)

	notify("{} draws {} cards.".format(me, count))

def toarchives(group = me.piles['Archives H']):
	mute()
	Archives = me.Archives
	for c in group: c.moveTo(Archives)
	#Archives.shuffle()
	notify ("{} moves Hidden Archives to Archives.".format(me))

def archivestoStack(group):
	mute()
	Stack = me.piles['R&D/Stack']
	for c in group: c.moveTo(Stack)
	#Archives.shuffle()
	if ( ds == "runner"):
		nameTrash = "Trash"
		nameStack = "Stack"
	else:
		nameTrash = "Archives"
		nameStack = "R&D"
	notify ("{} moves {} to {}.".format(me,nameTrash,nameStack))

def mill(group):
	if len(group) == 0: return
	mute()
    	count = askInteger("Mill how many cards?", 1)
	if ( ds == "runner"):
    		for c in group.top(count): c.moveTo(me.Archives)
		nameStack = "Stack"
		nameTrash = "Trash"
	else:
		for c in group.top(count): c.moveTo(me.piles['Archives H'])
		nameStack = "HQ"
		nameTrash = "Archives H"

    	notify("{} mills the top {} cards from {} to {}.".format(me, count,nameStack,nameTrash))

def moveXtopCardtoBottomStack(group):
	if len(group) == 0: return
	mute()
    	count = askInteger("Move how many cards?", 1)
	for c in group.top(count): c.moveToBottom(group)
	if ( ds == "runner"): nameStack = "Stack"
	else: nameStack = "R&D"

    	notify("{} moves the top {} cards from {} to bottom of {}.".format(me, count,nameStack,nameStack))


def checkDeckNoLimit (group):
	if ( ds == ""):
		whisper ("Choose a side first.")
		return 

	notify (" -> Checking deck of {} ...".format(me) )
	ok = 0
	loDeckCount = len(group)

	if ( loDeckCount < 45 ):
		ok = -1
		notify ( "- Error: only {} cards in {}'s Deck.".format(loDeckCount,me) )

	mute()
	if ( ds == "corp"):
		loAP = 0.0
		loRunner = 0
		for card in group:
			card.moveTo(me.piles['Archives'])
     			if ( re.match(r'\bAgenda\b', card.properties["Type"]) ): loAP += num(card.Stat)
			if ( card.properties["Player"] == "runner"): loRunner = 1
			card.moveToBottom(group)

		if ( loAP/loDeckCount < 2.0/5.0 ):
			notify ( "- Error: only {} Agenda Points in {}'s R&D.".format(loAP/1,me) )
			ok = -1

		if ( loRunner == 1 ):
			notify ( "- Error: Runner Cards found in {}'s R&D.".format(me) )
			ok = -1
	else:
		loCorp = 0
		for card in group:
			card.moveTo(me.piles['Archives'])
     			if (card.properties["Player"]== "corp"): loCorp = 1
			card.moveToBottom(group)

		if ( loCorp == 1 ):
			notify ( "- Error: Corp Cards found in {}'s Stack.".format(me) )
			ok = -1


	if ( ok == 0 ): notify (" -> Deck of {} OK !".format(me) )

	return ok

#------------------------------------------------------------------------------
# Automations
#------------------------------------------------------------------------------
def executeAutomations ( card, action ):
	
	if ( TurnAutomation != 0): return

	AutoScript = card.properties ["AutoScript"]

	if (  AutoScript == "") : return
	Execute = 0

	if ( action == "play" or action == "rez" or action == "scores"): Execute = 1
	
	if ( ( (action == "trash" and card.markers[Not_rezzed] == 0) or action == "derez") and AutoScript.find("ReverseYes") != -1 ): Execute = -1

	if ( Execute == 0): return

	Param1 = num(card.ParamAS1)*Execute
	Param2 = num(card.ParamAS2)*Execute

	if ( AutoScript == "autoGainXDrawY" ): autoGainXDrawY ( card, Param1, Param2 )
	elif ( AutoScript == "autoGainXIfY"): autoGainXIfY( card, Param1, Param2 )
	elif ( AutoScript == "autoGainX" ) : autoGainX ( card, Param1, Param2 )
	elif ( AutoScript == "autoDrawX" ) : autoDrawX ( card, Param1, Param2 )
	elif ( AutoScript == "autoAddBitsCounter" ): autoAddBitsCounter( card, Param1, Param2 )
	elif ( AutoScript == "autoGainXYTags"): autoGainXYTags( card, Param1, Param2 )
	elif ( AutoScript == "autoGainXYBadPub"): autoGainXYBadPub( card, Param1, Param2 )
	elif ( AutoScript.find("autoAddMUAndBitsCounter") != -1): autoAddMUAndCounter ( card, Param1, Param2 )
	elif ( Autoscript.find("autoaddMUHandSizeBitsCounter") != -1 ): autoaddMUHandSizeBitsCounter ( card, Param1, Param2 )
	elif ( AutoScript.find("autoAddMU") != -1 ): autoAddMU( card, Param1, Param2 )
	elif ( AutoScript.find("autoAddHandSize") != -1 ): autoAddHandSize( card, Param1, Param2 )
	
	else: return

def autoGainXDrawY ( card, Param1, Param2 ):
	mute()
	me.counters['Bit Pool'].value += Param1
	drawManySilent ( me.piles['R&D/Stack'], Param2)
	notify ( "--> {} gains {} bits and draws {} cards.".format(me,Param1,Param2) )

def autoGainX ( card, Param1,Param2 ):
	mute()
	me.counters['Bit Pool'].value += Param1
	notify ( "--> {} gains {} bits.".format(me,Param1) )

def autoDrawX ( card, Param1,Param2):
	mute()
	drawManySilent ( me.piles['R&D/Stack'], Param1)
	notify ( "--> {} draws {} card(s).".format(me,Param1) )

def autoAddBitsCounter ( card, Param1, Param2 ):
	intAddBits ( card, Param1)

def autoAddMU ( card, Param1, Param2 ):
	mute()
	Owner = card.owner
	Owner.counters['Memory'].value +=Param1
	notify (" --> {} max MU is now {}.".format(Owner,Owner.counters['Memory'].value) )

def autoAddMUAndCounter ( card, Param1, Param2 ):
	#mute()
	autoAddMU ( card, Param1, Param2 )
	intAddBits ( card, Param2)

def autoAddHandSize ( card, Param1, Param2):
	Owner = card.owner
	Owner.counters['Max Hand Size'].value +=Param1
	notify ("--> {} max Hand Size is now {}.".format(Owner,Owner.counters['Max Hand Size'].value) )

def autoaddMUHandSizeBitsCounter ( card, Param1, Param2):
	autoAddMuAndCounter ( card, Param1, Param2)
	autoaddHandSize ( card, Param1, 0)

def autoGainXYTags( card, Param1, Param2):
	autoGainX ( card, Param1, 0)
	me.counters['Tags'].value +=Param2
	notify ( "--> {} gets {} Tags.".format(me,Param2) )

def autoGainXYBadPub ( card, Param1, Param2):
	autoGainX ( card, Param1, 0)
	me.counters['Bad Publicity'].value +=Param2
	notify ( "--> {} gets {} Bad Publicy Points.".format(me,Param2) )

def autoGainXIfY ( card, Param1, Param2):
	if ( me.counters['Bit Pool'].value >= Param2): autoGainX ( card, Param1, 0)